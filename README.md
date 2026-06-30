# 📊 Data Science Salary Analytics Dashboard

An interactive **Streamlit** web app for exploring global data-science compensation — built on the popular [`ds_salaries`](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries) dataset. It combines data visualization, exploratory analytics, and a trained **machine learning model** in a single polished dashboard.

🔗 **Live demo:** _add your Streamlit Community Cloud link here after deploying_

---

## ✨ Features

- **KPI summary cards** — average/highest salary, total records, total countries (recalculated live as filters change)
- **Interactive filters** — experience level, company location, company size
- **Search & export** — search job titles in the data table and download the filtered results as CSV
- **6 analysis tabs:**
  | Tab | What it shows |
  |---|---|
  | 📋 Overview & Data | Searchable/exportable raw data table |
  | 💼 Roles & Experience | Top-paying job titles, salary by experience level |
  | 📈 Trends Over Time | Salary growth by year, broken down by seniority |
  | 🌍 Global Geography | Top-paying countries + an interactive world choropleth map |
  | 🏢 Company & Environment | Remote work distribution, salary by company size |
  | 🤖 Salary Predictor | **ML-powered** salary estimate for a custom role profile |
- **Machine Learning** — a `scikit-learn` Random Forest Regressor trained live on the dataset, with reported R² / MAE and an uncertainty range on each prediction (derived from variance across the forest's trees)

---

## 🛠️ Tech Stack

- **Frontend / App framework:** [Streamlit](https://streamlit.io)
- **Data processing:** Pandas
- **Visualization:** Plotly Express
- **Machine Learning:** scikit-learn (`RandomForestRegressor`, `OneHotEncoder`, `Pipeline`)
- **Language:** Python 3.10+

---

## 📁 Project Structure

```
job-market-analytics-dashboard/
├── app.py                  # Main Streamlit app (UI/layout only)
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml         # Theme + browser settings
├── data/
│   └── ds_salaries.csv     # Dataset
└── utils/
    ├── data_loader.py      # Loading, cleaning, mapping, filtering
    ├── styling.py          # CSS, KPI cards, Plotly theme helper
    └── ml_model.py          # Model training + prediction logic
```

The app is intentionally split into small, single-responsibility modules rather than one large script — this keeps `app.py` focused on layout, and makes the data/ML logic independently testable.

---

## 🚀 Running Locally

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd job-market-analytics-dashboard

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this project to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"**, select your repo/branch, and set the main file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically and gives you a public URL like:
   ```
   https://your-app-name.streamlit.app
   ```
5. Add that link to the top of this README and to your resume/GitHub profile.

---

## 🤖 About the ML Model

The "Salary Predictor" tab trains a `RandomForestRegressor` on `work_year`, `experience_level`, `employment_type`, `job_title`, `remote_ratio`, `company_location`, and `company_size` to predict `salary_in_usd`.

- Categorical features are one-hot encoded inside a scikit-learn `Pipeline` (no manual leakage-prone preprocessing).
- The model is evaluated on a held-out 20% test split — its R² and MAE are shown transparently in the app, not hidden.
- Rare job titles (fewer than 5 occurrences) are bucketed into `"Other"` to avoid noisy, overfit one-hot columns.
- Prediction "uncertainty" is the standard deviation of predictions across the forest's individual trees — a simple, legitimate way to communicate confidence instead of a single falsely-precise number.
- The model is trained on **~600 records**, so treat its accuracy as a solid educational/demo benchmark rather than production-grade — accuracy would scale with a larger dataset.

---

## 📈 Possible Future Improvements

- Swap in a larger, more recent salary dataset
- Add model comparison (Random Forest vs. Gradient Boosting vs. Linear Regression)
- User authentication + saved filter presets
- Dockerize for one-command deployment anywhere

---

## 📄 License

This project is open source and available for learning/personal portfolio use.
