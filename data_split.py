import argparse
import pandas as pd
from sklearn.model_selection import train_test_split


parser = argparse.ArgumentParser(description="Split dataset into train and test files.")
parser.add_argument("--input_file", type=str, required=True, help="Path to the input CSV file.")
parser.add_argument("--train_file", type=str, default='train_df.csv', help="Path to save the train CSV file.")
parser.add_argument("--test_file", type=str, default='test_df.csv', help="Path to save the test CSV file.")
parser.add_argument("--chunksize", type=int, default=100000, help="Number of rows per chunk. Default is 100000.")
parser.add_argument("--test_size", type=float, default=0.2, help="Proportion of the dataset to include in the test split. Default is 0.2.")
parser.add_argument("--random_state", type=int, default=42, help="Random state for reproducibility. Default is 42.")

args = parser.parse_args()


with open(args.train_file, 'w') as train_file, open(args.test_file, 'w') as test_file:
    for i, chunk in enumerate(pd.read_csv(args.input_file, chunksize=args.chunksize)):
        train_chunk, test_chunk = train_test_split(chunk, test_size=args.test_size, random_state=args.random_state)
        if i == 0:
            train_chunk.to_csv(train_file, index=False)
            test_chunk.to_csv(test_file, index=False)
        else:
            train_chunk.to_csv(train_file, index=False, header=False)
            test_chunk.to_csv(test_file, index=False, header=False)

print("Data has been split and saved!")
