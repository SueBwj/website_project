from common.file_process import load_json, save_json
from common.dir_path import prompt_summary_dir,roleplay_history_dir,critical_thinking_dir,example_dir,data_dir
from common.openai import client
from common.cookies import setUserId,getUserId
import os
import json
import re

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
        # 保存file到roleplay history file之中
        file = roleplay_history_dir.joinpath(f'chat_{user_id}_{claim}.json')
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
        file = roleplay_history_dir.joinpath('chat_'+ str(user_cookie) + '_' + str(claim) + '.json')
        data = load_json(file)
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
        file = roleplay_history_dir.joinpath('chat_'+ str(user_cookie) + '_' + str(claim) + '.json')
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
    

class CriticalThinkingService:

    @staticmethod
    def exercise_exists(user_cookie: str) -> bool:
        """
        检查用户是否已经开始进行习题训练.
        """
        file_path = critical_thinking_dir.joinpath(f"exercises_{user_cookie}.json")
        return os.path.exists(file_path)

    @staticmethod
    def generate_exercises(user_cookie: str) -> list:
        """
        生成一组新的批判性思维习题并存储用户 ID 和习题信息.
        """
        user_id  = getUserId()  # 获取用户 ID 和响应对象

        # 清理 user_id，移除所有非字母数字字符
        sanitized_user_id = re.sub(r'[^a-zA-Z0-9]', '_', user_id)

        # 读取用于生成批判性思维题目的comment
        comment_file_path = data_dir.joinpath('Comment.txt')
        with comment_file_path.open(encoding='utf-8') as f:
            comment = f.read()

        # 设置通用参数
        number = 2  # 生成题目的数量
        response_json_choice = {
            "Statement": "...",
            "Question": "...",
            "Options": {
                "a": "...",
                "b": "...",
            },
            "Correct": "correct answer",
            "Explanation": "explanation of the correct answer"
        }
        response_json_write = {"Question": "..."}

        # 调用 QuizService 生成不同技能的测验
        exercises = [
            QuizService.generate_quiz(comment, number, response_json_choice, "choice", example_dir.joinpath('Argument_test', 'argument_example.json'), "Evaluate the effectiveness of arguments"),
            QuizService.generate_quiz(comment, number, response_json_choice, "choice", example_dir.joinpath('Assumption_test', 'assumption_example.json'), "Identify when an assumption has been made"),
            QuizService.generate_quiz(comment, number, response_json_choice, "choice", example_dir.joinpath('Deductions_test', 'Deduction_example.json'), "Use deductive reasoning"),
            QuizService.generate_quiz(comment, number, response_json_choice, "choice", example_dir.joinpath('Inference_test', 'Inference_example.json'), "Arrive at correct inferences"),
            QuizService.generate_quiz(comment, number, response_json_choice, "choice", example_dir.joinpath('Interpret_info_test', 'Interpret_info_example.json'), "Reach logical conclusions"),
            QuizService.generate_quiz(comment, number, response_json_write, "write", example_dir.joinpath('Argument_test', 'argument_example.json'), "Writing persuasive comment")
        ]

        # 为每个习题分配唯一的 id
        for idx, exercise in enumerate(exercises):
            exercise["id"] = idx + 1
        
        # 保存习题到文件
        file_path = critical_thinking_dir.joinpath(f"exercises_{sanitized_user_id}.txt")
        save_json(file_path, exercises)

        return exercises


    @staticmethod
    def get_exercises(user_cookie: str) -> list:
        """
        获取用户之前生成的习题.
        """
        file_path = critical_thinking_dir.joinpath(f"exercises_{user_cookie}.json")
        return load_json(file_path)

    @staticmethod
    def check_answer(user_cookie: str, exercise_id: int, answer: str) -> tuple[bool, str]:
        """
        检查用户提交的答案是否正确，并返回反馈信息.
        """
        exercises = CriticalThinkingService.get_exercises(user_cookie)
        for exercise in exercises:
            if exercise["id"] == exercise_id:
                # 加载 prompt 文件
                prompt_file = prompt_summary_dir.joinpath('check_answer.json')
                prompt_data = load_json(prompt_file)

                # 构建 LLM 请求消息
                messages = [
                    {"role": "system", "content": f"{prompt_data['instruction']}\n\n**task:**\n{prompt_data['task']}"},
                    {"role": "user", "content": f"问题：{exercise.get('Question', '')}\n预期答案：{exercise.get('Correct', '')}\n题目描述：{exercise.get('Statement', '')}\n选项：{exercise.get('options', '')}\n解释：{exercise.get('Explanation', '')}\n用户答案：{''}"} 
                ]

                # 调用 LLM 获取评估结果
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=500
                )

                # 解析 LLM 响应
                feedback = response.choices[0].message.content

                # 判断答案是否正确
                if "正确" in feedback:
                    return True, feedback
                else:
                    return False, feedback
        return False, "找不到该习题。"

    @staticmethod
    def generate_guiding_question(user_cookie: str, exercise_id: int) -> str:
        """
        生成苏格拉底式引导问题.
        """
        exercises = CriticalThinkingService.get_exercises(user_cookie)
        for exercise in exercises:
            if exercise["id"] == exercise_id:
                # 加载 prompt 文件
                prompt_file = prompt_summary_dir.joinpath('generate_guiding_question.json')
                prompt_data = load_json(prompt_file)

                # 构建 LLM 请求消息
                messages = [
                    {"role": "system", "content": f"{prompt_data['instruction']}\n\n**task:**\n{prompt_data['task']}"},
                    {"role": "user", "content": f"问题：{exercise.get('Question', '')}\n预期答案：{exercise.get('Correct', '')}\n题目描述：{exercise.get('Statement', '')}\n选项：{exercise.get('options', '')}\n解释：{exercise.get('Explanation', '')}\n用户答案：{''}"} 
                ]

                # 调用 LLM 获取引导问题
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=300
                )

                # 解析 LLM 响应
                guiding_question = response.choices[0].message.content

                return guiding_question
        return "找不到该习题。"


class QuizService:

    @staticmethod
    def generate_quiz(comment, number, response_json, test_type, example_path, ability):
        """
        生成批判性思维习题.
        """
        with open(example_path, encoding='utf-8') as f:
            argument_example = f.read()

        prompt = f"""
        **Comment:** \n {comment} \n
        **You are an expert critical thinking question generator. You are expert in generating questions to test the ability of '{ability}'** 
        Given the above comment from reddit, it is your job to create **a quiz of {number} single choice questions** for Critical Thinking Class students.
        Make sure the questions are not repeated and check all the questions to be confirmed the text as well.
        Make sure to format your response like RESPONSE_JSON below and use it as a guide. 
        Ensure to make **{number}** single choice questions
        **RESPONSE_JSON:** \n {response_json} \n
        **Example:** See the example questions below with the correct answers and explanations given. \n {argument_example} \n
        Attention: Your output should be as plain text without any code block markers!!! 
        """

        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}]
        )

        quiz_output = response.choices[0].message.content.strip()

        try:
            output = json.loads(quiz_output)  # 尝试将返回内容加载为 JSON
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON. The returned output was:")
            print(quiz_output)  # 调试信息
            return None

        if isinstance(output, list):
            output = output[0]

        if isinstance(output, dict):
            output["type"] = test_type
        else:
            print("Unexpected format: output is neither a list nor a dictionary.")
            return None

        return output
