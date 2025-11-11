import os
from dotenv import load_dotenv

from google import genai
import sys
from google.genai import types

from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *




available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
if len(sys.argv)==1:
    print("prompt not provided")
    sys.exit(1)
x_args = sys.argv[1:]
natural = [a for a in x_args if not a.startswith("-")]
user_prompt = " ".join(natural)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Please, dont ask question.
If arguments are not provided, make function call without them.
If path is not provided, list files and directories to get the path. 
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

When providing your final answer, give a clear, concise explanation.
Do NOT include raw tool outputs or function results in your final response.
Summarize what you learned from the tools in natural language.
"""

def function_arguments (**some_args):
    return some_args

def return_result (function_name, function_result):
    return types.Content(
    role="user",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)

def call_function (function_call_part, verbose = False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_args = function_arguments(**function_call_part.args)
    function_args["working_directory"] = "./calculator"
    

    match (function_name):
        case ("get_files_info"):
            function_result = get_files_info(**function_args)
            return return_result(function_name,function_result)

        case ("get_file_content"):
            function_result = get_file_content(**function_args)
            return return_result(function_name,function_result)           

        case ("run_python_file"):
            function_result = run_python_file(**function_args)
            return return_result(function_name,function_result)            
        
        case ("write_file"):
            function_result = write_file(**function_args)
            return return_result(function_name,function_result)            
        
        case _:
            return types.Content(
            role="user",
            parts=[
            types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

for i in range (0,20):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config = types.GenerateContentConfig(
            system_instruction = system_prompt,
            tools = [available_functions],
            )
        )

    for reply in response.candidates:
        messages.append(reply.content)
        

    verbose = False
    if "--verbose" in sys.argv or "-v" in sys.argv:
        verbose = True

    if isinstance(response.function_calls,list):
        response_text = ""
        for function_call_part in response.function_calls:
            call_response = call_function (function_call_part, verbose)
            try:
                messages.append(call_response)
            except Exception:
                raise Exception ("Fatal exception of some sort")
    else:
        print (f"FINAL RESPONSE: {response.text}")
        break
    



def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
