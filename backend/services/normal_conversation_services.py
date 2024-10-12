import os
from common.openai import client
from common.dir_path import normal_chat_history_dir, summary_dir
from common.file_process import save_json,load_json


class NormalConversationService:
    @staticmethod
    def loadEventBackground(topic:str)->str:
        """
        加载事件背景
        """
        file = summary_dir.joinpath(f'{topic}.txt')
        with open(file, 'r', encoding='utf-8') as f:
            data = f.read()
            return data
        return ''

    @staticmethod
    def returnReply(user_cookie:str,message:str, topic:str):
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
        event_background = NormalConversationService.loadEventBackground(topic)
        if event_background and not os.path.exists(file):
            # 如果第一次聊天，则需要加上事件背景
            messages.append({"role": "user", "content": f"event background: {event_background}"})
        messages.append({"role": "user", "content": message})
        # 使用OpenAI客户端生成回复
        completion = client.chat.completions.create(
            model="gpt-4o", 
            messages=messages,
            temperature=0.5,  # 控制输出的随机性，0.0到1.0之间
            max_tokens=5000  # 限制响应的长度
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
