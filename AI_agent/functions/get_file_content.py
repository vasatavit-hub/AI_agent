import os
from .config import *

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the file in the specified file path, constrained to the working directory. Returns up to 10 000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to return content from, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        if not os.path.abspath(os.path.join(working_directory, file_path)).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
        f_path = os.path.join(working_directory, file_path)
        if not os.path.isfile(f_path):
            return f'Error: "{file_path}" is not a file'

        with open(f_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(f.read())>MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters].'
            return file_content_string



    except Exception as e:
        return f"Error: {e}"