import os

def delete_empty_folders(path):
    """
    Recursively delete empty folders starting from the given path.
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"Deleted empty folder: {folder_path}")

if __name__ == '__main__':
    path = "PATH"
    delete_empty_folders(path)
