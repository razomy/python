import ast_lib


def test_get_method_names_from_directory_recursive():
    directory_path = "../"
    methods_in_project = ast_lib.get_method_names_from_directory_recursive(directory_path)
    for file, methods in methods_in_project.items():
        print(f"Methods in {file}:")
        for method in methods:
            print(f"  - {method}")
