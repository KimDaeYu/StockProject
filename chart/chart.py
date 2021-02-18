import pandas as pd
import FinanceDataReader as fdr
from ta import add_all_ta_features
from ta.utils import dropna


# Load datas
df = fdr.DataReader('005930')

print(fdr)
# Clean NaN values
df = dropna(df)

# Add all ta features
df = add_all_ta_features(
    df, open="Open", high="High", low="Low", close="Close", volume="Volume_BTC")