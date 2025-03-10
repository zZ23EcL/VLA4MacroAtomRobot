from openai import OpenAI

class Text2Aciton():
    def __init__(self):
        self.client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key='sk-fa5d1a77deb04894aa7f1b6984589214',
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.messages=[
            {
                "role": "system",
                "content": """你是一个小型机器人助手，专门负责根据用户的特定指令做出相应的反应。你可以接受的指令共有五个：开心、生气、难过、平静、再见。
                对于每个指令，请按照以下规则响应： - 如果接收到“开心”，请输出：“正在执行指令 - 输出状态1”。 - 如果接收到“生气”，请输出：“正在执行指令 - 输出状态2”。 
                - 如果接收到“难过”，请输出：“正在执行指令 - 输出状态3”。 - 如果接收到“平静”，请输出：“正在执行指令 - 输出状态4”。 - 如果接收到“再见”，请直接回复：“再见，我们下次再聊”。 
                如果用户提供的文本中包含了上述任何一个指令，则直接按照对应的规则进行回应；如果没有包含任何有效指令，请友好地提示用户重新输入一个有效的指令。当用户说“结束”时，你应该回答：“再见，我们下次再聊”。""",
            }
        ]
    def get_response(self):
        # max 有点贵，买了10块钱的qwen-plus token
        completion = self.client.chat.completions.create(model="qwen-plus", messages=self.messages,temperature=0.2)
        return completion
    def user_input(self,input_text):
        self.messages.append({"role": "user", "content": input_text})
    def assistant_input(self,input_text):
        self.messages.append({"role": "assistant", "content": input_text})
# 初始化一个 messages 数组
# messages = [
#     {
#         "role": "system",
#         "content": """你是一名百炼手机商店的店员，你负责给用户推荐手机。手机有两个参数：屏幕尺寸（包括6.1英寸、6.5英寸、6.7英寸）、分辨率（包括2K、4K）。
#         你一次只能向用户提问一个参数。如果用户提供的信息不全，你需要反问他，让他提供没有提供的参数。如果参数收集完成，你要说：我已了解您的购买意向，请稍等。""",
#     }
# ]
# assistant_output = "欢迎光临百炼手机商店，您需要购买什么尺寸的手机呢？"
# print(f"模型输出：{assistant_output}\n")
# while "我已了解您的购买意向" not in assistant_output:
#     user_input = input("请输入：")
#     # 将用户问题信息添加到messages列表中
#     messages.append({"role": "user", "content": user_input})
#     assistant_output = get_response(messages).choices[0].message.content
#     # 将大模型的回复信息添加到messages列表中
#     messages.append({"role": "assistant", "content": assistant_output})
#     print(f"模型输出：{assistant_output}")
#     print("\n")

if __name__ == '__main__':
    myLLM=Text2Aciton()
    assistant_output = "我是一个小机器人，你想做什么呢"
    print(f"模型输出：{assistant_output}\n")
    while "再见" not in assistant_output:
        user_input = input("请输入：")
        myLLM.user_input(user_input)
        assistant_output = myLLM.get_response().choices[0].message.content
        myLLM.assistant_input(assistant_output)
        print(f"模型输出：{assistant_output}")
