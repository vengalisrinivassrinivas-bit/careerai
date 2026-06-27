import os
import joblib
import numpy as np
from typing import Dict, List, Tuple, Any

# Import text cleaning function
from ml.preprocessing import clean_text

class ResumePredictor:
    """
    Handles loading the trained classifier and TF-IDF models to perform
    predictions on new resumes and explain predictions using XAI keyword weights.
    """
    
    def __init__(self, models_dir: str = "AI_Resume_Screening/models"):
        """
        Initializes the predictor, loading the classifier and vectorizer models.
        """
        # Resolve paths
        self.classifier_path = os.path.join(models_dir, "resume_classifier.pkl")
        self.tfidf_path = os.path.join(models_dir, "tfidf.pkl")
        
        # Fallback pathing for local script executions
        if not os.path.exists(self.classifier_path):
            self.classifier_path = "models/resume_classifier.pkl"
            self.tfidf_path = "models/tfidf.pkl"
            
        if not os.path.exists(self.classifier_path) or not os.path.exists(self.tfidf_path):
            raise FileNotFoundError("Classifier or TF-IDF pickle files not found. Run train_model.py first.")
            
        # Load pickle files
        self.classifier = joblib.load(self.classifier_path)
        self.tfidf = joblib.load(self.tfidf_path)
        self.feature_names = self.tfidf.get_feature_names_out()
        
    def predict(self, raw_text: str) -> Dict[str, Any]:
        """
        Cleans the input text, runs vectorizer transformation, predicts the job role,
        estimates prediction confidence, and extracts explainable AI matching keywords.
        
        Args:
            raw_text (str): The raw text of the resume.
            
        Returns:
            Dict[str, Any]: Predicted category, confidence score, and top matching keywords.
        """
        # 1. Clean Text
        cleaned_text = clean_text(raw_text)
        
        if not cleaned_text:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "top_keywords": []
            }
            
        # 2. Vectorize
        X_vector = self.tfidf.transform([cleaned_text])
        X_dense = X_vector.toarray()[0]
        
        # 3. Predict & Confidence
        prediction = self.classifier.predict(X_vector)[0]
        
        # Get confidence using predict_proba
        try:
            proba = self.classifier.predict_proba(X_vector)[0]
            class_labels = self.classifier.classes_
            class_idx = np.where(class_labels == prediction)[0][0]
            confidence = proba[class_idx] * 100.0  # Percentage
        except Exception:
            confidence = 100.0  # Fallback
            
        # 4. Explainable AI (XAI) - Extract Top 10 Keywords contributing to predicted class
        top_keywords = []
        try:
            class_labels = self.classifier.classes_
            class_idx = np.where(class_labels == prediction)[0][0]
            
            # Check model type to get weights
            if hasattr(self.classifier, "coef_"):
                # Logistic Regression: Contributions = TF-IDF * Coefficient
                coefs = self.classifier.coef_[class_idx]
                contributions = X_dense * coefs
            elif hasattr(self.classifier, "feature_log_prob_"):
                # Naive Bayes: Contributions = TF-IDF * Log Prob
                log_probs = self.classifier.feature_log_prob_[class_idx]
                contributions = X_dense * log_probs
            else:
                # Fallback: Just TF-IDF values
                contributions = X_dense
                
            # Find indices of non-zero entries sorted in descending order
            sorted_indices = np.argsort(contributions)[::-1]
            
            # Extract top 10 keywords that actually appeared in the resume (X_dense > 0)
            for idx in sorted_indices:
                if len(top_keywords) >= 10:
                    break
                if X_dense[idx] > 0 and contributions[idx] > 0:
                    word = self.feature_names[idx]
                    weight = float(contributions[idx])
                    top_keywords.append((word, weight))
                    
        except Exception as xai_err:
            print(f"XAI keyword extraction failed: {xai_err}")
            # Fallback: simply sort by TF-IDF value of words present in the resume
            sorted_tfidf_indices = np.argsort(X_dense)[::-1]
            for idx in sorted_tfidf_indices:
                if len(top_keywords) >= 10:
                    break
                if X_dense[idx] > 0:
                    top_keywords.append((self.feature_names[idx], float(X_dense[idx])))
                    
        return {
            "category": prediction,
            "confidence": round(confidence, 2),
            "top_keywords": top_keywords
        }
