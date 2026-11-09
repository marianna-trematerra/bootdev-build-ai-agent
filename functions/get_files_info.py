import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: {directory} is not a directory'


        temp_list = []
        
        for file in os.listdir(target_dir):
            
            file_path = os.path.join(target_dir, file)
            file_name = file
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            
            temp_list.append(f'- {file_name}: file_size={file_size} bytes, is_dir={is_dir}')
            
        separator = '\n'    
        return(separator.join(temp_list))
    
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}