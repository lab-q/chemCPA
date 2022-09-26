"""
# Author: Dean-98543
# Time: 9/26/2022  16:39
# File: main.py
# Info: 
      1.
      2.
      3.
"""
from typing import List
import scanpy as sc
from geneInfer import ae

data_PATH = "src/sciplex_complete_middle_subset_lincs_genes.h5ad"
adata = sc.read(data_PATH)
gene_idx = 0


gene_expr = adata.to_df().iloc[gene_idx].to_list()
drug_name = adata.obs.iloc[gene_idx]['product_name']
dose = float(adata.obs.iloc[gene_idx]['dose'])
cell_type = adata.obs.iloc[gene_idx]['cell_type']

y = ae.predict(
    gene_expression=gene_expr,
    drug_name=drug_name,
    cell_type=cell_type,
    dose=dose
)
print(y)