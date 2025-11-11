import os
import subprocess
import sys

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run the file from, relative to the working directory. ",
            ),
            "arguments": types.Schema(
                type=types.Type.STRING,
                description="The arguments to run the file with. If not provided, will be run with args=[]",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try:
        if not os.path.abspath(os.path.join(working_directory, file_path)).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(os.path.abspath(os.path.join(working_directory, file_path))):
            return f'Error: File "{file_path}" not found.'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        cmd = [sys.executable,os.path.abspath(os.path.join(working_directory, file_path))] + args
        completed_process = subprocess.run (
            cmd,
            capture_output = True,
            text = True,
            timeout = 30,

        )
        STDOUT = f"STDOUT: {completed_process.stdout}"
        STDERR = f"STDERR: {completed_process.stderr}"
        EXIT_CODE = ""
        if completed_process.returncode !="0":
            EXIT_CODE = f"Process exited with code {completed_process.returncode}"
        OUTPUT = "No output produced"
        if completed_process.stdout != "" or completed_process.stderr !="" or completed_process.returncode !="":
            OUTPUT = STDOUT + "\n" + STDERR + "\n" + EXIT_CODE

        return OUTPUT
        
        
    except Exception as e:
        return f"Error: executing Python file: {e}"  
    