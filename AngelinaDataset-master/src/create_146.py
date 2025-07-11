import cv2
import os
from pathlib import Path

# Set base folder
base_folder = Path("braille_characters")

# Define input and output folders
input_folder = base_folder / "134"
output_folder = base_folder / "146"
output_folder.mkdir(parents=True, exist_ok=True)

# Process all .jpg images in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".jpg"):
        img_path = input_folder / filename
        img = cv2.imread(str(img_path))

        if img is None:
            print(f" Could not read: {img_path}")
            continue

        # Horizontal flip
        flipped = cv2.flip(img, 1)

        # Generate new filename by replacing prefix
        new_filename = filename.replace("134_", "146_")

        # Save flipped image
        out_path = output_folder / new_filename
        cv2.imwrite(str(out_path), flipped)
        print(f"Saved: {out_path}")

print("\nFlipping complete. Images renamed and saved to 146.")
