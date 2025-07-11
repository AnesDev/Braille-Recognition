import os
from label_tools import int_to_label123

v = [1, 2, 4, 8, 16, 32]


base_dir = "braille_characters"

# Loop through each folder (e.g., "0", "1", ..., "63")
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    if not os.path.isdir(folder_path):
        continue

    try:
        new_folder_name = int_to_label123(folder)
    except:
        print(f"Skipping folder {folder} (not an int?)")
        continue

    # Rename all images inside the folder
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        # Example: 11_5.jpg → get "5"
        parts = filename.split('_')
        if len(parts) != 2 or not parts[1].split('.')[0].isdigit():
            print(f"Skipping invalid file name: {filename}")
            continue

        index = parts[1]
        new_filename = f"{new_folder_name}_{index}"
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_filename)
        os.rename(src, dst)

    # Rename the folder itself
    new_folder_path = os.path.join(base_dir, new_folder_name)
    if new_folder_path != folder_path:
        os.rename(folder_path, new_folder_path)
        print(f"✅ Renamed folder {folder} → {new_folder_name}")
