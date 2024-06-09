import os


def get_in_directory_all(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def get_directories(directory):
    return [
        os.path.join(directory, name)
        for name in os.listdir(directory)
        if
        os.path.isdir(os.path.join(directory, name))
        and not name.startswith('.')
        and not name.startswith('_')
    ]


def read_file(file_path, can_be_none=False):
    try:
        with open(file_path, 'r') as file:
            current_content = file.read()
        return current_content
    except Exception as _e:
        if can_be_none:
            return ''
        else:
            raise _e


def write_file(file_path, result):
    with open(file_path, 'w', encoding='utf8') as output_file:
        output_file.write(result)


def get_and_rename_files(folder_path, old_file_name, new_file_name):
    """
    Recursively searches for files in a specified folder and renames them.

    :param folder_path: The path to the folder where the search should start.
    :param old_file_name: The current name of the files to be renamed.
    :param new_file_name: The new name for the files.
    """
    try:
        # Walk through the directory
        for dirpath, _, filenames in os.walk(folder_path):
            if old_file_name in filenames:
                old_file_path = os.path.join(dirpath, old_file_name)
                new_file_path = os.path.join(dirpath, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{old_file_path}' to '{new_file_path}'")

    except Exception as e:
        print(f"An error occurred: {e}")
