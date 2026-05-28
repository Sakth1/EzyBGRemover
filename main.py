import sys
from pathlib import Path
from PIL import Image
from rembg import remove

def validate_file_exist(file_path: Path):
    if file_path.exists() is True:
        print("File or the folder exist")
    else:
        print("File or the folder not exist")

def validate_path_is_folder(file_path: Path):
    if file_path.is_dir() is True:
        return True
    else:
        return False

def validate_file_image(file_path: Path):
    if file_path.is_file() is True and file_path.suffix == ".jpg" or file_path.suffix == ".png":
        return True
    else:
        return False
    
def remove_bg_and_save(file_path:Path, new_folder_path:Path=None):
    image_file = Image.open(file_path)
    img = remove(image_file)
    if new_folder_path is None:
        fp = file_path.name[:-4] + "_no_bg.png"
        img.save(fp)
        print(f"File saved at {Path(fp).resolve()}")
    else:
        fp = Path(str(new_folder_path) + "/" + str(file_path.name[:-4] + "_no_bg.png"))
        img.save(fp)
        print(f"File saved at {Path(fp).resolve()}")

def remove_bg_and_save_folder(file_path: Path, previous_folder_path: Path = None):
    if previous_folder_path is None:
        new_folder_path = Path(str(file_path) + "_no_bg")
        new_folder_path.mkdir(exist_ok=True)
    else:
        new_folder_path = Path(str(previous_folder_path) + "_no_bg")
        new_folder_path.mkdir(exist_ok=True)

    for file in file_path.iterdir():
        if validate_file_image(file) is True:
            remove_bg_and_save(file_path=file, new_folder_path=new_folder_path)
            print(f"Removed background from {file.name}")
        else:
            if validate_path_is_folder(file) is True:
                print("Found another folder: ", file.name)
                remove_bg_and_save_folder(file, Path(str(new_folder_path) + "/" + file.name))
            print(f"File {file.name} is not image")


def main():
    print(sys.argv)
    file: str = sys.argv[1]
    file_path: Path = Path(file).resolve()
    if validate_file_exist(file_path) is False:
        return

    if validate_file_image(file_path) is True:
        remove_bg_and_save(file_path)

    elif validate_path_is_folder(file_path) is True:
        print("Searching for image file")
        remove_bg_and_save_folder(file_path)

    else:
        print("File is not image or a folder having image")
        return

if __name__ == "__main__":
    main()
