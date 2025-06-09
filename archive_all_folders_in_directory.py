"""
Archive all folders in a specified directory.

This script takes a directory path as an argument and archives
each subfolder in the directory to a tar.zst file. The output
file is named after the folder and is placed in the same folder.

Example:

    $ python archive_all_folders_in_directory.py /path/to/folder

This script will create a tar.zst file for each subfolder in
/path/to/folder and place it in the same folder.

"""

import subprocess
import pathlib
import argparse

parser = argparse.ArgumentParser(
    description="Archive all folders in a specified directory."
)
parser.add_argument(
    "folder_path",
    type=pathlib.Path,
    help="Path to the folder containing subfolders to archive.",
)
args = parser.parse_args()

folder_path: pathlib.Path = args.folder_path
folders: list[pathlib.Path] = [path for path in folder_path.iterdir() if path.is_dir()]

for folder in folders:
    print(f"Packing folder: {folder.name}")
    with open(f"{str(folder)}.tar.zst", "wb") as output_file:
        with subprocess.Popen(
            ["tar", "cf", "-", "-C", str(folder_path), folder.name],
            stdout=subprocess.PIPE,
        ) as tar_process:
            with subprocess.Popen(
                ["pv"], stdin=tar_process.stdout, stdout=subprocess.PIPE
            ) as pv_process:
                subprocess.run(
                    ["pzstd"], stdin=pv_process.stdout, stdout=output_file, check=True
                )
    print(f"Packed {folder.name} successfully.")
print("All folders have been archived successfully.")
