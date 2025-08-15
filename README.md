# 🚀 Startup Valuation & Analysis Tool

This project is an end-to-end data science application designed to demystify company valuation. It combines traditional financial models with modern machine learning techniques, all presented through an interactive web dashboard. The entire data backend is managed by a daily automated ETL pipeline orchestrated with Apache Airflow.

---
## Live Demo
Check out the live, interactive demo hosted on Streamlit Community Cloud: 

**[Your Live App URL Will Go Here After You Deploy]**

---
## Key Features
* **Dual Valuation Capability:** Analyze public companies with quantitative models (DCF, ML Regression) or evaluate early-stage startups with five different qualitative models (Berkus, Scorecard, etc.).
* **Interactive Dashboard:** A user-friendly and intuitive interface built with Streamlit for dynamic analysis and scenario modeling.
* **Machine Learning Insights:** Includes an XGBoost model for market cap prediction and a K-Means model for clustering companies into financially similar peer groups.
* **Automated Data Pipeline:** A robust data pipeline built with Apache Airflow that runs daily to fetch, clean, merge, and load the latest financial data.

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
    git clone <your-repo-url>
    cd startup-valuation-tool
    ```
2.  **Set up the environment:**
    * This project uses a Conda environment. The `start.sh` and `start.bat` scripts will attempt to activate it automatically. Ensure you have a Conda environment named `valuation_env`. If not, create it from the `requirements.txt` file.
3.  **Create your Environment Variables file:**
    * Create a file named `.env` in the main project directory.
    * Add your API keys and contact info to this file:
        ```
        FMP_API_KEY="your_fmp_api_key_here"
        SEC_EDGAR_EMAIL="your_name@email.com"
        ```
4.  **Run the application:**
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
5.  **Access the application:**
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