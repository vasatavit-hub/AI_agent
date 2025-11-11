import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrite the contents of the file in the specified file path, constrained to the working directory. If the file path does not exist, it will create all missing parents directories and the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file specified by the file path.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        if not os.path.abspath(os.path.join(working_directory, file_path)).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        path = "/".join(file_path.split("/")[:-1])
        r_path = os.path.join(working_directory,path)
        #if not os.path.exists(os.path.join(working_directory, path)):
         #   print("xx")
        if path != "":
            os.makedirs(os.path.join(working_directory,path), mode=0o777, exist_ok=True)
        with open(os.path.join(working_directory,file_path), "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"