import os
import shutil

# Use the folder where the script is run as the source
source_dir = os.getcwd()
target_dir = os.path.join(source_dir, "organized")
os.makedirs(target_dir, exist_ok=True)

# Mapping rules for renaming
rename_map = {
    "matrix.mtx.gz": "matrix.mtx.gz",
    "barcodes.tsv.gz": "barcodes.tsv.gz",
    "features.tsv.gz": "features.tsv.gz"
}

# Loop through all files in the current folder
for fname in os.listdir(source_dir):
    if fname.endswith(".gz"):  # only process .gz files
        gsm_id = fname.split("_")[0]  
        
        # Create GSM subfolder inside organized/
        gsm_folder = os.path.join(target_dir, gsm_id)
        os.makedirs(gsm_folder, exist_ok=True)
        
        # Detect which type of file it is
        for key in rename_map:
            if fname.endswith(key):
                new_name = rename_map[key]
                break
        else:
            new_name = fname  # fallback: keep original if unmatched
        
        # Paths
        src_path = os.path.join(source_dir, fname)
        dest_path = os.path.join(gsm_folder, new_name)
        
        # Copy & rename
        shutil.copy(src_path, dest_path)  # use move() if you don’t want to keep originals
        print(f"Moved {fname} → {gsm_folder}/{new_name}")

print("All files organized and renamed inside:", target_dir)
