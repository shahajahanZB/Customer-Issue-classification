<!-- Project Video -->
<!-- ## 🎥 Project Demo

[![Service Sphere Demo](https://img.youtube.com/vi/BcdqpYm3tIk/0.jpg)](https://drive.google.com/file/d/1BcdqpYm3tIkvyUZ4fCE418QETPQKPSwg/view?usp=sharing)

> ⚠️ **Note:** There are many features that are not included in the demo video. To explore the full functionality, clone the repo and try it out yourself!

---

<div align="center" id="top"> 
  <img src="https://i.ibb.co/S6qMxwr/service-sphere.png" alt="Service Sphere" />
</div>
-->

<h1 align="center">Team API - QXH-23</h1>

<p align="center">
  <img alt="Top Language" src="https://img.shields.io/github/languages/top/shahajahanZB/TEAM-API-QXH-23?color=56BEB8">
  <img alt="Language Count" src="https://img.shields.io/github/languages/count/shahajahanZB/TEAM-API-QXH-23?color=56BEB8">
  <img alt="Repo Size" src="https://img.shields.io/github/repo-size/shahajahanZB/TEAM-API-QXH-23?color=56BEB8">
  <img alt="Issues" src="https://img.shields.io/github/issues/shahajahanZB/TEAM-API-QXH-23?color=56BEB8">
  <img alt="Forks" src="https://img.shields.io/github/forks/shahajahanZB/TEAM-API-QXH-23?color=56BEB8">
  <img alt="Stars" src="https://img.shields.io/github/stars/shahajahanZB/TEAM-API-QXH-23?color=56BEB8">
</p>

<h4 align="center"> 
	✨ Classio.ai — Where every issue finds its path  🛣️
</h4>

<!--
<h4 align="center">
  <a href="https://team-leveling.onrender.com/" target="_blank">🌐 Live Demo</a>
</h4>
-->

<hr>

<p align="center">
  <a href="#dart-introduction">Introduction</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-getting-started">Getting Started</a> &#xa0; | &#xa0;
  <a href="#lock-security">Security</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="#busts_in_silhouette-author">Author</a>
</p>

<br>

## :dart: Introduction ##

**Project name** is a full-stack platform that connects service providers with customers in need of their services. Our multi-client service marketplace allows businesses to showcase their services efficiently while providing an intuitive booking experience for customers. Whether you're offering home cleaning, beauty services, repairs, or professional consultations, Service Sphere provides the perfect environment to grow your business.

<!--
<div align="center">
  <img src="https://i.ibb.co/Yj5SXWZ/service-demo.gif" alt="Service Sphere Demo" width="600px" />
</div>
-->

## :sparkles: Features ##

### For Service Providers
✅ **User-Friendly Dashboard** - Manage your services, bookings, and customer interactions  
✅ **Service Creation & Management** - Multi-step service creation with detailed descriptions  
✅ **Dynamic Working Hours** - Set your availability with flexible scheduling options  
✅ **Booking Management** - Accept, reschedule, or cancel bookings with ease  
✅ **Performance Analytics** - Track your service performance and customer satisfaction  

### Platform Features
✅ **Responsive Design** - Mobile-friendly interface that works on all devices 📱  
✅ **Dark Mode Support** - Easy on the eyes during night browsing 🌙  
✅ **Advanced Search & Filters** - Find exactly what you're looking for  
✅ **Admin Panel** - Comprehensive management tools for platform administrators  
✅ **Security & Encryption** - Your data is always protected  

<!--
<div align="center">
  <img src="https://i.ibb.co/80kDGxL/features-showcase.png" alt="Features Showcase" width="700px" />
</div>
-->

## :rocket: Technologies ##

The following tools and technologies power Service Sphere:

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>
Additional tools:

- Flask - Lightweight WSGI web application framework
- Hugging Face Transformers - Load model and tokenizers for NLP models
- DistilBERT - Distilled version of BERT for efficient classification of labels
- Twilio - Communication APIs for whatsapp message retrivel

## :white_check_mark: Requirements ##

Before starting, you need to have:

- [Git](https://git-scm.com)
- [Python](https://www.python.org/) (3.8 or higher)
- Basic knowledge of Flask and web development

## :checkered_flag: Getting Started ##

#### 🔹 Step 1: Clone the Repository

```bash
git clone [https://github.com/shahajahanZB/TEAM-API-QXH-23.git]
cd "TEAM-API-QXH-23"
```

---

#### 🔹 Step 2: Create and Activate a Virtual Environment

```bash
python -m venv venv
```

```bash
# On macOS/Linux
source venv/bin/activate
```

```bash
# On Windows
venv\Scripts\activate
```

---

#### 🔹 Step 3: Install Project Dependencies

```bash
pip install -r requirements.txt
```

---
<!--
#### 🔹 Step 4: Database Setup

Option 1: MySQL (Recommended for Production)

- Create a MySQL database.
- Update `settings.py` with your database credentials under the `DATABASES` section.

Option 2: SQLite (Default for Development)

- No additional configuration needed. SQLite will be used automatically.

---

#### 🔹 Step 5: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

#### 🔹 Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

---
-->
#### 🔹 Step 4: Run the Development Server

```bash
python manage.py runserver
```

---

#### 🔹 Step 5: Access the Application

- 🌐 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🔐 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

<!--
Let me know if you want to add **Docker support**, `.env` setup, or **troubleshooting tips**!

## :lock: Security ##

This project requires a security key that is not included in the repository. If you would like to try the full functionality, please contact the project maintainer for access to the security key.

### Environment Variables

Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your_secret_key_here
DEBUG=True  # Set to False in production
DATABASE_URL=your_database_connection_string
```

## :eyes: Project Demo ##

<div align="center">
  <a href="https://team-leveling.onrender.com/" target="_blank">
    <img src="https://i.ibb.co/X5Kj9zJ/live-demo-button.png" alt="Live Demo Button" width="300px" />
  </a>
</div>
-->

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.

## :busts_in_silhouette: Author ##

Made with :heart: by <a href="https://github.com/shahajahanZB" target="_blank">Team API</a>

&#xa0;

<a href="#top">Back to top</a>
