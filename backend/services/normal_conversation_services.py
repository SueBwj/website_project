import os
from common.openai import client
from common.dir_path import normal_chat_history_dir
from common.file_process import save_json,load_json


class NormalConversationService:
    @staticmethod
    def returnReply(user_cookie:str,message:str):
        """
        返回gpt的回复信息
        """
        messages = []
        file = normal_chat_history_dir.joinpath(f'{user_cookie}.json')
        if os.path.exists(file):
            # 如果存在文件就直接追加,导出先前的聊天记录
            old_data = load_json(file)
            for item in old_data:
                messages.append(item)
        messages.append({"role": "user", "content": message})
        # 使用OpenAI客户端生成回复
        completion = client.chat.completions.create(
            model="gpt-4", 
            messages=messages,
            temperature=0.5,  # 控制输出的随机性，0.0到1.0之间
            max_tokens=3000  # 限制响应的长度
        )
        # 从响应中提取生成的文本
        generated_text = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": generated_text})
        # 将记录保存
        NormalConversationService.saveHistory(messages, user_cookie)
        return generated_text

    @staticmethod
    def saveHistory(messages, user_cookie):
        """
        将记录保存
        """
        file = normal_chat_history_dir.joinpath(f'{user_cookie}.json')
        # 将记录保存
        save_json(file, messages)
