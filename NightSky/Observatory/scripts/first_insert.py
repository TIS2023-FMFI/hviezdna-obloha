from pathlib import Path
from .insert import Insert


def insert_fits_in_folder(folder):
    insert = Insert(str(folder))
    del insert


def process_folders_with_fits(root_dir):
    root_path = Path(root_dir)
    for folder in root_path.rglob('*'):
        if folder.is_dir():
            insert_fits_in_folder(folder)
