# ChEMBL-data-preparation

## Data_extraction
`python data_exraction.py --dp_path=`
默认在当前目录下生成 `pIC50_ChEMBL.csv` 文件


## Data split
用于分割train, val and test set. 
    python dataset_split.py --input_file='/home/jovyan/proj-liujing/ramdon/random_smiles.csv'  --test_file='t1.csv' --train_file='t2.csv'
    python dataset_split.py --input_file='/home/jovyan/proj-liujing/ramdon/random_smiles.csv' 
还可以添加 `--test_size=` 和 `random_state=` 默认分别为0.2和42
如果不指定生成的`test_file` 和`train_file` 文件命名， 文件名会覆盖
用于测试的文件名为`test_matrix.csv` or `test_extracted_chembl.csv`

## Data_conversion
`python data_convertion.py --file='/home/jovyan/proj-liujing/ramdon/testset.csv' `
需要用 `--file=` 指定所需要转换为matrix的文件。 用于测试的文件名为`test_extracted_chembl.csv`
默认生成文件名为`chembl_matrix.csv` 文件名不会被覆盖，以及该文件所对应的 `target dictionary`

## smi_to_pyg

