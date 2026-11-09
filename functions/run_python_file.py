import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try:    
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        target_file_is_file = os.path.isfile(target_file_path)
        
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not target_file_is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if os.path.splitext(target_file_path)[1] != '.py':
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        
        if args is not None:
            command.extend(args)
            
        completed_process = subprocess.run(args = command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        
        output_parts = []
        
        if completed_process.returncode != 0:
            output_parts.append(f'Process exited with code {completed_process.returncode}')
        
        if not (completed_process.stderr or completed_process.stdout):
            output_parts.append(f'No output produced')
        
        else:
            if completed_process.stdout:
                output_parts.append(f'STDOUT: {completed_process.stdout}')
            
            if completed_process.stderr:
                output_parts.append(f'STDERR: {completed_process.stderr}')

        final_output = "\n".join(output_parts)
        return final_output
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file located relative to the working directory, using the working directory as the current directory, and returns its output. The result includes STDOUT and STDERR, plus the exit code if the script fails. Execution is stopped after 30 seconds. Returns an error message if the file doesn't exist, isn't a .py file or is outside the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of command-line arguments to pass to the script, each as a separate string (for example, ['3 + 5'])",
                },
            },
            "required": ["file_path"],
        },
    },
}