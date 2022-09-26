"""
# Author: Dean-98543
# Time: 9/26/2022  16:38
# File: geneInfer.py
# Info: 
      1.
      2.
      3.
"""
from typing import List
import pickle
from chemCPA.model import ComPert
import torch
device = torch.device('cpu')

class geneInfer(object):

    def __init__(self, model_PATH, drug_sorted_PATH):
        state_dict, adversary_cov_state_dicts, cov_embeddings_state_dicts, model_config, history = torch.load(model_PATH)
        my_drug_embeddings = torch.nn.Embedding(
            num_embeddings=model_config['num_drugs'],  # 188
            embedding_dim=194
        )

        self.ae = ComPert(
            num_genes=model_config['num_genes'],    # 977
            num_drugs=model_config['num_drugs'],    # 188
            num_covariates=model_config['num_covariates'],  # [3]
            device=device,
            seed=model_config['seed'],  # 1337
            patience=model_config['patience'],  # 50
            doser_type=model_config['doser_type'],  # "amortized"
            decoder_activation=model_config['decoder_activation'],  # "ReLU"
            hparams=model_config['hparams'],    # dict(...)
            drug_embeddings=my_drug_embeddings,     # [188, 194]
            use_drugs_idx=model_config['use_drugs_idx'],    # true
            append_layer_width=None,
        )
        self.ae.load_state_dict(state_dict)

        self.cell2idx = {'A549': [1, 0, 0],
                    'K562': [0, 1, 0],
                    'MCF7': [0, 0, 1]}

        drugs_sorted = pickle.load(open(drug_sorted_PATH, 'rb'))
        self.drug2idx = {v:k for k,v in enumerate(drugs_sorted)}


    def predict(self, gene_expression:List[float], cell_type:str, drug_name:str, dose:float):
        assert (cell_type in self.cell2idx)
        assert (drug_name in self.drug2idx)
        assert (isinstance(dose, float))

        my_gene = torch.tensor([gene_expression, gene_expression])

        my_drug = torch.tensor([self.drug2idx[drug_name], self.drug2idx[drug_name]])

        my_dose = float(dose)
        my_dose = torch.tensor([my_dose, my_dose])

        my_cell = torch.tensor([self.cell2idx[cell_type],
                                self.cell2idx[cell_type]]).unsqueeze(0)

        y = self.ae.predict(
            genes=my_gene,
            drugs=None,
            drugs_idx=my_drug,
            dosages=my_dose,
            covariates=my_cell,
        )

        return y

ae = geneInfer(
    model_PATH="src/27b401db1845eea26c102fb614df9c33.pt",
    drug_sorted_PATH="src/drugs_names_unique_sorted.pkl"
)
