import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import joblib

# Add project root to the Python path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import all your backend functions
from utils.query_utils import get_sql_data
from scripts.valuation.dcf_model import calculate_dcf
from scripts.valuation.berkus_model import calculate_berkus
from scripts.valuation.scorecard_model import calculate_scorecard
from scripts.valuation.risk_factor_model import calculate_risk_factor
from scripts.valuation.cost_to_duplicate_model import calculate_cost_to_duplicate
from scripts.valuation.vc_method_model import calculate_vc_method

# Use Streamlit's caching to load the ML models only once, making the app much faster.
@st.cache_resource
def load_models():
    try:
        regression_model = joblib.load('regression_model.joblib')
        clustering_model = joblib.load('clustering_model.joblib')
        scaler = joblib.load('clustering_scaler.joblib')
        return regression_model, clustering_model, scaler
    except FileNotFoundError:
        return None, None, None

regression_model, clustering_model, scaler = load_models()

# Cluster Definitions for user-friendly explanations
CLUSTER_DEFINITIONS = {
    0: "High-Growth / Volatile Tech (e.g., META, NFLX, NVDA, TSLA)",
    1: "Unique Behemoth - Retail & Cloud (e.g., AMZN)",
    2: "Mega-Cap Tech Giants (e.g., AAPL, GOOGL, MSFT)"
}

# --- Page Configuration (first Streamlit command) ---
st.set_page_config(
    page_title="Startup Valuation & Analysis Tool",
    page_icon="🚀",
    layout="wide"
)

# --- Welcome Section ---
st.title("🚀 Startup Valuation & Analysis Tool")
st.markdown("""
Welcome! This application is designed to make financial valuation fast and accessible.
- **For Public Companies:** Enter a stock ticker to perform a Discounted Cash Flow (DCF) analysis and see an ML-powered market cap prediction.
- **For Startups:** Use the sidebar to explore five different qualitative models for valuing early-stage ventures.

**To get started, enter a stock ticker in the box below (e.g., AAPL, GOOGL, MSFT).**
""")
st.divider()


# --- Sidebar for Startup Models ---
with st.sidebar:
    st.header("Early-Stage Startup Valuation")
    st.info("These models are for early-stage, pre-revenue startups.")

    with st.expander("ℹ️ Berkus Method Assumptions ($)"):
        st.write("Values a startup based on five key risk factors, assigning up to $500k for each.")
        berkus_idea = st.slider("Sound Idea", 0, 500000, 400000, 25000, format="%d")
        berkus_proto = st.slider("Prototype", 0, 500000, 300000, 25000, format="%d")
        berkus_mgmt = st.slider("Quality Management Team", 0, 500000, 500000, 25000, format="%d")
        berkus_relation = st.slider("Strategic Relationships", 0, 500000, 250000, 25000, format="%d")
        berkus_rollout = st.slider("Product Rollout", 0, 500000, 150000, 25000, format="%d")

    with st.expander("ℹ️ Scorecard Method Assumptions"):
        st.write("Compares your startup to other funded startups in the same region and market.")
        scorecard_avg_val = st.number_input("Avg. Pre-Money Valuation ($)", value=2000000, step=100000, format="%d")
        scorecard_mgmt = st.slider("Management Team Strength (0.5-1.5x)", 0.5, 1.5, 1.25, 0.05)
        scorecard_size = st.slider("Size of Opportunity (0.5-1.5x)", 0.5, 1.5, 1.50, 0.05)
        scorecard_prod = st.slider("Product/Technology Strength (0.5-1.5x)", 0.5, 1.5, 1.0, 0.05)

    with st.expander("ℹ️ Risk Factor Summation Assumptions ($)"):
        st.write("Starts with an average valuation and adjusts it based on common risk factors.")
        risk_avg_val = st.number_input("Avg. Pre-Money Valuation ($)", value=1500000, step=100000, format="%d", key="risk_avg")
        risk_mgmt = st.slider("Management Risk Adj.", -500000, 500000, 250000, 25000, format="%d")
        risk_stage = st.slider("Stage of Business Risk Adj.", -500000, 500000, 125000, 25000, format="%d")
        risk_comp = st.slider("Competition Risk Adj.", -500000, 500000, -250000, 25000, format="%d")

    with st.expander("ℹ️ Cost-to-Duplicate Assumptions ($)"):
        st.write("Values the business based on the estimated cost to build it from scratch.")
        cost_r_d = st.number_input("R&D Costs ($)", value=150000, step=10000, format="%d")
        cost_salaries = st.number_input("Dev Salaries ($)", value=250000, step=10000, format="%d")
        cost_assets = st.number_input("Physical Assets ($)", value=20000, step=5000, format="%d")

    with st.expander("ℹ️ VC Method Assumptions"):
        st.write("Calculates a pre-money valuation based on a future exit value and required ROI.")
        vc_revenue = st.number_input("Projected Revenue at Exit ($)", value=50000000, step=1000000, format="%d")
        vc_multiple = st.number_input("Industry P/S Multiple", value=4.0, step=0.5)
        vc_roi = st.number_input("Required ROI (Multiple)", value=20.0, step=1.0)
        vc_investment = st.number_input("Investment Amount ($)", value=2000000, step=100000, format="%d")

    if st.button("Run Startup Models", key='sidebar_button'):
        st.subheader("Valuation Results")
        
        berkus_scores = {'sound_idea': berkus_idea, 'prototype': berkus_proto, 'management_team': berkus_mgmt, 'strategic_relationships': berkus_relation, 'product_rollout': berkus_rollout}
        berkus_val = calculate_berkus(berkus_scores)
        st.metric(label="Berkus Method", value=f"${berkus_val:,.0f}")
        
        scorecard_factors = { 'management_team': (0.30, scorecard_mgmt), 'size_of_opportunity': (0.25, scorecard_size), 'product_technology': (0.15, scorecard_prod), 'competitive_environment': (0.10, 1.0), 'marketing_sales': (0.10, 1.0), 'need_for_funding': (0.05, 1.0), 'other': (0.05, 1.0) }
        scorecard_val = calculate_scorecard(scorecard_avg_val, scorecard_factors)
        st.metric(label="Scorecard Method", value=f"${scorecard_val:,.0f}")

        risk_scores = {'management_risk': risk_mgmt, 'stage_of_business': risk_stage, 'competition_risk': risk_comp}
        risk_factor_val = calculate_risk_factor(risk_avg_val, risk_scores)
        st.metric(label="Risk Factor Summation", value=f"${risk_factor_val:,.0f}")
        
        cost_inputs = {'research_and_development': cost_r_d, 'software_development_salaries': cost_salaries, 'physical_assets_computers': cost_assets}
        cost_val = calculate_cost_to_duplicate(cost_inputs)
        st.metric(label="Cost-to-Duplicate", value=f"${cost_val:,.0f}")
        
        vc_val = calculate_vc_method(vc_revenue, vc_multiple, vc_roi, vc_investment)
        st.metric(label="VC Method (Pre-Money)", value=f"${vc_val['pre_money_valuation']:,.0f}")
        
        st.subheader("How to Interpret These Results")
        st.info("""
        These models provide a *range* of possible valuations. Investors use this range to inform their negotiation, often taking an average after discarding the highest and lowest values.
        """)

