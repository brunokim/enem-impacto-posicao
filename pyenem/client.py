from pathlib import Path
import time

from attrs import define, field
from attrs.validators import instance_of
from google.cloud.bigquery import Client as BigqueryClient
from google.cloud.storage import transfer_manager, Client as StorageClient

from pyenem.cache import Cache


@define
class Client:
    cache_dir = field(converter=Path, validator=instance_of(Path))
    bucket_path = field(converter=Path, validator=instance_of(Path))
    gcp_project = field(default="enem-microdata", validator=instance_of(str))
    bucket_name = field(default="enem-microdata", validator=instance_of(str))

    cache = field(init=False)
    bq = field(init=False)
    st = field(init=False)

    def __attrs_post_init__(self):
        self.cache = Cache(self.cache_dir)
        self.bq = BigqueryClient(project=self.gcp_project)
        self.st = StorageClient(project=self.gcp_project)
    
    def df_fetch(self, sql):
        key = self.cache.create(sql)
        result = self.bq.query_and_wait(sql)
        df = result.to_dataframe(progress_bar_type="tqdm")
        parquet_path = self.cache_dir / key / "data_0.parquet"
        df.to_parquet(parquet_path)
        return df
    
    def gcs_fetch(self, sql):
        key = self.cache.create(sql)
    
        dest_uri = f"gs://{self.bucket_name}/{self.bucket_path}/{key}/data_*.parquet"
        print(dest_uri)
        sql = f"""
            EXPORT DATA OPTIONS(uri="{dest_uri}", format="parquet", overwrite=true)
            AS {sql}
        """
        self.bq.query_and_wait(sql)
        print(f"Query done. Downloading...")
    
        bucket = self.st.bucket(self.bucket_name)
        blobs = list(bucket.list_blobs(match_glob=f"{self.bucket_path}/{key}/data_*.parquet"))
        blob_names = [Path(blob.name).name for blob in blobs]
        transfer_manager.download_many_to_path(
            bucket,
            blob_names,
            blob_name_prefix=f"{self.bucket_path}/{key}/",
            destination_directory=self.cache_dir / key,
            max_workers=16,
            raise_exception=True,
            create_directories=False,
        )
        print("Download done.")
        time.sleep(1)
    
        return self.cache.get_table(sql)
    
    def query(self, sql, fetch_strategy='df'):
        table = self.cache.get_table(sql)
        if table is not None:
            return table
        f = {'df': self.df_fetch, 'gcs': self.gcs_fetch}[fetch_strategy]
        return f(sql)