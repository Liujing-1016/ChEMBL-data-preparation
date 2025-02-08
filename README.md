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

## ECPF_conv.py
```bash
python ECPF_copy.py --input train_chunk_1.csv --output train_ecfp_chunk_1.csv
```
This script converts molecular data into Extended-Connectivity Fingerprints (ECFP) format.


