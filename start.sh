#!/bin/bash
echo " Starting Startup Valuation Tool..."
source /opt/anaconda3/bin/activate valuation_env
export AIRFLOW_HOME="$(pwd)/airflow"
echo " Starting Airflow server in the background..."
airflow standalone > /dev/null 2>&1 &
sleep 15
echo "Starting Streamlit dashboard..."
streamlit run app.py