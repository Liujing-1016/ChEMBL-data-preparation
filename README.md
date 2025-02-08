# ChEMBL Data Preparation

## data_extraction.py
```bash
python data_extraction.py --dp_path=
```
This script extracts data and generates the `pIC50_ChEMBL.csv` file in the current directory by default.

## data_conversion.py
```bash
python data_conversion.py --file='/home/jovyan/proj-liujing/random/testset.csv'
```
This script converts the specified file into a matrix format. The required file should be specified using `--file=`.

The default generated output file is `chembl_matrix.csv`, and the filename will not be overwritten. A corresponding `target dictionary` is also created.

A test dataset is available as `test_extracted_chembl.csv`.

## data_split.py
This script splits the preprocessed matrix into train, validation, and test sets.
```bash
python dataset_split.py --input_file='/home/jovyan/proj-liujing/random/random_smiles.csv' --test_file='t1.csv' --train_file='t2.csv'
python dataset_split.py --input_file='/home/jovyan/proj-liujing/random/random_smiles.csv'
```
Optional parameters:
- `--test_size=` (default: 0.2)
- `--random_state=` (default: 42)

If output filenames (`--test_file` and `--train_file`) are not specified, the existing filenames will be overwritten.

Test dataset filenames: `test_matrix.csv` or `test_extracted_chembl.csv`.

## smi_to_pyg_00.py
Version 00 does not use one-hot encoding. Node and edge dimensions are `(5,2)`.

This script converts a dataset containing SMILES strings into the `Data` format recognizable by PyTorch and stores node and edge information.

### Features:
- **Node features:**
  - Atomic number: Number of protons in the atom.
  - Formal charge: Charge based on valence electrons and bonding.
  - Hybridization state: Describes how atomic orbitals mix (e.g., sp, sp2, sp3).
  - Degree: Number of bonds formed with neighboring atoms.
  - Implicit hydrogen count: Number of hydrogen atoms attached to the atom but not explicitly shown.
- **Edge features:**
  - Bond type
  - Conjugation status

```bash
python smi_to_pyg.py --input='/home/jovyan/proj-liujing/random/random_smiles.csv'
```
The test dataset used is `test_matrix.csv`.

Use `--input=` and `--output=` to specify input and output files. The default output file is `graph_data.pt`.

## smi_to_pyg_02.py
Version 02 uses one-hot encoding. Node and edge dimensions are `(39,9)`.

This script converts a dataset containing SMILES strings into PyTorch Geometric `Data` format while encoding atomic and bond properties using one-hot encoding.

### Features:
- **Node features:**
  - Atomic number (one-hot encoded for common elements)
  - Degree (one-hot for [0-5])
  - Formal charge
  - Radical electrons count
  - Hybridization state (one-hot)
  - Aromaticity
  - Hydrogen count (one-hot for [0-4])
  - Chirality (one-hot encoded for R/S)
- **Edge features:**
  - Bond type (single, double, triple, aromatic, one-hot)
  - Conjugation status (one-hot)
  - Ring status (one-hot)
  - Stereo configuration (one-hot for STEREONONE, STEREOZ, STEREOE)

```bash
python smi_to_pyg_02.py --input='/home/jovyan/proj-liujing/random/random_smiles.csv' --output='graph_data_02.pt'
```

Use `--input=` and `--output=` to specify the input and output files. The default output file is `graph_data_02.pt`.

## ECPF_conv.py
```bash
python ECPF_copy.py --input train_chunk_1.csv --output train_ecfp_chunk_1.csv
```
This script converts molecular data into Extended-Connectivity Fingerprints (ECFP) format.

## MyDataset Class
This custom dataset class is designed to handle SMILES-based molecular data and convert them into PyTorch Geometric `Data` format.

### Initialization:
- Reads SMILES and corresponding task values.
- Converts molecules using `smi_to_pyg`.
- Stores PyTorch Geometric `Data` objects.

### Methods:
- `__getitem__(idx)`: Returns the `Data` object at index `idx`.
- `__len__()`: Returns the total number of samples.
- `__head__(n=5)`: Returns the first `n` samples for previewing.

### Example Usage:
```python
from torch.utils.data import DataLoader

dataset = MyDataset(smiles_list, task_df)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
```




