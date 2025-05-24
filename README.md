
# Render PaaS Projects

This repository contains 5 individual Python Flask apps designed for deployment on [Render.com](https://render.com). Each app is in its own folder and can be deployed independently as a web service.

## 🧩 Project Structure

```
render_paass_projects/
├── even_numbers_app/
├── matrix_multiplication_app/
├── user_validation_db_app/
├── nth_largest_number_app/
└── user_info_storage_app/
```

Each folder contains:
- `app.py` – Main Flask application
- `index.html` – Simple UI template
- `requirements.txt` – Python dependencies
- `render.yaml` – Render deployment configuration

---

## 🚀 Deployment Guide

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/render-paass-projects.git
cd render-paass-projects
```

### 2. Deploy on Render
For each app:
1. Go to [https://render.com](https://render.com) → **New → Web Service**
2. Connect this GitHub repo
3. In "Advanced", set the **Root Directory** to one of the folders (e.g. `even_numbers_app`)
4. Use:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Create Web Service**

Repeat for all 5 apps.

---

## 📦 Included Projects

| App Folder | Description |
|------------|-------------|
| `even_numbers_app` | Generates N even numbers and displays them |
| `matrix_multiplication_app` | Multiplies two matrices and shows the result |
| `user_validation_db_app` | Validates user with MySQL credentials |
| `nth_largest_number_app` | Displays the Nth largest number from a list |
| `user_info_storage_app` | Stores and validates user info using a database |

---

## 🛠 Technologies Used

- Python 3
- Flask
- Gunicorn (for production WSGI server)
- HTML (for basic UI)
- Render PaaS for hosting

---

## 📬 Contact
Feel free to reach out if you need help deploying or running the projects.
