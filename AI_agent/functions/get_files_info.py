import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        if not os.path.abspath(os.path.join(working_directory, directory)).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        dir_path = os.path.join(working_directory, directory)
        if not os.path.isdir(dir_path):
            return f'Error: "{directory}" is not a directory'

        contents = os.listdir(dir_path)
        contents_info = ""
        for content in contents:
            c_path = os.path.join(dir_path, content)
            contents_info += f"{content}: file_size= {os.path.getsize(c_path)} bytes, is_dir={os.path.isdir(c_path)} \n"
        contents_info = contents_info[:-1]
        return contents_info
    except Exception as e:
        return f"Error: {e}"