import sys
import pandas as pd
import json

def parquet2jsonl(parquet_file, json_file):
    df = pd.read_parquet(parquet_file)
    with open(json_file, 'a') as f:
        df.to_json(f, orient='records', lines=True)



if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("please use the script by: \n``\npython parquet2jsonl.py <input_parquet_file> <output_jsonl_file>\n``\n")
    else:
        parquet2jsonl(sys.argv[1], sys.argv[2])
