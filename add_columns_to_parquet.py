import pandas as pd
import json

# Step 1: Read the JSON file
with open('summary_new.json', 'r') as json_file:
    json_data = json.load(json_file)

# Step 2: Extract MX and MY values
mapping = json_data["sample_id_map"]
mx_dict = {}
my_dict = {}
for key, value in mapping.items():
    if "NMSSM_XYH_Y_gg_H_bb" in key:
        mx, my = map(int, key.split("_MX_")[1].split("_MY_"))
        mx_dict[value] = mx
        my_dict[value] = my

# Step 3: Read the existing Parquet file
parquet_data = pd.read_parquet('merged_nominal_scored_skimmed.parquet')

# Step 4: Create a new DataFrame with MX and MY values
new_data = pd.DataFrame({'process_id': list(mapping.values())})
new_data['MX'] = new_data['process_id'].map(mx_dict)
new_data['MY'] = new_data['process_id'].map(my_dict)

# Step 5: Update MX and MY values where process_id is not in the mapping
new_data.loc[new_data['MX'].isnull(), ['MX', 'MY']] = 0

# Step 6: Merge the new DataFrame with the existing Parquet DataFrame based on 'process_id'
parquet_data = pd.merge(parquet_data, new_data, on='process_id', how='left')

# Step 7: Write the updated DataFrame back to a Parquet file
parquet_data.to_parquet('updated_merged_nominal_scored_skimmed.parquet', index=False)

