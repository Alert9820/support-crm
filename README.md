# 🎫 Support CRM

A fully functional Customer Support Ticketing System built with FastAPI, MongoDB, and Tailwind CSS. Deployed live on Render.

## 🔗 Live Demo
[https://support-crm-cuvt.onrender.com](https://support-crm-cuvt.onrender.com)

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI
- **Database:** MongoDB Atlas
- **Frontend:** HTML, Tailwind CSS, Vanilla JS
- **Deployment:** Render

## ✨ Features
- Create support tickets with customer info
- List all tickets with clean UI
- Search across name, email, ID, description
- Filter by status — Open, In Progress, Closed
- View ticket details and update status
- Add internal notes to tickets

## 📁 Project Structure
```
support-crm/
├── main.py          # FastAPI app + all routes
├── database.py      # MongoDB connection
├── models.py        # Pydantic schemas
├── requirements.txt
├── .env.example
├── .gitignore
└── frontend/
    └── index.html
```

## ⚙️ Local Setup

1. Clone the repo
```bash
git clone https://github.com/yourusername/support-crm.git
cd support-crm
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
```bash
cp .env.example .env
```
Add your MongoDB URI in `.env`:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

4. Run the app
```bash
uvicorn main:app --reload
```

5. Open browser at `http://localhost:8000`

## 🚀 Deployment
Deployed on Render with MongoDB Atlas as cloud database.

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment Variable:** `MONGO_URI`
