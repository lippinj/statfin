import json
import os
import pathlib

import pandas as pd


_cache_dir = pathlib.Path(".statfin_cache")


def _cache_paths(name: str) -> tuple[pathlib.Path, pathlib.Path]:
    _cache_dir.mkdir(parents=True, exist_ok=True)
    return _cache_dir / f"{name}.meta", _cache_dir / f"{name}.df"


def clear() -> None:
    """
    Remove all cached data
    """
    try:
        os.removedirs(_cache_dir)
    except OSError:
        pass


def set_dir(dirname: str | pathlib.Path) -> None:
    """
    Set the parent directory for cache files
    """
    _cache_dir = pathlib.Path(dirname)


def load(name: str, fingerprint: dict) -> pd.DataFrame | None:
    """
    Load a dataframe from the given cache name

    There must also be a {path}.meta file which contains a "fingerprint" JSON
    for the dataframe. If not, the cached dataframe is rejected (and will
    probably be overwritten).
    """
    try:
        meta_path, df_path = _cache_paths(name)
        with open(meta_path, "r", encoding="utf-8") as f:
            j = json.load(f)
            if j != fingerprint:
                return None
        return pd.read_pickle(df_path)
    except:
        return None


def store(name: str, df: pd.DataFrame, fingerprint: dict) -> None:
    """
    Cache a dataframe to the given path
    """
    meta_path, df_path = _cache_paths(name)
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(fingerprint))
    df.to_pickle(df_path)
