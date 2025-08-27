import pandas as pd
import sys
import os

def load_file(file):
    """
    Load a file and return only the hgnc_symbol column,
    renamed to the file's base name.
    """
    try:
        df = pd.read_csv(file, sep=None, engine="python")  # auto-detect separator
    except Exception:
        df = pd.read_excel(file)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    if "hgnc_symbol" not in df.columns:
        raise ValueError(f"{file} must contain 'hgnc_symbol' column")

    # Rename column to filename (without extension)
    colname = os.path.splitext(os.path.basename(file))[0]
    return df[["hgnc_symbol"]].rename(columns={"hgnc_symbol": colname})


def main(files):
    dfs = []
    for file in files:
        print(f"Loading {file} ...")
        dfs.append(load_file(file))

    # Merge all on index (outer join keeps all rows, aligns by row index)
    merged = pd.concat(dfs, axis=1)

    merged.to_csv("merged_symbols.csv", index=False)
    print(f"✅ Merged {len(files)} files. Saved as merged_symbols.csv")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_common_genes_and_merge.py <file1> <file2> ...")
        sys.exit(1)
    main(sys.argv[1:])
