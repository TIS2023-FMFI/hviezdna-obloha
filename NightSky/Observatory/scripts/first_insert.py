from pathlib import Path
from .insert import Insert


def insert_fits_in_folder(folder):
    insert = Insert(str(folder))
    count = insert.get_number_of_inserted_rows()
    del insert

    return count


def process_folders_with_fits(root_dir):
    count = insert_fits_in_folder(root_dir)
    root_path = Path(root_dir)

    for folder in root_path.rglob("*"):
        if folder.is_dir():
            count += insert_fits_in_folder(folder)

    return count
