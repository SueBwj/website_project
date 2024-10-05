from common.file_process import load_json, save_json
from common.dir_path import prompt_summary_dir,roleplay_history_dir
from common.openai import client
import os
import hashlib

class RoleplayService:

    @staticmethod
    def insertClaim(claim:str)->list:
        """
        返回插入了claim后的数据
        """
        roleplay_file = prompt_summary_dir.joinpath('roleplay.json')
        data = load_json(roleplay_file)

        # 将观点插入到prompt
        sys_content = data[0]['content']
        prompt = sys_content.replace('{观点}',claim)
        data[0]['content'] = prompt

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
    def returnFirstReply(claim:str,user_id:str):
        # 先插入观点
        claim, messages = RoleplayService.insertClaim(claim)
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
    def generate_question(claim: str,user_cookie:str)->list:
        """
        根据 claim 生成 2-3 个问题, 返回一个列表包含三个问题
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一位专家，需要根据给定的观点生成 3 个问题，用于用户选择。"},
                {"role": "user", "content": f"请根据以下观点生成问题：{claim},每个问题字数不超过10个字,直接给出问题即可"}
            ],
            max_tokens=100
        )

        return response.choices[0].message.content.split('\n')