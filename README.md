# ChEMBL-data-preparation

## data_extraction.py
```{bash}
python data_exraction.py --dp_path=
```
默认在当前目录下生成 `pIC50_ChEMBL.csv` 文件

## data_conversion.py
```{bash}
python data_convertion.py --file='/home/jovyan/proj-liujing/ramdon/testset.csv'
```
需要用 `--file=` 指定所需要转换为matrix的文件。 用于测试的文件名为`test_extracted_chembl.csv`

默认生成文件名为`chembl_matrix.csv` 文件名不会被覆盖，以及该文件所对应的 `target dictionary`


## data_split.py
将预处理好的matrix 分割train, val and test set. 
```{bash}
    python dataset_split.py --input_file='/home/jovyan/proj-liujing/ramdon/random_smiles.csv'  --test_file='t1.csv' --train_file='t2.csv'
    python dataset_split.py --input_file='/home/jovyan/proj-liujing/ramdon/random_smiles.csv'
```
还可以添加 `--test_size=` 和 `random_state=` 默认分别为0.2和42

如果不指定生成的`test_file` 和`train_file` 文件命名， 文件名会覆盖

用于测试的文件名为`test_matrix.csv` or `test_extracted_chembl.csv`




## smi_to_pyg.py
将含有smiles的matrix dataset转换为可供PyTorch识别的 `Data` 类型
把node, edge等信息保存
- node: 
    - 原子序数： 原子中质子的数量。
    - 正式电荷： 根据价电子和键合情况计算得出的电荷。
    - 杂化状态： 描述原子轨道混合形成化学键的方式（如 sp、sp2、sp3）。
    - 度数： 原子与邻近原子形成的键数。
    - 隐含氢原子数： 与原子连接的但未显式显示的氢原子数。
- Edge:
    - 键的类型
    - 是否共轭
```
python smi_to_pyg.py --input='/home/jovyan/proj-liujing/ramdon/random_smiles.csv'
```
用于测试的dataset为 `test_matrix.csv `
