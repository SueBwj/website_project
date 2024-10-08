from common.file_process import load_json, save_json
from common.dir_path import prompt_summary_dir,roleplay_history_dir,topic_summary_dir
from common.openai import client
import os
import io
import hashlib
import json  # 导入 json 库，用于处理 JSON 数据
import re

class RoleplayService:


    def remove_potential_prefix(text):
        """
        尝试去除字符串中的潜在前缀（例如用户名）。

        Args:
            text: 要处理的字符串。

        Returns:
            去除前缀后的字符串。
        """
        match = re.search(r'^.*?:\s*(.+)', text)
        if match:
            return match.group(1)
        return text

    @staticmethod
    def escape_special_chars(text):
        """
        将字符串中的特殊字符转换为 JSON 兼容的转义序列。

        Args:
            text: 要转义的字符串。

        Returns:
            包含转义序列的字符串。
        """
        return json.dumps(text)

    @staticmethod
    def add_comment_and_siblings(related_comments, data, parent_comment):
        """
        辅助函数：添加目标评论及其同级评论到 related_comments 列表。
        """
        if parent_comment:
            related_comments.append(parent_comment)
        related_comments.append(data)
        if parent_comment and "subcomments" in parent_comment:
            for sibling in parent_comment["subcomments"]:
                related_comments.append(sibling)

    @staticmethod
    def find_comments_by_content(data, target_content, related_comments=None, parent_comment=None):
        """
        递归搜索特定内容（在 "content" 或 "premises" 中）并返回其完整讨论串
        （包括父级评论、同级评论和子评论）。

        Args:
            data: JSON 数据。
            target_content: 要搜索的目标内容。
            related_comments: 累积相关评论的列表（初始化为 None）。
            parent_comment: 当前正在处理的评论的父级评论。

        Returns:
            相关评论列表，如果未找到 target_content，则返回 None。
        """

        # 1. 初始化 related_comments 列表
        if related_comments is None:
            related_comments = []

            # 去除 target_content 中的潜在前缀
        target_content = RoleplayService.remove_potential_prefix(target_content)

        # 2. 判断 data 的类型
        if isinstance(data, list):
            # 如果 data 是列表（顶层评论列表）
            for item in data:
                # 遍历每个评论项
                # 递归调用 find_comments_by_content 函数，将当前评论项作为 data，
                # related_comments 列表和 parent_comment 传递给递归调用
                RoleplayService.find_comments_by_content(item, target_content, related_comments, parent_comment)
        elif isinstance(data, dict):
            # 如果 data 是字典（单个评论对象）

            # 3. 检查 content 字段是否匹配
            if "content" in data and data["content"] == target_content:
                # 如果 content 字段存在且匹配 target_content
                RoleplayService.add_comment_and_siblings(related_comments, data, parent_comment)

            # 4. 检查 major_claim.content 字段是否匹配
            elif "major_claim" in data and "content" in data["major_claim"] and data["major_claim"]["content"] == target_content:
                # 如果 major_claim.content 字段存在且匹配 target_content
                RoleplayService.add_comment_and_siblings(related_comments, data, parent_comment)

            # 5. 检查 premises 列表中是否包含目标内容
            elif "premises" in data and isinstance(data["premises"], list):
                for premise in data["premises"]:
                    if premise == target_content:
                        RoleplayService.add_comment_and_siblings(related_comments, data, parent_comment)
                        break # 找到匹配项后跳出循环

            # 6. 递归搜索 subcomments 字段
            if "subcomments" in data:
                RoleplayService.find_comments_by_content(data["subcomments"], target_content, related_comments, data)
            # 7. 递归搜索 major_claim.claims 字段
            if "major_claim" in data and "claims" in data["major_claim"]:
                RoleplayService.find_comments_by_content(data["major_claim"]["claims"], target_content, related_comments, data)
            # 8. 递归搜索 claims 字段
            if "claims" in data:
                RoleplayService.find_comments_by_content(data["claims"], target_content, related_comments, data)

        # 9. 返回结果
        return related_comments if related_comments else None
    
    @staticmethod
    def extract_comments(data):
        """
        提取文件里的comment.
        Extracts all 'comment' fields from the nested JSON data.

        Args:
            data: The JSON data (can be a list or a dictionary).

        Returns:
            A list containing all 'comment' values from the JSON data.
        """

        comments = []

        if isinstance(data, list):
            for item in data:
                comments.extend(RoleplayService.extract_comments(item))  # Extend the list with comments from sub-items
        elif isinstance(data, dict):
            if "comment" in data:
                comments.append(data["comment"])
            # Recursively call extract_comments on subcomments
            if "subcomments" in data:
                comments.extend(RoleplayService.extract_comments(data["subcomments"]))
            # Recursively call extract_comments on major_claim (if needed)
            if "major_claim" in data:
                comments.extend(RoleplayService.extract_comments(data["major_claim"]))
        # print(comments)
        comments_str = "".join(comments)
        # print(comments_str)
        # print(2)
        return comments_str
    

    @staticmethod
    def insertClaim(claim:str,topic_id)->list:
        """
        返回插入了claim相关评论后的数据
        """
        
        # 提取claim相关评论
        topic_summary_path = topic_summary_dir.joinpath(f"{topic_id}.json") # 加载 JSON 数据
        topic_summary_file = load_json(topic_summary_path)
        
        target = claim
        target = RoleplayService.escape_special_chars(target)
        target = json.loads(target)
        
        found_comments = RoleplayService.find_comments_by_content(topic_summary_file, target)
        
        with io.StringIO() as buffer:
            json.dump(found_comments, buffer, indent=4, ensure_ascii=False)
            found_comments_json = buffer.getvalue()  # 获取字符串缓冲区中的 JSON 数据
       
        found_comments_dict = json.loads(found_comments_json)
        all_comments = RoleplayService.extract_comments(found_comments_dict)


        roleplay_file = prompt_summary_dir.joinpath('roleplay.json')
        data = load_json(roleplay_file)

        # 将观点插入到prompt
        sys_content = data[0]['content']
        prompt = sys_content.replace('{观点}',claim)
        data[0]['content'] = prompt

        # 将 all_comments 插入到 data 中
        data[0]['comment'] = data[0]['comment'].replace('{评论}', all_comments) 
        return claim, data


    @staticmethod
    def saveHistory(data:list, user_id:str, claim:str):
        # 使用哈希函数生成claim的唯一标识符
        claim_hash = hashlib.md5(claim.encode()).hexdigest()[:8]
        # 保存file到roleplay history file之中
        file = roleplay_history_dir.joinpath(f'chat_{user_id}_{claim_hash}.json')
        # 如果不存在文件就直接创建
        if not os.path.exists(file):
            save_json(file, data)
        else:
            # 如果存在文件就直接追加
            old_data = load_json(file)
            for item in data:
                old_data.append(item)
            save_json(file, old_data)
    
    @staticmethod
    def getGeneratedText(messages):
        """
        返回gpt的回复信息
        """
        # 使用OpenAI客户端生成回复
        completion = client.chat.completions.create(
            model="gpt-4", 
            messages=messages,
            temperature=0.5,  # 控制输出的随机性，0.0到1.0之间
            max_tokens=3000  # 限制响应的长度
        )
        
        # 从响应中提取生成的文本
        generated_text = completion.choices[0].message.content
        
        return generated_text
    
    @staticmethod
    def returnFirstReply(claim:str,user_id:str,topic_id):
        # 先插入观点
        claim, messages = RoleplayService.insertClaim(claim, topic_id)
        # 获取reply
        reply = RoleplayService.getGeneratedText(messages)
        messages.append({
            'role':'system',
            'content':f'{reply}'
        })
        # 将记录保存
        RoleplayService.saveHistory(messages, user_id, claim)
        return reply

    @staticmethod
    def returnReply(user_cookie:str, claim:str ,message:str):
        """对用户的消息进行回应"""
        # 根据user_id和claim取出对应的历史文件
        claim_hash = hashlib.md5(claim.encode()).hexdigest()[:8]
        data = []
        data.append({
            'role':'user',
            'content': f'{message}'
        })
        reply = RoleplayService.getGeneratedText(data)
        data.append({
            'role':'system',
            'content': f'{reply}'
        })
        RoleplayService.saveHistory(data, user_cookie, claim)
        return reply

    @staticmethod
    def file_exist(user_cookie:str, claim:str):
        """
        判断文件是否存在
        """
        claim_hash = hashlib.md5(claim.encode()).hexdigest()[:8]
        file = roleplay_history_dir.joinpath('chat_'+ str(user_cookie) + '_' + str(claim_hash) + '.json')
        return os.path.exists(file)


