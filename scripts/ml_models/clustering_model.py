import sys
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.query_utils import get_all_sql_data

def find_company_clusters(n_clusters=3):
    data = get_all_sql_data()
    if data.empty:
        print("No data found. Halting clustering.")
        return None

    features_for_clustering = ['freeCashFlow', 'totalDebt', 'cashAndCashEquivalents', 'volume']
    
    data_for_clustering = data.dropna(subset=features_for_clustering).copy()
    
    if len(data_for_clustering) < n_clusters:
        print("Not enough data to form the requested number of clusters.")
        return None

    X = data_for_clustering[features_for_clustering]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    data_for_clustering['cluster'] = kmeans.fit_predict(X_scaled)

    final_clusters = data_for_clustering.groupby('symbol')['cluster'].agg(lambda x: x.mode()[0])
    return final_clusters.reset_index()

# Example Test Run.
if __name__ == '__main__':
    print("--- Finding Company Clusters (K-Means) ---")
    
    number_of_clusters = 3
    clustered_companies = find_company_clusters(n_clusters=number_of_clusters)
    
    if clustered_companies is not None:
        print(f"\n✔ Clustering complete. Companies grouped into {number_of_clusters} clusters.\n")
        
        for i in range(number_of_clusters):
            print(f"--- Cluster {i} ---")
            companies_in_cluster = clustered_companies[clustered_companies['cluster'] == i]['symbol'].tolist()
            print(", ".join(companies_in_cluster))