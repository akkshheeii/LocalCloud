
<div align="center">

### LocalCloud
Upload • Download • Organize • Analyze


</div>


### `>About The Project`
```LocalCloud is a lightweight cloud storage platform inspired by Google Drive. It allows users to securely upload
manage, organize, download and share files locally without relying on any third-party cloud services.
The project focuses on **clean backend architecture**, **modular Flask development**, and **beginner-friendly code**
making it an excellent learning project for Flask and full-stack web development.
```

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)  

</div>

### `> ScreenShots`


```
> Login Page
Simple modern authentication interface.
```

![Login](docs/Screenshot%202026-06-30%20172149.png)

---
 
```
> Dashboard
Upload files, search and manage them.
```

![Dashboard](docs/Screenshot%202026-06-30%20172227.png)

---

```
> Analytics Dashboard
Storage statistics and visual analytics.
```

![Analytics](docs/Screenshot%202026-06-30%20172241.png)

---

```
> Storage Insights
Largest, smallest and average file size.
```

![Insights](docs/Screenshot%202026-06-30%20172405.png)

---

```
> Recent Activity
Displays latest uploaded files.
```

![Activity](docs/Screenshot%202026-06-30%20172416.png)

---



---

### `> Project Structure`

```
LocalCloud/

│
├── app.py
├── main.py
├── requirements.txt
│
├── instance/
│      database.db
│
├── uploads/
│      user-folders
│
├── LocalCloud/
│      │
│      ├── __init__.py
│      ├── auth.py
│      ├── views.py
│      ├── models.py
│      │
│      ├── templates/
│      │
│      └── static/
│
└── README.md
```

```bash
python main.py
```

### `> Database Models`

> User

```
id
username
password
storage_limit
storage_used
```

---

> File

```
id
filename
filepath
file_size
filetype
upload_date
user_id
```


Built with ❤️ By Akshay !
