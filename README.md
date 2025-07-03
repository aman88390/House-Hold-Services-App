# 🏡 House-Hold Services App

A full-stack web application for booking and managing household services like cleaning, plumbing, and electrical repairs. Built with a **Vue.js frontend** and a **Python backend** using **Celery + Celery Beat** for background task scheduling and processing.

## 🚀 Features

- Book services like cleaning, plumbing, electrical, etc.  
- Schedule services by selecting preferred time/date  
- Background task execution using Celery  
- Periodic task scheduling with Celery Beat  
- Admin data export via CSV  
- Responsive Vue.js frontend with Vite

## 🛠️ Tech Stack

Frontend: Vue.js, Vite  
Backend: Python (Flask)  
Task Queue: Celery  
Scheduler: Celery Beat  
Database: SQLite  
Exports: Custom CSV exporter

## 📥 Getting Started

### 🔽 Clone the Repository

```
git clone https://github.com/aman88390/House-Hold-Services-App.git
cd House-Hold-Services-App
```


## 🔧 Backend Setup

1. Navigate to the backend folder:  
   `cd backend`  
2. Create and activate a virtual environment:  
   `python3 -m venv venv`  
   `source venv/bin/activate` (or `.\venv\Scripts\activate` on Windows)  
3. Install dependencies:  
   `pip install -r requirements.txt`  
4. Run the backend app:  
    `python main.py`

## ⏱ Start Celery with Beat

Run the following command from the backend directory:  
`celery -A main.celery_app worker --loglevel=info -B`  
(Note: Use separate processes for worker and beat in production)

## 💻 Frontend Setup

1. Navigate to the frontend folder:  
   `cd frontend`  
2. Install dependencies:  
   `npm install`  
3. Run the dev server:  
   `npm run dev`  
Frontend will run at: http://localhost:5173

## 🤝 Contributing

Contributions are welcome!  
Fork this repo, create a branch, make changes, and open a pull request.

## 🪪 License

This project is licensed under the MIT License.  
See the LICENSE file for details.

## 👤 Author

**Aman Yadav**  
GitHub: [https://github.com/aman88390](https://github.com/aman88390)
