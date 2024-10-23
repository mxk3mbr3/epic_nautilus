import requests
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.base_hook import BaseHook

from airflow import DAG
from datetime import datetime
from airflow.utils.dates import days_ago

# Define Class PowerBIDataflowRefreshOperator

class PowerBIDataflowRefreshOperator(BaseOperator):
    @apply_defaults
    def __init__(self, group_id, dataflow_id, powerbi_conn_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_id = group_id
        self.dataflow_id = dataflow_id
        self.powerbi_conn_id = powerbi_conn_id

    def execute(self, context):
        # Step 1: Retrieve connection details
        connection = BaseHook.get_connection(self.powerbi_conn_id)

        # Step 2: Extract credentials from connection
        client_id = connection.login
        client_secret = connection.password
        tenant_id = connection.extra_dejson.get('tenantId')  # No need to load JSON

        # Step 3: Get the Azure AD token
        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default',
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        access_token = response.json().get('access_token')

        # Step 4: Refresh the dataflow
        refresh_url = f"https://api.powerbi.com/v1.0/myorg/groups/{self.group_id}/dataflows/{self.dataflow_id}/refreshes"
        headers = {'Authorization': f'Bearer {access_token}'}
        refresh_response = requests.post(refresh_url, headers=headers)
        refresh_response.raise_for_status()

        return refresh_response.json()

# Dataflow DAG

with DAG(
        dag_id='refresh_dataflow_powerbi',
        schedule_interval=None,
        start_date=datetime(2024, 10, 22),
        catchup=False,
        tags=['powerbi', 'dataflow', 'refresh']
) as dag:

    refresh_dataflow_test = PowerBIDataflowRefreshOperator(
        task_id="refresh_dataflow_test",
        powerbi_conn_id="powerbi_conn",
        dataflow_id="e1ea643c-3160-49b9-a5b8-a3718162dd43",
        group_id="d01c785c-61ea-4acf-8fe6-21dd97af0112"
    )

    refresh_dataflow_test