# --- Main Page for Public Company Analysis ---
st.header("Public Company Analysis")
st.caption("Note: This analysis works for the 8 pre-loaded companies: AAPL, GOOGL, MSFT, AMZN, TSLA, NVDA, META, NFLX.")
symbol = st.text_input("Enter a Stock Symbol from the list above:", "AAPL").upper()

with st.expander("ℹ️ What is a DCF Valuation?"):
    st.write("""
    A Discounted Cash Flow (DCF) analysis estimates a company's value based on its expected future cash flows. 
    You can adjust the key assumptions below to see how they impact the final valuation.
    """)

st.subheader("DCF Valuation Assumptions")
col_g, col_p, col_w = st.columns(3)
g_rate = col_g.slider("5-Year Growth Rate (%)", 1.0, 20.0, 6.0, 0.5) / 100
p_rate = col_p.slider("Perpetual Growth Rate (%)", 1.0, 5.0, 2.5, 0.1) / 100
wacc = col_w.slider("Discount Rate (WACC) (%)", 5.0, 15.0, 9.0, 0.5) / 100

# Main action button for the public company analysis.
if st.button("Run Full Analysis", key='main_button'):
    if not symbol:
        st.error("Please enter a stock symbol.")
    elif regression_model is None:
        st.error("ML models not found. Please check if model files are present.")
    else:
        with st.spinner(f'Fetching data and running analysis for {symbol}...'):
            data = get_sql_data(symbol)
            if data.empty:
                st.error("Could not fetch data. Please enter one of the 8 pre-loaded symbols.")
            else:
                latest_data = data.iloc[-1]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("DCF Valuation")
                    dcf_value = calculate_dcf(symbol, g_rate, p_rate, wacc)
                    st.metric(
                        label="Intrinsic Value per Share", 
                        value=f"${dcf_value:,.2f}",
                        help="The value calculated based on future cash flows using your assumptions."
                    )

                with col2:
                    st.subheader("Machine Learning Insights")
                    
                    features = ['freeCashFlow', 'totalDebt', 'cashAndCashEquivalents', 'volume']
                    predict_data = pd.DataFrame([latest_data[features]])
                    
                    predicted_market_cap = regression_model.predict(predict_data)[0]
                    st.metric(
                        label="Predicted Market Cap (XGBoost)", 
                        value=f"${predicted_market_cap:,.0f}",
                        help="Market cap predicted by the regression model based on financial metrics."
                    )
                    
                    scaled_data = scaler.transform(predict_data)
                    cluster = clustering_model.predict(scaled_data)[0]
                    
                    st.metric(
                        label="Peer Group (K-Means)", 
                        value=f"Cluster {cluster}",
                        help="A group of companies with similar financial structures."
                    )
                    st.info(f"**This company belongs to the '{CLUSTER_DEFINITIONS[cluster]}' peer group.**")

                st.subheader("Latest Financial Data")
                st.dataframe(data.tail())