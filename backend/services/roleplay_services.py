from common.file_process import load_json, save_json
from common.dir_path import prompt_summary_dir,roleplay_history_dir
from datetime import datetime
import os

class RoleplayService:

    @staticmethod
    def insertClaim(claim)->list:
        """
        返回插入了claim后的数据
        """
        roleplay_file = prompt_summary_dir.joinpath('roleplay.json')
        data = load_json(roleplay_file)

        # 将观点插入到prompt
        sys_content = data[0]['content']
        prompt = sys_content.replace('{观点}',claim)
        data[0]['content'] = prompt

        return data

        

    @staticmethod
    def saveHistory(data:list):
        # 保存file到roleplay history file之中
        file = roleplay_history_dir.joinpath('chat_test.json')
        # 如果不存在文件就直接创建
        if not os.path.exists(file):
            save_json(file, data)
        else:
            # 如果存在文件就直接追加
            old_data = load_json(file)
            for item in data:
                old_data.append(item)
            save_json(file, old_data)
        