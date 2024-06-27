import ast
import os


def get_method_names_from_path(file_path: str):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    methods = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            methods.append(node.name)

        if isinstance(node, ast.ClassDef):
            methods.append(node.name)

    return methods


def get_method_names_from_directory_recursive(directory_path: str):
    all_methods = {}

    for root, _, files in os.walk(directory_path):
        for file in files:
            if not file.endswith(".py"):
                continue

            file_path = str(os.path.join(root, file))
            relative_path = os.path.relpath(file_path, directory_path)

            methods = get_method_names_from_path(file_path)
            if not methods:
                continue

            all_methods[relative_path] = methods

    return all_methods
