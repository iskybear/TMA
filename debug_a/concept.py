import pandas as pd
from tma.collector.ths import get_plate_shares, get_ths_plates
from tma import data_path
import os

plates = get_ths_plates()

shares = []

for _, row in plates.iterrows():
    try:
        plate_name = row['name']
        plate_shares = get_plate_shares(row['code'], kind=row['kind_en'])
        for _, share in plate_shares.iterrows():
            shares.append([row['name'], share['代码'], share['名称']])
        print("success on %s" % row['name'])
    except:
        print("fail on %s" % row['name'])

shares_df = pd.DataFrame(shares, columns=['plate', 'share_code', 'share_name'])
shares_df.to_csv(os.path.join(data_path, "concept_ths.csv"), encoding='utf-8', index=False)
