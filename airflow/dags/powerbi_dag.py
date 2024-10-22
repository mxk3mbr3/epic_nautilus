from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow_powerbi_plugin.operators.powerbi import PowerBIDatasetRefreshOperator

with DAG(
        dag_id='refresh_dataset_powerbi',
        schedule_interval=None,
        start_date=datetime(2024, 10, 21),
        catchup=False,
        tags=['powerbi', 'dataset', 'refresh']
) as dag:

    refresh_in_test_workspace = PowerBIDatasetRefreshOperator(
        task_id="refresh_in_test_workspace",
        powerbi_conn_id="powerbi_conn",
        dataset_id="0491fd0d-175d-43ba-8a4c-7090bae49ceb",
        group_id="d01c785c-61ea-4acf-8fe6-21dd97af0112"
    )

    refresh_in_test_workspace