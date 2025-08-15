from __future__ import annotations
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
import subprocess

project_path = "/Users/devashishdwivedi/Documents/startup_valuation_tool"
python_executable = "/opt/anaconda3/envs/valuation_env/bin/python"

def check_scripts(**context):
    """Verify all scripts exist before running"""
    scripts = [
        "scripts/fetching/fetch_all_raw.py",
        "scripts/cleaning/clean_fmp.py",
        "scripts/cleaning/clean_sec.py",
        "scripts/cleaning/clean_yfinance.py",
        "scripts/integration/merge_company_data.py",
        "scripts/integration/db_push.py",
        "scripts/integration/mongo_push.py"
    ]
    
    missing = []
    for script in scripts:
        full_path = os.path.join(project_path, script)
        if not os.path.exists(full_path):
            missing.append(script)
        else:
            print(f"✓ Found: {script}")
    
    if missing:
        raise FileNotFoundError(f"Missing scripts: {', '.join(missing)}")
    
    result = subprocess.run([python_executable, "--version"], capture_output=True, text=True)
    print(f"Python version: {result.stdout}")
    
    return "All scripts and environment found!"

# This DAG is scheduled to run daily at 2 AM UTC, ensuring the financial data
# is refreshed before the start of the next business day.
with DAG(
    dag_id="data_pipeline_workflow",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule="0 2 * * *",
    catchup=False,
    tags=["data_pipeline"],
    doc_md="""
    This DAG runs the entire data pipeline for the valuation tool.
    1. Fetches all raw data.
    2. Cleans FMP, SEC, and Yahoo Finance data in parallel.
    3. Merges all cleaned data.
    4. Loads the final data into SQLite and MongoDB in parallel.
    """,
) as dag:
    
    # A pre-flight check to ensure all script files exist. This helps the pipeline
    # fail quickly if the project structure is incorrect, saving time.
    check_task = PythonOperator(
        task_id="check_all_scripts_exist",
        python_callable=check_scripts,
    )
    
    fetch_task = BashOperator(
        task_id="fetch_all_raw_data",
        bash_command=f'cd "{project_path}" && "{python_executable}" scripts/fetching/fetch_all_raw.py',
    )

    clean_fmp_task = BashOperator(
        task_id="clean_fmp_data",
        bash_command=f'cd "{project_path}" && "{python_executable}" scripts/cleaning/clean_fmp.py',
    )
    
    clean_sec_task = BashOperator(
        task_id="clean_sec_data",
        bash_command=f'cd "{project_path}" && "{python_executable}" scripts/cleaning/clean_sec.py',
    )

    clean_yf_task = BashOperator(
        task_id="clean_yfinance_data",
        bash_command=f'cd "{project_path}" && "{python_executable}" scripts/cleaning/clean_yfinance.py',
    )

    merge_task = BashOperator(
        task_id="merge_cleaned_data",
        bash_command=f'cd "{project_path}" && "{python_executable}" scripts/integration/merge_company_data.py',
    )

    load_sqlite_task = BashOperator(
        task_id="load_to_sqlite",
        bash_command=f'cd "{project_path}" && "{python_executable}" scripts/integration/db_push.py',
    )

    load_mongo_task = BashOperator(
        task_id="load_to_mongodb",
        bash_command=f'cd "{project_path}" && "{python_executable}" scripts/integration/mongo_push.py',
    )

    # This line defines the entire workflow. The tasks in lists (e.g., cleaning)
    # run in parallel to make the pipeline faster.
    check_task >> fetch_task >> [clean_fmp_task, clean_sec_task, clean_yf_task] >> merge_task >> [load_sqlite_task, load_mongo_task]