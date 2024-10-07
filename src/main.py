import aoai
import bing
import memory
import json
import get_workdays
from env import TASK_DESCRIPTION


def agent_chat(conversation, tool_list=None, tool_choice=None):
    response = aoai.call_llm_API(
        conversation, tool_list=tool_list, tool_choice=tool_choice
    )
    # response_message = response.choices[0].message
    res = response.choices[0]
    # print(res.message)
    if res.finish_reason == "tool_calls":
        conversation.append({"role": "assistant", "tool_calls": res.message.tool_calls})
        print("Function calls: ", res.message.tool_calls)
        for tool_call in res.message.tool_calls:
            tool_call_id = tool_call.id
            function_call = tool_call.function
            function_name = function_call.name
            arguments = json.loads(function_call.arguments)

            if function_name == "get_workdys":
                print(f"Function get_workdys called")
                call_result = get_workdays.get_workdys()
            elif function_name == "bing_web_search":
                print(f"Function bing_web_search called")
                search_query = arguments["search_query"]
                call_result = bing.bing_web_search(search_query)
                print("Get the search result from Bing Web Search API, and the first 50 characters are: ", call_result[:50])

            # add the function call to the memory
            conversation.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": function_name,
                    "content": call_result,
                }
            )
        print(conversation)
        second_response = aoai.call_llm_API(
            conversation, tool_list=None, tool_choice=None
        )
        return second_response
    else:
        print(f"Function not required, responding to user")
        # conversation.append(res.message)
        return response


if __name__ == "__main__":

    tools = [
        {
            "type": "function",
            "function": {
                "name": "bing_web_search",
                "description": "Search details for a  develop task using Bing Web Search API",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "The search query to use",
                        }
                    },
                    "required": ["search_query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_workdys",
                "description": "This is a function fetches holiday data from an external API and then categorizes each day as either a Working day or Non-working day",
            },
        },
    ]

    system_message = """You are a highly intelligent and efficient project management assistant specializing in cloud native development. Your task is to help break down a large project into manageable smaller tasks, estimate the completion time, and assign daily tasks based on the provided workdays.
    You can get workdays information by calling the `get_workdys` function from today in a month. 
    You can also use the `bing_web_search` function to search for details of a task.
    Let's Begin!"""

    pm_memory = memory.Memory()
    pm_memory.add_message("system", system_message)

    pm_memory.add_message("user", "What are the working days in the future?")
    response = agent_chat(pm_memory.conversation, tool_list=tools, tool_choice="auto")
    pm_memory.add_message("assistant", response.choices[0].message.content)

    pm_memory.add_message("user", TASK_DESCRIPTION+"Can you search the details and draft a work plan for me?")
    response = agent_chat(pm_memory.conversation, tool_list=tools, tool_choice="auto")
    pm_memory.add_message("assistant", response.choices[0].message.content)

    pm_memory.add_message(
        "user",
        "Now summarize all the past conversation and generate the final plan for me. You need to include the tasks breakdown, estimated time, and daily tasks assignment and their date. You don't need to assign tasks in non-working days. Make sure you have used working days information from get_workdays function in your plan.",
    )
    response = agent_chat(pm_memory.conversation, tool_list=tools, tool_choice="auto")
    pm_memory.add_message("assistant", response.choices[0].message.content)

    last_message = pm_memory.conversation[-1]["content"]

    reviewer_memory = memory.Memory()
    review_system_message = """You're a principal project manager who're good at reviewing a draft plan and provide feedback in cloud native development.
    In your feedback, you should list three sections: `Pros`, `Cons` and `Suggestions`
    Note: Don't recreate the plan by yourself, only provide comments.
    Let's Begin!"""

    reviewer_memory.add_message("system", review_system_message)
    reviewer_memory.add_message("user", f"Please review the following travel plan: {last_message}")
    response = agent_chat(reviewer_memory.conversation)
    reviewer_memory.add_message("assistant", response.choices[0].message.content)

    review_comment = reviewer_memory.conversation[-1]["content"]

    pm_memory.add_message("user", f"I have some comments to the plan, can you revise it accordingly? Comments:{review_comment}")
    response = agent_chat(pm_memory.conversation, tool_list=tools, tool_choice ="auto")
    pm_memory.add_message("assistant", response.choices[0].message.content)
    pm_memory.display_full_conversation()
