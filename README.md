# 🚀 Startup Valuation & Analysis Tool

---
### Executive Summary
This project is an easy-to-use web application that makes company valuation fast and simple. It automatically gathers the latest financial data and uses both traditional financial models and modern AI to help determine a company's worth. For an investor, this tool helps in making smarter, quicker decisions. For a startup founder, it helps in understanding their company's potential value in the market.
---

## Live Demo
Check out the live demo: **[Startup Valuation & Analysis Tool](https://startupvaluationtool-cktwmgeh4ow4oikct6wzf.streamlit.app/)**

## 🎯 Quick Start Guide
After launching the app, try this example workflow:
1.  Enter the ticker "AAPL" in the text input on the main page.
2.  Adjust the "Discount Rate (WACC)" slider to see how it impacts the DCF valuation in real-time.
3.  Compare the DCF Intrinsic Value with the ML-Predicted Market Cap.
4.  Navigate to the sidebar to explore the five different valuation models for early-stage startups.

---

## Project Motivation & Real-World Application

### The Problem: The Valuation Gap
Financial valuation is a complex and often fragmented process. 
1.  **For Public Companies:** Analysts spend hundreds of hours manually gathering data from disparate sources (APIs, public filings) to feed into complex, static spreadsheets. Comparing companies or performing scenario analysis is cumbersome and slow.
2.  **For Startups:** Early-stage, pre-revenue startups are notoriously difficult to value due to a lack of financial history. This creates a significant "valuation gap," leading to difficult and often subjective negotiations between founders and investors.
3.  **For Both:** There is a lack of unified platforms that combine traditional financial models (like DCF) with machine learning insights (like peer group clustering) and qualitative assessments.

### The Solution: A Unified, Automated Platform
This project was built to bridge that gap by providing a single, end-to-end tool that addresses these challenges:

* **Automation & Efficiency:** The **Apache Airflow** pipeline automates the entire data gathering and processing workflow, saving time and ensuring data is always fresh and reliable.
* **Holistic Analysis:** The application provides a comprehensive framework. It combines a dynamic **DCF model** with **XGBoost regression** and **K-Means clustering** for a multi-faceted view of public companies. For startups, it offers five distinct heuristic models, providing a defensible *range* of valuations rather than a single, arbitrary number.
* **Democratized Decision-Making:** The interactive **Streamlit** dashboard makes this complex analysis accessible. It allows users to perform real-time scenario modeling and stress-test assumptions, enabling faster, more data-informed investment or strategic decisions.

---

## Key Features
* **Dual Valuation Capability:** Analyze public companies with quantitative models (DCF, ML) or evaluate early-stage startups with five different qualitative models.
* **Interactive Dashboard:** A user-friendly interface built with Streamlit for dynamic analysis and scenario modeling.
* **Machine Learning Insights:** Includes models for market cap prediction and peer group clustering.
* **Automated Data Pipeline:** Daily data updates orchestrated with Apache Airflow.

---

## Project Architecture
The application is built with a decoupled architecture, separating the backend data pipeline from the frontend user interface.

`[APIs: FMP, Yahoo, SEC] -> [Airflow Pipeline: Fetch, Clean, Merge] -> [Databases: SQLite, MongoDB] -> [Streamlit App: UI, Models]`

---

## Tech Stack
* **Data Science & ML:** Python, Pandas, Scikit-learn, XGBoost
* **Web Framework:** Streamlit
* **Data Pipeline & Orchestration:** Apache Airflow
* **Databases:** SQLite (for structured data), MongoDB (for unstructured text data)
* **APIs:** Financial Modeling Prep, yfinance, SEC EDGAR

---

## Local Setup & Installation

### Prerequisites
* Git
* Conda
* Python 3.9+

### Instructions
1.  **Clone the repository:**
    ```bash
    git clone  https://github.com/devashish-1305/startup_valuation_tool.git 
    cd startup-valuation-tool
    ```
2.  **Create your Environment Variables file:**
    * Create a file named `.env` in the main project directory.
    * Add your API keys to this file:
        ```
        FMP_API_KEY="your_fmp_api_key_here"
        SEC_EDGAR_EMAIL="your_name@email.com"
        ```
3.  **Run the application:**
    * **On Mac/Linux:**
        ```bash
        # Make the script executable (only need to do this once)
        chmod +x start.sh
        # Run the entire project (Airflow + Streamlit)
        ./start.sh
        ```
    * **On Windows:**
        ```batch
        start.bat
        ```
4.  **Access the application:**
    * Streamlit UI: `http://localhost:8501`
    * Airflow UI: `http://localhost:8080` (default login: admin/admin)

---

## Model Development & Future Work

During development, several machine learning models were built and evaluated:

* **Regression (XGBoost):** *[Included in the final app]* Predicts a company's market cap based on its financial metrics.
* **Clustering (K-Means):** *[Included in the final app]* Groups similar companies into peer groups based on their financial structure.
* **Classification:** A model was developed to predict short-term stock price movement (up/down).
* **Forecasting (Prophet):** A time-series model was built to forecast future stock prices.

For the final version of the interactive dashboard, the focus was narrowed to the regression and clustering models as they provide the most direct and actionable insights for company valuation and comparison. The code for the other models remains in the repository, and they could be integrated into the app as a future feature.