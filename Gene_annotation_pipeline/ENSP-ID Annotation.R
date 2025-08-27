
# set the working directory
setwd(" D:/ /")

# install biomart

if (!require("biomaRt")) install.packages("biomaRt")
library(biomaRt)


mart <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")


#Specify the files name, the gene col name should be ENSP-ID

files <- c("Betweenness.csv", "Degree.csv", "Closeness.csv","mcc.csv")

for (f in files) {
  df <- read.csv(f)
  
  mapping <- getBM(
    attributes = c("ensembl_peptide_id", "hgnc_symbol"),
    filters = "ensembl_peptide_id",
    values = df$ENSP.ID,
    mart = mart
  )
  
  df_annot <- merge(df, mapping, by.x = "ENSP.ID", by.y = "ensembl_peptide_id", all.x = TRUE)
  
  # Save annotated file
  outname <- sub(".csv", "_annotated.csv", f)
  write.csv(df_annot, outname, row.names = FALSE)
}
