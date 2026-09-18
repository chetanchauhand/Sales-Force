# Student Marks Analyzer

import os
import shutil

folder = input("Enter folder path: ")

if not os.path.exists(folder):
    print("Folder does not exist.")
    exit()

file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Programs": [".py", ".java", ".cpp", ".c"]
}

for file in os.listdir(folder):

    file_path = os.path.join(folder, file)

    if os.path.isfile(file_path):

        extension = os.path.splitext(file)[1].lower()

        moved = False

        for folder_name, extensions in file_types.items():

            if extension in extensions:

                new_folder = os.path.join(folder, folder_name)

                os.makedirs(new_folder, exist_ok=True)

                shutil.move(
                    file_path,
                    os.path.join(new_folder, file)
                )

                print(file, "→", folder_name)

                moved = True
                break

        if not moved:
            print(file, "→ Other")

print("\nFiles organized successfully!")