import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        target_file_is_dir = os.path.isdir(target_file_path)
        
        if not valid_target_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'    
            
        elif target_file_is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
            
        else:
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            
            with open(target_file_path, "w") as f:
                f.write(content)
            
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'          
    
    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text content to a file at the given path, relative to the working directory. Creates the file, and any missing parent directories, if they don't exist. If the file already exists, its contents are completely overwritten. Returns an error message if the path points to a directory or falls outside the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The full text to write to the file. This replaces any existing contents.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}