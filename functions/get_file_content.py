import config
import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:    
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        target_file_path_is_file = os.path.isfile(target_file_path)
        
        if not valid_target_file_path :           
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            
        elif not target_file_path_is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        else:
            MAX_CHARS = config.MAX_CHARS
            
            f = open(target_file_path)
            content = f.read(MAX_CHARS)
            
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
            return content
                
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file at the given path, relative to the working directory. Returns the file's text, truncated with a notice if it exceeds the maximum character limit. Returns an error message if the file doesn't exist or is outside the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}