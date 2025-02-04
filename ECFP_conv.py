import argparse
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

def smiles_to_ecfp(smiles, radius=2, n_bits=1024):
    """Convert SMILES to ECFP fingerprint"""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(n_bits)  # Handle invalid SMILES
    return np.array(AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits))

def process_file(input_file, output_file, chunk_size=10000):
    """Process input CSV in chunks and generate ECFP features"""
    print(f"Processing {input_file}...")
    reader = pd.read_csv(input_file, chunksize=chunk_size)
    
    first_chunk = True  # Track first chunk for header writing
    for chunk in reader:
        print(f"Processing chunk with {len(chunk)} rows...")
        
        ecfp_features = np.array([smiles_to_ecfp(sm) for sm in chunk["smiles"]])
        df_ecfp = pd.DataFrame(ecfp_features)
        
        df_ecfp.to_csv(output_file, mode='a', index=False, header=first_chunk)
        first_chunk = False  # Only write header for the first chunk
    
    print(f"Saved {output_file} ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input CSV file containing SMILES")
    parser.add_argument("--output", type=str, required=True, help="Output CSV file for ECFP features")
    args = parser.parse_args()
    
    process_file(args.input, args.output)
