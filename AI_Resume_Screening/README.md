# AI Resume Screening Assistant using Machine Learning and Agentic AI

This is a comprehensive, production-quality college mini-project that demonstrates the integration of **Traditional Supervised Machine Learning** and **Agentic Generative AI** to solve real-world talent acquisition and career planning challenges.

---

## 📌 Problem Statement & Objectives

### Problem Statement
Modern recruitment processes are overwhelmed by hundreds of candidate applications. Traditional keyword-based Applicant Tracking Systems (ATS) are rigid, often filtering out qualified candidates due to minor formatting discrepancies. Conversely, manual screening is slow, error-prone, and fails to provide actionable feedback or developmental roadmaps to candidates who fall slightly short of job requirements.

### Project Objectives
1. **Automated Domain Classification**: Parse text from PDF resumes and utilize a trained Machine Learning model to accurately classify the candidate's professional field.
2. **Explainable AI (XAI)**: Calculate and visualize the specific vocabulary keywords that mathematically drove the ML prediction to ensure model transparency.
3. **Advanced Profile Parsing**: Programmatically extract structural profile segments (Contact Details, Skills, Education, Experience, Projects, Certifications) using pattern matching and keyword dictionaries.
4. **Hybrid Talent Scoring**: Compute a *Resume Quality Score* (measuring document completeness) and an *ATS Alignment Score* (measuring target role skill matching density).
5. **Multi-Agent Careers Guidance**: Orchestrate four specialized Gemini-powered agents sequentially to review the resume, outline skill gaps, chart a 30-day learning calendar, and compile custom interview questions.
6. **Talent Dossier Export**: Generate downloadable, professional PDF reports summarizing all screening metrics and AI insights.

---

## 🏗️ System Architecture & Workflow

### Technical Workflow Diagram
```
        Upload Resume PDF
               │
               ▼
      [utils/pdf_reader.py]  ──► Extracts plain text with error handling
               │
               ▼
     [utils/resume_parser.py] ──► Extracts Contact details, Skills, Sections
               │
               ▼
    [ml/preprocessing.py]    ──► Normalization, lowecasing, regex, stopwords
               │
               ▼
      [models/tfidf.pkl]     ──► Vectorizes text to sparse feature space
               │
               ▼
 [models/resume_classifier.pkl] ──► Logistic Regression category prediction
               │
               ▼
  [utils/category_mapper.py] ──► Maps raw category labels to clean titles
               │
               ▼
    [Programmatic Scoring]   ──► Calculates Resume Score & ATS Match Score
               │
               ▼
   ┌───────────┴──────────────────────────────────────────────────────┐
   │                  SEQUENTIAL AI AGENTS (Gemini API)               │
   ├──────────────────────────────────────────────────────────────────┤
   │ 🤖 1. ResumeReviewerAgent       ──► Strengths, Weaknesses, Tips  │
   │ 🤖 2. SkillRecommendationAgent ──► Gap Analysis, Courses, Certs  │
   │ 🤖 3. RoadmapGeneratorAgent     ──► 30-Day Calendar Calendar     │
   │ 🤖 4. InterviewPrepAgent        ──► Personalizes offline Q&A     │
   └───────────┬──────────────────────────────────────────────────────┘
               │
               ▼
      Streamlit Interface    ──► Interactive KPI Cards, Plotly analytics,
     & PDF Dossier Export        and fpdf2 Report Downloader
```

---

## 🛠️ Technology Stack & Libraries

* **Core Language**: Python 3.11+
* **User Interface**: Streamlit (Responsive layouts & state caching via `st.session_state`)
* **Machine Learning Model**: Scikit-Learn (`TfidfVectorizer` + `LogisticRegression` primary model)
* **LLM Engine**: Google Gemini API (`google-generativeai` package running `gemini-2.5-flash`)
* **PDF Processing**: PyPDF2 (Binary text stream parsing)
* **Report Compilation**: fpdf2 (Structured PDF compiling with character sanitization)
* **Data & Math Operations**: Pandas, NumPy, Joblib
* **Data Visualization**: Plotly Express & Plotly Graph Objects

---

## 📁 Project Folder Structure

```
AI_Resume_Screening/
├── app.py                      # Main entry point (Config, CSS & State Init)
├── .env                        # Local secrets storage (GEMINI_API_KEY)
├── requirements.txt            # Python dependencies configuration
├── README.md                   # Comprehensive project documentation and viva guide
│
├── data/
│     UpdatedResumeDataSet.csv  # Sourced Kaggle resume classification dataset
│     skills_dataset.csv        # Pre-seeded category skills database
│     projects_dataset.csv      # Mapped project recommendations database
│     interview_questions.csv   # Target interview questions database
│
├── models/
│     resume_classifier.pkl     # Trained Logistic Regression classifier
│     tfidf.pkl                 # Fitted TF-IDF Vectorizer
│
├── ml/
│     __init__.py
│     preprocessing.py          # Case normalization & stopword filtering logic
│     train_model.py            # Model comparison training script
│     predictor.py              # Prediction pipeline and XAI keyword calculator
│
├── agents/
│     __init__.py
│     resume_agent.py           # Strengths, weaknesses, and ATS format suggestions
│     skill_agent.py            # Course recommendations and credential maps
│     roadmap_agent.py          # Structured 30-day curriculum scheduler
│     interview_agent.py        # Custom mock interview personalization
│
├── utils/
│     __init__.py
│     pdf_reader.py             # Binary stream text parsing & exception catcher
│     resume_parser.py          # Profile segment extractor (Regex/NLP-lookup)
│     category_mapper.py        # Translates raw model outputs to clean labels
│     prompts.py                # Prompt template isolation repository
│     gemini_client.py          # Gemini API wrapper with error managers
│     pdf_report_generator.py   # Compiles candidate dossier using fpdf2
│
└── assets/                     # Preserves design templates/media assets
```

