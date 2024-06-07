import json
import pandas as pd


def load(path: str, fingerprint: dict) -> pd.DataFrame | None:
    """
    Load a dataframe from the given cache path

    There must also be a {path}.meta file which contains a "fingerprint" JSON
    for the dataframe. If not, the cached dataframe is rejected (and will
    probably be overwritten).
    """
    try:
        with open(f"{path}.meta", "r") as f:
            j = json.load(f)
            if j != fingerprint:
                return None
        return pd.read_pickle(path)
    except:
        return None


def store(path: str, df: pd.DataFrame, fingerprint: dict) -> None:
    """
    Cache a dataframe to the given path
    """
    with open(f"{path}.meta", "w") as f:
        f.write(json.dumps(fingerprint))
    df.to_pickle(path)
