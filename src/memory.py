from termcolor import colored

class Memory:
    def __init__(self):
        self.conversation = []

    # def add_message(self, role, content):
    #     message = {"role": role, "content": content}
    #     self.conversation.append(message)
    
    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation.append(message)

    def display_full_conversation(self):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "tool": "magenta",
        }
        for message in self.conversation:
            # print(message)
            if "tool_calls" in message:
                func = message["tool_calls"][0].function
                print(
                    colored(
                        f"{message['role']}: {func}\n",
                        role_to_color[message["role"]],
                    )
                )
            else:
                print(
                    colored(
                        f"{message['role']}: {message['content']}\n",
                        role_to_color[message["role"]],
                    )
                )
        
    def display_last_message(self):
        role_to_color = {
            "system": "red",
            "user": "green",
            "assistant": "blue",
            "tool": "magenta",
        }
        message = self.conversation[-1]
        # print(message)
        if "tool_calls" in message:
            func = message["tool_calls"][0].function
            print(
                colored(
                    f"{message['role']}: {func}\n",
                    role_to_color[message["role"]],
                )
            )
        else:
            print(
                colored(
                    f"{message['role']}: {message['content']}\n",
                    role_to_color[message["role"]],
                )
            )
