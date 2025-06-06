import pandas as pd


class QueryResponse:
    def __init__(self, df):
        self.df = df

    def map(self, *to_keep, **to_remap) -> pd.DataFrame:
        """
        Map to a new DataFrame with given values only
        
        to_keep: columns that should be kept as-is.
        to_remap: columns that should be renamed, newname=oldname.
        """
        out = self.df[[*to_keep]]
        for out_key, in_key in to_remap.items():
            out[out_key] = self.df[in_key]
        return out
