# 📝 SEO-Friendly Blog Project

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.3-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

این پروژه یک **بلاگ مدرن و سئو-محور** است که به‌گونه‌ای طراحی شده تا بتوان آن را به‌راحتی برای موتورهای جستجو (SEO) بهینه‌سازی کرد.  
ساختار پروژه به شکلی است که توسعه‌پذیر، تمیز و مناسب پروژه‌های واقعی باشد.

This project is a **modern, SEO-friendly blog** designed to be easily optimized for search engines.  
The structure is clean, scalable, and suitable for real-world projects.

---

## 🚀 Features / ویژگی‌ها

- ✅ ساختار مناسب برای SEO / SEO-friendly structure
- ✅ URL های خوانا و استاندارد / Clean and standard URLs
- ✅ امکان افزودن meta tags (title, description) / Ability to add meta tags (title, description)
- ✅ آماده برای توسعه و شخصی‌سازی / Ready for customization and extension
- ✅ معماری تمیز و قابل نگهداری / Clean and maintainable architecture
- ✅ مناسب برای بلاگ‌های شخصی یا حرفه‌ای / Suitable for personal or professional blogs

---

## 🧠 SEO Considerations / نکات سئو

- استفاده از ساختار مناسب صفحات / Proper page structure
- امکان تعریف Meta Title و Meta Description / Ability to define Meta Title and Meta Description
- محتوای قابل ایندکس توسط موتورهای جستجو / Indexable content for search engines
- آماده برای پیاده‌سازی Sitemap و Robots.txt / Ready for Sitemap and Robots.txt
- ساختار مناسب برای لینک‌سازی داخلی / Proper internal linking structure

---

## 🛠 Technologies Used / تکنولوژی‌های استفاده‌شده

- Backend: Django / Django Rest Framework
- Database: SQLite / PostgreSQL
- Authentication: JWT
- Frontend: HTML, CSS, JavaScript (Optional: React/Vue)
- Version Control: Git & GitHub
- SEO Tools: Django SEO Framework, Meta Tags

---

## ⚙️ Installation & Setup / نصب و راه‌اندازی

```bash
git clone git@github.com:melikatavakoli/blog.git
cd blog

# نصب محیط مجازی / Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

# نصب وابستگی‌ها / Install dependencies
pip install -r requirements.txt

# اعمال مایگریشن‌ها / Apply migrations
python manage.py migrate

# ایجاد سوپر یوزر برای مدیریت / Create superuser for admin
python manage.py createsuperuser

# اجرای سرور توسعه / Run development server
python manage.py runserver
