
import pandas as pd
from dagster import asset
from .dbt_assets import dbt_yellow_distance_moving
from ..constant import (
    PROCESS_SCHEMA,
    TABLE_PSQL_YELLOW_DISTANCE_MOVING
)


@asset(
    name=TABLE_PSQL_YELLOW_DISTANCE_MOVING.lower(),
    key_prefix=["result"],
    deps=([dbt_yellow_distance_moving]),
    required_resource_keys={"psql_result_extractor"},
    io_manager_key="minio_ts_io_manager",
    compute_kind='MinIO',
    description=f"upload to minio for table {TABLE_PSQL_YELLOW_DISTANCE_MOVING}"
)
def yellow_distance_moving(context) -> pd.DataFrame:
    sql_stm = f"SELECT * FROM {PROCESS_SCHEMA}.{TABLE_PSQL_YELLOW_DISTANCE_MOVING}"
    pd_data = context.resources.psql_result_extractor.extract_data(sql_stm, context)
    return pd_data

