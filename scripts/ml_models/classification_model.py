import sys
import re
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import nltk
from nltk.corpus import stopwords

project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from utils.query_utils import get_all_mongo_documents

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

def train_risk_classifier():
    try:
        stopwords.words('english')
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords')

    documents = get_all_mongo_documents()
    if not documents:
        print("No documents found in MongoDB. Halting training.")
        return None, None, None
    
    df = pd.DataFrame(documents)
    df['clean_text'] = df['content'].apply(preprocess_text)
    
    high_risk_symbols = ['TSLA', 'NVDA', 'NFLX']
    df['risk_label'] = df['symbol'].apply(lambda x: 'High Risk' if x in high_risk_symbols else 'Low Risk')

    print("\n--- Label Distribution ---")
    print(df['risk_label'].value_counts())
    print("------------------------\n")

    X = df['clean_text']
    y = df['risk_label']

    if len(y.unique()) < 2:
        print("Still only one class after labeling. Halting.")
        return None, None, None

    vectorizer = TfidfVectorizer(max_features=1000)
    X_tfidf = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.3, random_state=42, stratify=y)

    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, zero_division=0)

    return model, vectorizer, report

# Example Test Run .
if __name__ == '__main__':
    print("--- Training Risk Classification Model (NLP) ---")
    trained_model, text_vectorizer, class_report = train_risk_classifier()
    
    if trained_model:
        print("\n✔ Model training complete.")
        print("\nClassification Report:")
        print(class_report)
        
        print("\n--- Example Prediction ---")
        sample_text_1 = "This company faces significant market risk and competition."
        sample_text_2 = "Our market position is stable and our growth is steady."

        for text in [sample_text_1, sample_text_2]:
            clean_sample = preprocess_text(text)
            vectorized_sample = text_vectorizer.transform([clean_sample])
            prediction = trained_model.predict(vectorized_sample)
            print(f"\nSample Text: '{text}'")
            print(f"  - Predicted Risk Level: {prediction[0]}")