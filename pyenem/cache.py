from hashlib import md5
from pathlib import Path
import re

from attrs import frozen, field
from attrs.validators import instance_of
import pandas as pd


def normalize_formula(text):
    # Remove comments
    text = re.sub(r"(?m)#.*$", "", text)
    # Remove newlines and redundant whitespace.
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    # Remove space between words and symbols.
    text = re.sub(r"(\W) (\w)", r"\1\2", text)
    text = re.sub(r"(\w) (\W)", r"\1\2", text)
    return text


def normalize_sql(text):
    # Remove comments
    text = re.sub(r"(?m)--.*$", "", text)
    # Remove newlines and redundant whitespace.
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    # Remove space between words and symbols.
    text = re.sub(r"\s*([,()])\s*", r"\1", text)
    text = re.sub(r"(\W) (\w)", r"\1\2", text)
    text = re.sub(r"(\w) (\W)", r"\1\2", text)
    return text


def md5_hash(text):
    h = md5()
    h.update(text.encode("utf8"))
    return h.hexdigest()[:8]


def sql_key(text):
    return md5_hash(normalize_sql(text))


def formula_key(text):
    return md5_hash(normalize_formula(text))


@frozen
class Cache:
    cache_dir = field(converter=Path, validator=instance_of(Path))
    
    def get_table(self, sql):
        key = sql_key(sql)
        subdir = self.cache_dir / key
        pq_files = list(subdir.glob("data_*.parquet"))
        if not pq_files:
            return None
        print(f"Read from cache {key}")
        return pd.concat(pd.read_parquet(pq_file) for pq_file in pq_files)
    
    def create(self, sql):
        key = sql_key(sql)
        subdir = self.cache_dir / key
        subdir.mkdir(exist_ok=True)
        sql_path = subdir / "query.sql"
        with sql_path.open("wt") as f:
            f.write(sql)
        print(f"Create cache for {key}")
        return key
