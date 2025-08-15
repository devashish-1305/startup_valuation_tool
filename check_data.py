from utils import query_utils

# SCRIPT TO CHECK COLUMN NAMES AND DATA.

SYMBOL_TO_CHECK = 'AAPL'

print(f"--- Checking data for {SYMBOL_TO_CHECK} ---")

# Fetch the data using our utility
df = query_utils.get_financial_data(SYMBOL_TO_CHECK)

if not df.empty:
    # 1. Print all available column names
    print("\n[1] Available columns in the database table:")
    print(df.columns.tolist())

    # 2. Check the last few rows for the specific data we need
    print("\n[2] Last 5 rows for key DCF columns:")
    
    # We list potential variations of the column names to check
    potential_fcf_cols = ['freeCashFlow', 'Free Cash Flow', 'fcf']
    potential_shares_cols = ['sharesOutstanding', 'Shares Outstanding', 'shares_outstanding']
    
    # Filter to only show columns that actually exist in the DataFrame
    cols_to_check = ['date']
    for col_list in [potential_fcf_cols, potential_shares_cols]:
        for col in col_list:
            if col in df.columns:
                cols_to_check.append(col)
                break # Found one, move to the next list
    
    print(df[cols_to_check].tail())

else:
    print(f"Could not retrieve data for {SYMBOL_TO_CHECK}")

print("\n--- Check complete ---")
