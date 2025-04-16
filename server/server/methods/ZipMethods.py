import os
import shutil
import tempfile
import uuid
import zipfile
from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from server.configs.dropbox.config import get_dropbox_service
from server.models import FileModel, RepositoryModel, DirectoryModel
from server.utils.ResponseBody import ResponseBody


def fetch_repo(user: str, repo_name: str) -> dict:
    try:
        repo = RepositoryModel.objects.get(name=repo_name, owner=user)
    except RepositoryModel.DoesNotExist:
        return {"message": "Repository not found", "status": 404}

    # Get all directories and files associated with the repository
    directories = DirectoryModel.objects.filter(repo=repo).select_related("parent_dir")
    files = FileModel.objects.filter(repo=repo).select_related("directory")

    # Initialize data structures
    dir_map = {}  # Maps directory IDs to directory data
    root_dirs = []  # Top-level directories (no parent)
    root_files = []  # Files in the root directory (no parent directory)

    # First pass: create all directory entries
    for directory in directories:
        dir_data = {
            "dirID": directory.dirID,
            "dirName": directory.dirName,
            "files": [],
            "subdirectories": [],
        }
        dir_map[directory.dirID] = dir_data

        if directory.parent_dir is None:
            root_dirs.append(dir_data)

    # Second pass: build the hierarchy
    for directory in directories:
        if directory.parent_dir and directory.parent_dir.dirID in dir_map:
            parent_data = dir_map[directory.parent_dir.dirID]
            parent_data["subdirectories"].append(dir_map[directory.dirID])

    # Third pass: organize files
    for file in files:
        file_data = {
            "fileID": file.fileID,
            "fileName": file.fileName,
            "filePath": file.filePath if hasattr(file, "filePath") else None,
        }
        if file.directory:
            if file.directory.dirID in dir_map:
                dir_map[file.directory.dirID]["files"].append(file_data)
        else:
            root_files.append(file_data)

    # Prepare the final response
    response_data = {
        "repoID": repo.repoID,
        "repoName": repo.name,
        "owner": repo.owner.username if hasattr(repo.owner, "username") else repo.owner,
        "structure": {"rootFiles": root_files, "directories": root_dirs},
        "status": 200,
    }

    return response_data


def insert_repo_details(zip_file: zipfile.ZipFile, user: str, repo_name: str) -> dict:
    if not zip_file or not user:
        return Response({"message": "No zip or username file found"}, status=400)

    # Create temporary directory and extract zip
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_file.file, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # Create repository
    repo = RepositoryModel.objects.create(name=repo_name, owner=user)

    # Dictionary to track created directories and their models
    created_dirs = {}
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            path = os.path.join(root, file)  # full path
            rel_file_path = os.path.relpath(
                path, start=temp_dir
            )  # relative part to temp dir
            parent_dir = os.path.dirname(rel_file_path)  # parent dir of current file

            path_part = (
                parent_dir.split(os.sep) if parent_dir else []
            )  # dirs and subdirs
            current_path = ""
            parent_dir_model = None

            for part in path_part:
                current_path = os.path.join(current_path, part)
                if current_path not in created_dirs:
                    parent_dir_model = DirectoryModel.objects.create(
                        dirName=part, repo=repo, parent_dir=parent_dir_model
                    )
                    created_dirs[current_path] = parent_dir_model
                else:
                    parent_dir_model = created_dirs[current_path]

            FileModel.objects.create(
                fileName=file, directory=parent_dir_model, repo=repo
            )

    return {"message": "Repo created successfully", "status": 201}


def get_file_content(file_path: str) -> ResponseBody:
    dbx = get_dropbox_service()
    try:
        metadata, res = dbx.files_download(file_path)
        if res.status_code != 200:
            return ResponseBody.build(
                {"message": "Failed to download file"}, status=res.status_code
            )
        file_name = metadata.name
        content = res.content.decode("utf-8")
        print(f"File metadata: {metadata}")
        print(f"File content: {content}")
        return ResponseBody.build(
            {"message": {"file_name": file_name, "content": content}}, status=200
        )
    except Exception as e:
        print(f"Error: {e}")
        return None
