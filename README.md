# 📊 Data Science Salary Analytics Dashboard

An interactive Streamlit web app for exploring global data-science compensation trends — built on the `ds_salaries` dataset. Combines data visualization, exploratory analytics, and a trained machine learning model in one dashboard.

🔗 **Live demo:** _add your link here after deploying_

## ✨ Features

- **KPI summary cards** — average/highest salary, total records, total countries
- **Interactive filters** — experience level, company location, company size
- **Search & export** — search job titles, download filtered results as CSV
- **6 analysis tabs:**
  - 📋 Overview & Data — searchable, exportable data table
  - 💼 Roles & Experience — top-paying job titles, salary by experience level
  - 📈 Trends Over Time — salary growth by year and seniority
  - 🌍 Global Geography — top countries + interactive world map
  - 🏢 Company & Environment — remote work distribution, salary by company size
  - 🤖 Salary Predictor — ML-powered salary estimate for a custom role profile

## 🛠️ Tech Stack

- **Framework:** Streamlit
- **Data processing:** Pandas
- **Visualization:** Plotly Express
- **Machine Learning:** scikit-learn (Random Forest Regressor)
- **Language:** Python 3.10+

## 🚀 Running Locally

\`\`\`bash
git clone <your-repo-url>
cd job-market-analytics-dashboard
pip install -r requirements.txt
streamlit run app.py
\`\`\`

The app opens at `http://localhost:8501`.

## 🤖 About the ML Model

The Salary Predictor tab trains a Random Forest Regressor on work year, experience level, employment type, job title, remote ratio, company location, and company size to predict salary in USD.

- Categorical features are one-hot encoded inside a scikit-learn Pipeline
- Evaluated on a held-out 20% test split, with R² and MAE shown transparently in the app
- Prediction "confidence range" comes from the standard deviation across the Random Forest's individual trees
- Trained on ~600 records — a solid educational demo rather than production-grade accuracy

## 📈 Possible Future Improvements

- Larger, more recent salary dataset
- Compare multiple ML models (Random Forest vs Gradient Boosting)
- Dockerize for one-command deployment

## 📄 License

Open source — free to use for learning and portfolio purposes.s