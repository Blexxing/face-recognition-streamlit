# Streamlit Face Recognition Demo

Simple Streamlit app using `face_recognition` to register known faces and recognize faces in uploaded images.

## How to run locally
```
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Push to GitHub
```
git init
git add .
git commit -m "Initial Streamlit face recognition app"
git remote add origin YOUR_REPO_URL
git branch -M main
git push -u origin main
```

## Deploy on Streamlit Cloud
Go to https://share.streamlit.io/ → New App → Select repo → Choose `app.py`
