"""Semantic Kernel Demo - Main File
"""

# # from services import Service
# import asyncio
import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
# from semantic_kernel.prompt_template.input_variable import InputVariable
# from semantic_kernel.contents.chat_history import ChatHistory
# from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

# # selectedService = Service.OpenAI
# kernel = sk.Kernel()

api_key, org_id = sk.openai_settings_from_dot_env()
# service_id = "oai_chat_gpt"
# kernel.add_service(
#     OpenAIChatCompletion(
#         service_id=service_id,
#         ai_model_id="gpt-3.5-turbo-1106",
#         api_key=api_key,
#         org_id=org_id,
#     )
# )

# execution_settings = sk_oai.OpenAIChatPromptExecutionSettings(
#     service_id=service_id,
#     ai_model_id="gpt-3.5-turbo-1106",
#     max_tokens=2000,
#     temperature=0.7,
# )

# prompt = """
# ChatBot can have a conversation with you about any topic.
# It can give explicit instructions or say 'I don't know' if it does not have an answer.

# {{$history}}
# User: {{$user_input}}
# ChatBot: """

# prompt_template_config = sk.PromptTemplateConfig(
#     template=prompt,
#     name="chat",
#     template_format="semantic-kernel",
#     input_variables=[
#         InputVariable(name="input", description="The user input", is_required=True),
#         InputVariable(name="history", description="The conversation history", is_required=True),
#     ],
#     execution_settings=execution_settings,
# )

# chat_function = kernel.create_function_from_prompt(
#     function_name="chat",
#     plugin_name="chatPlugin",
#     prompt_template_config=prompt_template_config,
# )

# chat_history = ChatHistory()
# chat_history.add_system_message("You are a helpful chatbot who is good about giving book recommendations.")

# async def chat() -> None:
#     # Save new message in the context variables
#     input_text = input("Your Message: ")
#     print(f"User: {input_text}")
#     chat_history.add_user_message(input_text)

#     # Process the user message and get an answer
#     answer = await kernel.invoke(chat_function, KernelArguments(user_input=input_text, history=chat_history))
#     print(f"ChatBot: {answer}")
#     chat_history.add_assistant_message(str(answer))

# if __name__ == "__main__":
#     while True:
#         asyncio.run(chat())


import asyncio
import os

import semantic_kernel as sk
from semantic_kernel.planners.basic_planner import BasicPlanner


async def main():
    # Initialize the kernel
    kernel = sk.Kernel()

    # Add the service to the kernel
    # use_chat: True to use chat completion, False to use text completion
    kernel.add_service(OpenAIChatCompletion(service_id="oai_chat_gpt", ai_model_id="gpt-3.5-turbo-1106", api_key=api_key, org_id=org_id))

    script_directory = os.path.dirname(__file__)
    plugins_directory = os.path.join(script_directory, "plugins")
    kernel.import_native_plugin_from_directory(plugins_directory, "EmailGen")
    kernel.import_plugin_from_prompt_directory("plugins", "Email")

    planner = BasicPlanner(
        service_id="default"
    )

    goal = "Write an email to the marketing team to join the meeting that just started"  # noqa: E501

    # Create a plan
    plan = await planner.create_plan(goal, kernel)

    # Execute the plan
    result = await kernel.invoke(plan)

    print(f"The goal: {goal}")
    print(f"Plan results: {result}")


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
