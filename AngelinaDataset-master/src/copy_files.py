import os
import shutil
from pathlib import Path

BASE_DIR = Path("braille_characters")
TOTAL_DIR = BASE_DIR / "total"
TOTAL_DIR.mkdir(exist_ok=True)

count = 0

for label_folder in BASE_DIR.iterdir():
    if not label_folder.is_dir():
        continue
    if label_folder.name == "total":
        continue


    for img_file in label_folder.glob("*.jpg"):
        dest = TOTAL_DIR / img_file.name
        shutil.copy(img_file, dest)
        count += 1

print(f"Copied {count} images into {TOTAL_DIR}")
