import pandas as pd
import itertools
import os

def find_common_genes(input_dir=".", col_name="hgnc_symbol", output="common_genes_summary.csv"):
    gene_sets = {}

    # Read all CSV files in the directory
    files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    if not files:
        print("No CSV files found in the directory.")
        return

    for file in files:
        path = os.path.join(input_dir, file)
        df = pd.read_csv(path, sep=None, engine="python")  # auto-detect delimiter
        df.columns = df.columns.str.strip()  # clean spaces
        if col_name not in df.columns:
            print(f"⚠️ Column '{col_name}' not found in {file}. Skipping...")
            continue
        gene_sets[file] = set(df[col_name].dropna().astype(str).str.strip())

    results = []

    # Common genes across ALL files
    if len(gene_sets) > 1:
        all_common = set.intersection(*gene_sets.values())
        results.append({
            "Comparison": f"Common across ALL {len(gene_sets)} files",
            "Gene_Count": len(all_common),
            "Genes": ", ".join(sorted(all_common))
        })

    # Common genes across combinations (2, 3, …, n-1)
    for r in range(2, len(gene_sets)):
        for combo in itertools.combinations(gene_sets.keys(), r):
            common_genes = set.intersection(*(gene_sets[f] for f in combo))
            results.append({
                "Comparison": f"Common in {r} files: {', '.join(os.path.basename(f) for f in combo)}",
                "Gene_Count": len(common_genes),
                "Genes": ", ".join(sorted(common_genes))
            })

    # Save to CSV
    result_df = pd.DataFrame(results)
    result_df.to_csv(output, index=False)
    print(f"Common gene summary saved to {output}")


if __name__ == "__main__":
    # Run directly in current directory
    find_common_genes(".")
