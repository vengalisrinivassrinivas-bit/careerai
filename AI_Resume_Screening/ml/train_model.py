import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

# Import text cleaning function from preprocessing
from preprocessing import clean_text

def train_and_evaluate():
    # Define paths
    dataset_path = "AI_Resume_Screening/data/UpdatedResumeDataSet.csv"
    models_dir = "AI_Resume_Screening/models"
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Load Dataset
    print(f"Loading dataset from: {dataset_path}")
    if not os.path.exists(dataset_path):
        # Allow running from current folder as well
        dataset_path = "data/UpdatedResumeDataSet.csv"
        models_dir = "models"
        if not os.path.exists(dataset_path):
            raise FileNotFoundError("UpdatedResumeDataSet.csv not found in data directories.")
            
    df = pd.read_csv(dataset_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Dataset columns: {df.columns.tolist()}")
    
    # Ensure columns match expected 'Category' and 'Resume'
    if 'Category' not in df.columns or 'Resume' not in df.columns:
        raise ValueError("Dataset must contain 'Category' and 'Resume' columns.")
        
    # 2. Preprocess text
    print("Preprocessing resume text...")
    df['Cleaned_Resume'] = df['Resume'].apply(clean_text)
    
    # 3. TF-IDF Vectorization
    print("Vectorizing text using TF-IDF...")
    tfidf = TfidfVectorizer(max_features=5000, sublinear_tf=True)
    X = tfidf.fit_transform(df['Cleaned_Resume'])
    y = df['Category']
    
    # 4. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    
    # 5. Train & Evaluate Models
    # Model 1: Logistic Regression (Primary)
    print("\n--- Training Logistic Regression Model ---")
    log_reg = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    log_reg.fit(X_train, y_train)
    y_pred_lr = log_reg.predict(X_test)
    
    lr_acc = metrics.accuracy_score(y_test, y_pred_lr)
    lr_prec = metrics.precision_score(y_test, y_pred_lr, average='weighted')
    lr_rec = metrics.recall_score(y_test, y_pred_lr, average='weighted')
    lr_f1 = metrics.f1_score(y_test, y_pred_lr, average='weighted')
    
    # Model 2: Multinomial Naive Bayes (Baseline)
    print("--- Training Multinomial Naive Bayes Model ---")
    naive_bayes = MultinomialNB(alpha=1.0)
    naive_bayes.fit(X_train, y_train)
    y_pred_nb = naive_bayes.predict(X_test)
    
    nb_acc = metrics.accuracy_score(y_test, y_pred_nb)
    nb_prec = metrics.precision_score(y_test, y_pred_nb, average='weighted')
    nb_rec = metrics.recall_score(y_test, y_pred_nb, average='weighted')
    nb_f1 = metrics.f1_score(y_test, y_pred_nb, average='weighted')
    
    # 6. Compare Metrics
    print("\n" + "="*50)
    print("MODEL COMPARISON SUMMARY")
    print("="*50)
    print(f"{'Metric':<15} | {'Logistic Regression':<20} | {'Naive Bayes':<15}")
    print("-"*55)
    print(f"{'Accuracy':<15} | {lr_acc:<20.4f} | {nb_acc:<15.4f}")
    print(f"{'Precision':<15} | {lr_prec:<20.4f} | {nb_prec:<15.4f}")
    print(f"{'Recall':<15} | {lr_rec:<20.4f} | {nb_rec:<15.4f}")
    print(f"{'F1 Score':<15} | {lr_f1:<20.4f} | {nb_f1:<15.4f}")
    print("="*50)
    
    # Determine the best model based on F1 Score
    best_model_name = "Logistic Regression" if lr_f1 >= nb_f1 else "Multinomial Naive Bayes"
    best_model = log_reg if lr_f1 >= nb_f1 else naive_bayes
    best_f1 = max(lr_f1, nb_f1)
    
    print(f"\nWinner: {best_model_name} with F1-Score of {best_f1:.4f}")
    
    # Print classification report & confusion matrix for the winning model
    y_pred_best = y_pred_lr if lr_f1 >= nb_f1 else y_pred_nb
    print("\nClassification Report (Best Model):")
    print(metrics.classification_report(y_test, y_pred_best))
    
    # 7. Save models
    classifier_path = os.path.join(models_dir, "resume_classifier.pkl")
    tfidf_path = os.path.join(models_dir, "tfidf.pkl")
    
    print(f"\nSaving best classifier model to {classifier_path}...")
    joblib.dump(best_model, classifier_path)
    
    print(f"Saving TF-IDF Vectorizer to {tfidf_path}...")
    joblib.dump(tfidf, tfidf_path)
    
    print("Training process finished successfully!")

if __name__ == "__main__":
    train_and_evaluate()