---

## 📊 Machine Learning Model Comparison

During the model training step (`ml/train_model.py`), both **Logistic Regression** and **Multinomial Naive Bayes** were trained and evaluated on an 80/20 train/test split. The metrics achieved:

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | **99.48%** | **99.56%** | **99.48%** | **99.47%** | **Selected & Saved** |
| **Multinomial Naive Bayes** | 92.23% | 95.54% | 92.23% | 92.02% | Baseline |

*Logistic Regression was automatically selected as the winning model and saved to `models/resume_classifier.pkl`.*

---

## 🚀 Installation & How to Run

### 1. Clone or Navigate to the Workspace Directory
Ensure you are in the parent directory containing the `AI_Resume_Screening/` folder.

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r AI_Resume_Screening/requirements.txt
```

### 4. Configure Secrets
Create or edit the `.env` file inside the `AI_Resume_Screening/` directory:
```env
GEMINI_API_KEY=your_actual_google_gemini_api_key
```

### 5. Launch the Streamlit Interface
Run the application using:
```bash
streamlit run AI_Resume_Screening/app.py
```
Open the local URL displayed in your terminal (usually `http://localhost:8501`).

---

## 🎓 College Viva Questions & Answers

### Q1: Why did you choose Logistic Regression over Naive Bayes for this project?
* **Answer**: We trained and compared both algorithms. Logistic Regression achieved an F1-Score of **99.47%**, outperforming Multinomial Naive Bayes, which scored **92.02%**.
* Naive Bayes operates on the assumption of strong conditional independence between features, which is mathematically violated in natural language text (e.g., terms like "Machine" and "Learning" appear together). Logistic Regression is a discriminative classifier that fits weights (coefficients) to maximize log-likelihood, capturing overlapping feature dependencies more effectively on the TF-IDF representation.

### Q2: How did you implement Explainable AI (XAI) in your model prediction?
* **Answer**: For any prediction, we calculate the feature contribution scores.
* Mathematically, for the predicted class $c$, we take the element-wise product of the TF-IDF vector of the input resume $X_{\text{tfidf}}$ and the model coefficients $W_{c}$ for that class:
  $$\text{Contribution}_i = X_{\text{tfidf}, i} \times W_{c, i}$$
  By sorting these values in descending order, we extract the top 10 features (words) that had the highest positive influence on the classification decision. This explains *why* the model made its decision.

### Q3: Explain how your Agentic AI workflow is coordinated.
* **Answer**: We did not use heavy agent frameworks like CrewAI or LangGraph to keep the architecture light, modular, and easy to explain.
* Instead, we implemented each agent as an independent Python class (`ResumeReviewerAgent`, `SkillRecommendationAgent`, etc.). The main Streamlit application acts as the coordinator, passing inputs sequentially from one agent to the next using `st.session_state` to cache results. This avoids overhead and guarantees deterministic sequence execution.

### Q4: How are the Resume Score and ATS Score calculated?
* **Answer**: We use a **Hybrid Scoring System** combining structural rules and vocabulary overlap:
  1. **Resume Score**: Calculated programmatically based on document section presence (Contact Details = 15, Education = 15, Experience = 20, Projects = 20, Skills = 20, Certifications = 10).
  2. **ATS Score**: Calculated using a combination of contact details completeness (10), section presence (40), and the **Skill Match Ratio** (40) which measures the percentage overlap between the candidate's skills and the required skills defined in `skills_dataset.csv` for the predicted role.

### Q5: How did you handle encoding errors when compiling text outputs into the PDF?
* **Answer**: Standard PDF fonts (like Helvetica) in `fpdf2` only support Latin-1 characters. Resume texts and Gemini markdown outputs often contain non-Latin1 symbols (e.g., bullet points `•`, smart quotes `“` `”`, checkmarks `✓`).
* We implemented `clean_for_pdf()`, which maps Unicode characters to their ASCII/Latin-1 equivalents (e.g., replacing smart quotes with standard double quotes, checkmarks with `[x]`, bullets with hyphens), and encodes the text using `latin-1` with the `ignore` flag. This prevents runtime compile crashes.

---

## 🔮 Future Enhancements

1. **OCR Support**: Integrate Tesseract OCR to parse scanned or image-based resume PDFs.
2. **Multilingual Support**: Extend the TF-IDF Vectorizer and Agent prompts to support resumes in multiple languages.
3. **Advanced Models**: Incorporate fine-tuned BERT/DistilBERT classifiers as alternatives in the training pipeline.
4. **Mock Interview Audio**: Add text-to-speech (TTS) and speech-to-text (STT) features for spoken mock interviews.

---

## 📚 References

1. *Kaggle Resume Dataset for Resume Classification*: [Kaggle Dataset Link](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset)
2. *Scikit-Learn documentation for Logistic Regression*: [Scikit-Learn Docs](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
3. *Google Gemini API Documentation for developer integrations*: [Google AI Docs](https://ai.google.dev/docs)
4. *FPDF2 documentation for generating document buffers in Python*: [FPDF2 Docs](https://pyfpdf.github.io/fpdf2/)