class RoleplayPromptService:

    @staticmethod
    def generate_question(claim: str,user_cookie:str,topic_id = 4)->list:
        """
        根据 claim 生成 2-3 个问题, 返回一个列表包含三个问题
        """
        # # 提取claim相关评论
        # topic_summary_path = topic_summary_dir.joinpath(f"{topic_id}.json") # 加载 JSON 数据
        # topic_summary_file = load_json(topic_summary_path)
        
        # target = claim
        
        # found_comments = RoleplayService.find_comments_by_content(topic_summary_file, target)
        
        # with io.StringIO() as buffer:
        #     json.dump(found_comments, buffer, indent=4, ensure_ascii=False)
        #     found_comments_json = buffer.getvalue()  # 获取字符串缓冲区中的 JSON 数据
       
        # found_comments_dict = json.loads(found_comments_json)
        # all_comments = RoleplayService.extract_comments(found_comments_dict)

        # 提取claim相关评论
        topic_summary_path = topic_summary_dir.joinpath(f"{topic_id}.json") # 加载 JSON 数据
        topic_summary_file = load_json(topic_summary_path)
        
        target = claim
        target = RoleplayService.escape_special_chars(target)
        target = json.loads(target)
        
        found_comments = RoleplayService.find_comments_by_content(topic_summary_file, target)
        
        with io.StringIO() as buffer:
            json.dump(found_comments, buffer, indent=4, ensure_ascii=False)
            found_comments_json = buffer.getvalue()  # 获取字符串缓冲区中的 JSON 数据
       
        found_comments_dict = json.loads(found_comments_json)
        all_comments = RoleplayService.extract_comments(found_comments_dict)


        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一位专家，需要根据给定的观点生成 3 个问题，用于用户选择。"},
                {"role": "user", "content": f"请根据以下观点生成问题：{claim},同时你可以参考下面评论内容: {all_comments}. 每个问题字数不超过10个字,直接给出问题即可"}
            ],
            max_tokens=100
        )

        return response.choices[0].message.content.split('\n')