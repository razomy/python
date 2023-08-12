import os
import git


def last_commit_versions(repo_root, file_path):
    repo = git.Repo(path=repo_root)
    rel_file_path = str(os.path.relpath(file_path, repo_root))
    last_commit = repo.head.commit
    last_commit_content = last_commit.tree[rel_file_path].data_stream.read().decode("utf-8")
    return last_commit_content
