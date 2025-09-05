# Django-Vectorizer-Web
_A portfolio project by Tobias – Remote Python/Django Developer_
---

## 👨‍💻 About Me
Hi, I’m **Tobias Chen**, a Python/Django developer focused on building scalable, production-ready web applications.  
I specialize in **Machine Learning, Data Science, and backend engineering, API design, and cloud deployments**. My work emphasizes **clean architecture, CI/CD automation, and maintainability** – essential skills for remote-first development teams.

- 🌍 Open to **remote opportunities across Europe/Australia/Asia/North America**  
- 💼 Strong experience with **Python, Django, REST APIs, Docker, PostgreSQL**  
- ⚙️ Familiar with **async processing, Celery, Redis, and modern CI/CD pipelines, AZure**  
- 🎨 Interested in projects combining **web apps + image processing + automation**  
- 🔗 [LinkedIn](https://www.linkedin.com/in/jiawei-chen-4095802a9/) | [GitHub](https://github.com/JackyFuHk)  
- 📧 tobiaschannel1999@gmail.com  

---


## Introduction
A **web-based Django application** that converts bitmap images (PNG, JPG, BMP) into **scalable vector graphics (SVG)**.  
This tool is designed for developers, designers, and researchers who need fast, customizable image vectorization.

---

### 🧩 Key Skills Demonstrated
- **Django Architecture**: Cleanly separated apps (`converter`, `vectorizer`, `api`) with clear responsibilities.
- **Image Processing**: Implemented bitmap → SVG conversion pipeline (extensible with custom algorithms).
- **API Development**: RESTful endpoints to integrate vectorization into other platforms.
- **Database Design**: PostgreSQL with migrations, indexing, and optional async job queue.
- **Scalability**: Dockerized setup, production-ready with Gunicorn + Nginx.
- **DevOps Practices**:
  - CI/CD pipeline with **GitHub Actions**
  - Code quality checks (`flake8`, `black`, `mypy`)
  - Unit/integration tests with `pytest`
- **Remote-Friendly Workflow**: Documentation, Docker onboarding, `.env` configuration for team reproducibility.


---

## 🛠️ Tech Stack
- **Backend Framework**: Django 5.x (Python 3.11+)
- **Database**: PostgreSQL (production), SQLite (local dev)
- **Task Queue**: Celery + Redis (for async image processing)
- **Testing**: pytest + Django TestCase
- **Linting & Formatting**: black, flake8, isort, mypy
- **CI/CD**: GitHub Actions with automated testing & linting
- **Deployment**: Docker, Docker Compose, Kubernetes-ready
- **Authentication**: Django Allauth / JWT (optional for API)

---
## 📂 How to Run Locally
## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/JackyFuHk/Django-Vectorizer-Web.git

# 2. Enter the project directory
cd Django-Vectorizer-Web

# 3. Create and activate a virtual environment
python3 -m venv venv && source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply database migrations
python manage.py migrate

# 6. Run the development server
python manage.py runserver




## 📂 Project Structure
```bash
+---.vscode
+---algorithm
|   +---pngtosvg
+---core
|   +---management
|   +---migrations
+---djecommerce
|   +---settings
+---locale
|   +---en
|   +---zh_Hans
|   \---zh_Hant
+---log
+---media_root
|   +---models
|   +---model_ass
+---static_in_env
|   +---client_svg
|   +---css
|   |   +---addons
|   +---font
|   +---fonts
|   +---img
|   +---js
|   \---scss
+---static_root
|   +---admin
|   +---css
|   +---debug_toolbar
|   +---flags
|   +---font
|   +---fonts
|   +---img
|   +---js
|   \---scss
\---templates
    +---account
    +---blog
    +---openid
    +---products
    \---socialaccount