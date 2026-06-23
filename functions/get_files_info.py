import os


def get_files_info(working_directory: str, directory: str):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))
    is_valid_dir = (
        os.path.commonpath([abs_working_directory, target_dir]) == abs_working_directory
    )
    try:
        if not is_valid_dir:
            print(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )
            return
        if not os.path.isdir(target_dir):
            print(f'Error: "{directory}" is not a directory')
            return
        else:
            print(f'Success: "{directory}" is within the working directory')
            return

    except Exception as e:
        print(f"Error: {e}")
        return
