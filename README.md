# Simple Social

**Simple Social** is a modern, full-stack social media application built with **FastAPI** and **Streamlit**. It features a high-end, animated user interface, secure authentication, and real-time media sharing capabilities.

![Simple Social Banner](https://via.placeholder.com/1200x400?text=Simple+Social+Preview) 
*(Note: Replace with an actual screenshot of your animated homepage)*

## ✨ Features

- **Modern & Fluid UI**: Custom-designed frontend with a sophisticated, liquid-like animated gradient background and glassmorphism effects.
- **Secure Authentication**: Robust JWT-based system for User Registration, Login, and Session Management using `fastapi-users`.
- **Media Sharing**: Upload and share images and short videos seamlessly.
- **Cloud Storage Integration**: Optimized media handling and delivery via **ImageKit.io**.
- **Interactive Feed**: Real-time social feed with caption overlays and owner-specific controls (delete functionality).
- **Responsive Design**: Mobile-friendly layout adapted for various screen sizes.

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: SQLite with SQLAlchemy (AsyncIO)
- **Authentication**: `fastapi-users`
- **Media Storage**: `imagekitio`

### Frontend
- **Framework**: [Streamlit](https://streamlit.io/)
- **Styling**: Custom CSS3 Animations, Flexbox grid
- **Communication**: `requests` for REST API consumption

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- An ImageKit.io account (for media storage)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-project-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: Ensure `streamlit`, `requests`, `fastapi`, `uvicorn`, `sqlalchemy`, `fastapi-users`, `imagekitio` are installed.*

4.  **Configuration:**
    Create a `.env` file or configure your secrets in `app/users.py` and `app/app.py`.
    *Important: Update the ImageKit credentials in `app/app.py` with your own keys.*

### Running the Application

You need to run both the Backend and Frontend servers.

**1. Start the Backend API:**
Open a terminal and run:
```bash
python main.py
```
*The API will start at `http://localhost:8000`*

**2. Start the Frontend UI:**
Open a second terminal and run:
```bash
python -m streamlit run app/frontend.py
```
*The App will open in your browser at `http://localhost:8501`*

## 📂 Project Structure

```
├── app/
│   ├── app.py          # Main FastAPI application and endpoints
│   ├── db.py           # Database models and session configuration
│   ├── frontend.py     # Streamlit frontend application
│   ├── schemas.py      # Pydantic models for data validation
│   └── users.py        # User management and authentication logic
├── main.py             # Entry point for the backend server
├── pyproject.toml      # Project dependencies and configuration
└── README.md           # Project documentation
```

## 🛡️ License

This project is open-source and available under the [MIT License](LICENSE).

---
**Developed with ❤️ by [Your Name]**