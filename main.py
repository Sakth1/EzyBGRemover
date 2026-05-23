import time
import sys
from pathlib import Path
from PIL import Image
from rembg import remove

def validate_file_exist(file_path: Path):
    if file_path.exists() is True:
        print("File or the folder exist")
        time.sleep(3)
    else:
        print("File or the folder not exist")
        time.sleep(3)

def validate_file_image(file_path: Path):
    if file_path.is_dir():
        pass
    elif file_path.is_file() and file_path.suffix == ".jpg" or file_path.suffix == ".png":
        print("File is image")
        time.sleep(3)
    else:
        print("File is not image")
        time.sleep(3)


def main():
    print(sys.argv)
    file: str = sys.argv[1]
    file_path = Path(file).resolve()
    validate_file_exist(file_path)
    validate_file_image(file_path)

    image_file = Image.open(file_path)
    img = remove(image_file)
    fp = file_path.name[:-4] + "_no_bg.png"
    img.save(fp)
    print(f"File saved at {Path(fp).resolve()}")

if __name__ == "__main__":
    main()
