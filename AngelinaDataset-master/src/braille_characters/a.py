# v = [1, 2, 4, 8, 16, 32]

# def int_to_label123(int_lbl):
#     int_lbl = int(int_lbl)
#     r = ""
#     for i in range(6):
#         if int_lbl & v[i]:
#             r += str(i + 1)
#     return r

# all_possible = [int_to_label123(i) for i in range(1, 64)]

# # Sort by length, then lexicographically
# all_possible.sort(key=lambda x: (len(x), x))

# print("All 63 expected labels:")
# for lbl in all_possible:
#     print(lbl)

# print(f"\nTotal = {len(all_possible)}")





# from pathlib import Path

# # Current directory
# base_path = Path(".")

# # List all folders in the same directory as this script
# folders = [f.name for f in base_path.iterdir() if f.is_dir()]

# # Sort the list
# folders.sort()

# # Print the folder names
# print("Folders found:")
# for folder in folders:
#     print(folder)

# print(f"\nTotal folders: {len(folders)}")




from pathlib import Path

v = [1, 2, 4, 8, 16, 32]

def int_to_label123(int_lbl):
    r = ""
    for i in range(6):
        if int_lbl & v[i]:
            r += str(i + 1)
    return r

# Generate expected labels (from 1 to 63)
expected = set(int_to_label123(i) for i in range(1, 64))

# Read actual folder names in current directory
base_path = Path(".")
actual = set(f.name for f in base_path.iterdir() if f.is_dir())

# Find the missing ones
missing = expected - actual
extra = actual - expected

print("🚫 Missing folders:")
for m in sorted(missing):
    print(m)

print("\n❓ Unexpected (extra) folders:")
for e in sorted(extra):
    print(e)

print(f"\n✅ Total expected: {len(expected)}")
print(f"📂 Total actual  : {len(actual)}")
print(f"❌ Total missing : {len(missing)}")


