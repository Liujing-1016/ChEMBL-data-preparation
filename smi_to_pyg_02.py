from rdkit import Chem
from rdkit.Chem import AllChem, Draw

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


atom_symbols = ['B', 'C', 'N', 'O', 'F', 'Si', 'P', 'S', 'Cl', 'As', 
                    'Se', 'Br', 'Te', 'I', 'At', 'metal']
hybridization_types = ['SP', 'SP2', 'SP3', 'SP3D', 'SP3D2', 'other']
chirality_types = ['R', 'S']
bond_types = ['SINGLE', 'DOUBLE', 'TRIPLE', 'AROMATIC']
stereo_types = ['STEREONONE', 'STEREOANY', 'STEREOZ', 'STEREOE']

def get_atom_features(atom):

    """获取原子的 one-hot 特征"""
    # Atom symbol (one-hot)
    atom_symbol_one_hot = [1 if atom.GetSymbol() == sym else 0 for sym in atom_symbols]
    
    # Degree (number of covalent bonds, one-hot for [0-5])
    degree_one_hot = [1 if atom.GetDegree() == i else 0 for i in range(6)]
    
    # Formal charge (integer, directly used)
    formal_charge = atom.GetFormalCharge()
    
    # Radical electrons (integer, directly used)
    radical_electrons = atom.GetNumRadicalElectrons()
    
    # Hybridization (one-hot)
    hybridization = str(atom.GetHybridization())
    hybridization_one_hot = [1 if hybridization.upper() == h else 0 for h in hybridization_types]
    
    # Aromaticity (one-hot)
    aromaticity = [1 if atom.GetIsAromatic() else 0]
    
    # Hydrogens (number of connected hydrogens, one-hot for [0-4])
    hydrogens_one_hot = [1 if atom.GetTotalNumHs() == i else 0 for i in range(5)]
    
    # Chirality (is chiral or not, one-hot)
    chirality = [1 if atom.GetChiralTag() != Chem.rdchem.ChiralType.CHI_UNSPECIFIED else 0]
    
    # Chirality type (R/S, one-hot)
    # 检查属性是否存在，避免异常
    if atom.HasProp('_CIPCode'):
        chirality_value = atom.GetProp('_CIPCode')
    else:
        chirality_value = ''

    chirality_type = [1 if chirality_value == c else 0 for c in chirality_types]

    
    # Combine all features
    atom_feature = atom_symbol_one_hot + degree_one_hot + [formal_charge] + [radical_electrons] + \
                   hybridization_one_hot + aromaticity + hydrogens_one_hot + chirality + chirality_type
    
    return atom_feature






def smi_to_pyg(smi, y=None):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None

    node_features = []

    node_features = [get_atom_features(atom) for atom in mol.GetAtoms()]
    node_features = torch.tensor(node_features, dtype=torch.float)

    # 构建边特征（键特征）
    bond_types = [1.0, 1.5, 2.0, 3.0]  # 单键、芳香键、双键、三键
    stereo_types = ['STEREONONE', 'STEREOZ', 'STEREOE']  # 键的立体化学
    edge_index = []
    edge_attr = []
    for bond in mol.GetBonds():
        i = bond.GetBeginAtomIdx()  # 起始原子索引
        j = bond.GetEndAtomIdx()  # 结束原子索引

        bond_type_one_hot = [1 if bond.GetBondTypeAsDouble() == bt else 0 for bt in bond_types]
        is_conjugated_one_hot = [1 if bond.GetIsConjugated() else 0]
        is_in_ring_one_hot = [1 if bond.IsInRing() else 0]
        stereo_one_hot = [1 if str(bond.GetStereo()) == s else 0 for s in stereo_types]

        bond_features = bond_type_one_hot + is_conjugated_one_hot + is_in_ring_one_hot + stereo_one_hot

        # 添加双向边
        edge_index.append([i, j])
        edge_index.append([j, i])
        edge_attr.append(bond_features)
        edge_attr.append(bond_features)

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_attr, dtype=torch.float)

    return Data(
        x=node_features, 
        edge_index=edge_index, 
        edge_attr=edge_attr, 
        y=torch.tensor([y], dtype=torch.float) if y is not None else None, 
        mol=mol, 
        smiles=smi
    )

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
