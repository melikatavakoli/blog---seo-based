# 📝 SEO-Friendly Blog Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.3-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A **modern, SEO-focused blog platform** built with Django, designed to be clean, flexible, and easy to optimize for search engines.

This project was created with real-world usage in mind — whether for a personal blog, a content platform, or as a solid foundation for larger publishing systems.

---

## ✨ Key Features
- 🔍 SEO-friendly structure out of the box
- 🔗 Clean, readable, and standard URLs
- 🏷 Support for meta tags (title & description)
- 🧩 Easy to extend and customize
- 🧼 Clean and maintainable project architecture
- 🧑‍💻 Suitable for both personal and professional blogs

---

## 🧠 SEO Considerations
This project takes SEO seriously and provides a strong base for further optimization:

- Proper HTML and page structure
- Customizable Meta Title & Meta Description
- Search-engine indexable content
- Ready for Sitemap.xml and robots.txt
- Logical internal linking structure

---

## 🛠 Tech Stack
- **Backend:** Django / Django REST Framework
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT
- **Version Control:** Git & GitHub
- **SEO Tools:** Django SEO utilities, Meta Tags

---

## ⚙️ Installation & Setup

```bash
git clone git@github.com:melikatavakoli/blog.git
cd blog

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
