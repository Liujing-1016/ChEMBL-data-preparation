import rdkit
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, AllChem, Draw

import torch
from torch_geometric.data import Data
from torch.utils.data import Dataset, Subset
from torch_geometric.utils import to_networkx

from tqdm.notebook import tqdm
from tqdm import tqdm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

import argparse

parser = argparse.ArgumentParser(description="Convert SMILES dataset into PyTorch geometric Data.")
parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file.")
parser.add_argument("--output", type=str, default='graph_data.pt', help="Path to save the test CSV file.")
args = parser.parse_args()




def smi_to_pyg(smi, y=None):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
      return None

    node_features =[]
    hybridization_map = {'SP3': 0, 'SP2': 1, 'SP': 2}
    for atom in mol.GetAtoms():
        atomic_num = atom.GetAtomicNum()
        formal_charge = atom.GetFormalCharge()      
        hybridization = hybridization_map.get(str(atom.GetHybridization()),-1)
        atom_degree = atom.GetDegree()
        atom_imp = atom.GetNumImplicitHs()

        node_features.append([atomic_num, formal_charge, hybridization, atom_degree, atom_imp])
    node_features = torch.tensor(node_features, dtype=torch.float)

    edge_index = []
    edge_attr = []
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()  # 起始原子索引
        j = bond.GetEndAtomIdx()  # 结束原子索引
        bond_type = bond.GetBondTypeAsDouble()  # 键的类型（例如单键、双键等）
        is_conjugated = bond.GetIsConjugated()  # 是否共轭

        # 将边添加到边索引中
        edge_index.append([i, j])
        edge_index.append([j, i])
        edge_attr.append([bond_type, is_conjugated])
        edge_attr.append([bond_type, is_conjugated])
    
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)

    return Data(x=node_features, 
                edge_index=edge_index, 
                edge_attr=edge_attr, 
                y=torch.tensor([y], dtype=torch.float) if y is not None else None, 
                mol=mol, 
                smiles=smi)

class MyDataset(Dataset):
  def __init__(self, smiles, tasks):
    """
    smiles: list of SMILES 
    tasks: DataFrame containig task values
    
    """
    mols = [smi_to_pyg(smi, y=tasks.iloc[i].values) for i, smi in \
            tqdm(enumerate(smiles), total=len(smiles))]
    self.X = [m for m in mols if m]

  def __getitem__(self, idx):
    return self.X[idx]

  def __len__(self):
    return len(self.X)
  
  def __head__(self, n=5):
    return self.X[:n]

df = pd.read_csv(args.input)
data = MyDataset(df['smiles'], df.drop(columns='smiles'))
torch.save(data, args.output)
