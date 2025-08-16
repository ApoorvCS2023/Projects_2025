# Projects_2025
In this repository I'll be showcasing my newly developed project, related to AI/ML and Data
# AI Job Description & Resume Matcher

This project analyzes a **job description** and a **resume**, extracts relevant skills, and calculates a **match score** along with the skills you already have and those you might need to learn.  
Built with Hugging Face NLP models, sentence embeddings, and experiment tracking using Weights & Biases (W&B).

---

## 🚀 Features
- **Skill Extraction** from both JD and resume using Sentence Transformers.
- **Semantic Matching** with cosine similarity (plus fuzzy matching for typos).
- **Match Report** with overlap, missing skills, and coverage percentage.
- **Experiment Tracking** in W&B for reproducible results.
- **Ready for Deployment** with AWS (Lambda + API Gateway + Amazon Comprehend integration planned).

---

## 🛠 Tech Stack
- **Python** – Core language.
- **Hugging Face Transformers & Sentence-Transformers** – NLP and embeddings.
- **PyTorch** – Model backend.
- **Weights & Biases** – Experiment tracking and logging.
- **RapidFuzz** – Fuzzy matching for skill variations.
- **Google Colab / Jupyter Notebook** – Development environment.

---

## 📂 How to Run in Google Colab
1. **Open the Notebook in Colab**
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ApoorvCS2023/Projects_2025/blob/main/jd_resume_matcher_clean.ipynb)


3. **Install dependencies**  
   Run the first cell to install required libraries.

4. **Replace sample texts**  
   - Paste a real job description into `job_description_text`.
   - Paste your resume text into `resume_text`.

5. **Run all cells**  
   Get your skill match report instantly.

---

## 📊 Sample Output
[!Match_Score_Screenshot]<img width="1610" height="214" alt="Screenshot 2025-08-15 215705" src="https://github.com/user-attachments/assets/ff9afba7-931c-4855-a743-1053a79d6b25" />


---

## 📌 Future Improvements
- AWS API deployment with Lambda + API Gateway.
- Amazon Comprehend integration for skill extraction.
- PDF parsing for resumes and JDs.
- Extended skill vocabulary and auto-updates.

---

## 🤝 Contributing
Pull requests and suggestions are welcome!  
If you find an issue, open one in the Issues tab.

---

## 📜 License
This project is open-source under the MIT License.
