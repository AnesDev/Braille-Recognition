from pathlib import Path
import PIL.Image
import data
import shutil

v = [1, 2, 4, 8, 16, 32]

def int_to_label123(int_lbl):
    int_lbl = int(int_lbl)
    r = ""
    for i in range(6):
        if int_lbl & v[i]:
            r += str(i + 1)
    return r

# Root folders to search for data
search_dirs = [
    Path("../books"),
    Path("../handwritten"),
    Path("../uploaded")
]

# Output dir for cropped braille characters
output_dir = Path("braille_characters")

# Delete existing output folders
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(parents=True)

# Counter for image naming
label_counters = {}

def process_annotation(csv_file):
    ann = data.read_csv_annotation(csv_file)
    img_file = csv_file.with_suffix(".jpg")

    if not img_file.exists():
        print(f"Image not found for {csv_file}")
        return

    img = PIL.Image.open(img_file)
    width, height = img.size

    for left, top, right, bottom, label in ann:
        # Convert label to actual braille class like "124"
        braille_label = int_to_label123(label)

        # Convert normalized to pixel coordinates
        x1 = int(left * width)
        y1 = int(top * height)
        x2 = int(right * width)
        y2 = int(bottom * height)

        # Crop
        cropped = img.crop((x1, y1, x2, y2))

        # Create folder
        label_folder = output_dir / braille_label
        label_folder.mkdir(parents=True, exist_ok=True)

        # Increment counter
        label_counters[braille_label] = label_counters.get(braille_label, 0) + 1
        idx = label_counters[braille_label]

        # Save with new name
        save_path = label_folder / f"{braille_label}_{idx}.jpg"
        cropped.save(save_path)

        print(f"Saved {save_path}")

if __name__ == "__main__":
    for base_dir in search_dirs:
        for csv_file in base_dir.glob("**/*.csv"):
            print(f"Processing: {csv_file}")
            process_annotation(csv_file)
