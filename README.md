
---

````markdown
# QuizMaster 🎓🧠  
**Design Quizzes. Build Groups. Grow Together.**

[![QuizMaster Screenshot](https://i.postimg.cc/d0xd5v8b/Screenshot-2025-05-02-at-12-24-56-PM.png)](https://postimg.cc/8FLjC2X4)


QuizMaster is a Django-powered quiz platform designed to make learning interactive and fun. Whether you're an educator, student, or quiz enthusiast, QuizMaster helps you create quizzes, form groups, invite friends or students, and track progress — all from one easy-to-use application.

---

## 🚀 Features

### ✅ Quiz Creation & Management
- Create **subjects**, **categories**, and **quizzes**.
- Add questions with options, correct answers, time limits, and more.
- Use "Save" or "Save and New" to streamline question input.

### 📊 Bulk Question Upload (Excel)
- Download a ready-to-use **Excel template**.
- Fill in your quiz content offline.
- Upload and save questions to the system with a few clicks.

### 🤖 AI-Powered Quiz Generator
- Generate questions instantly using **Google Gemini AI**.
- Select your subject, topic, or language — AI does the rest.
- Edit and review before saving or sharing the quiz.

### 👥 Group Management
- Create groups and invite **friends** or **students**.
- Assign quizzes to groups and track participation and results.
- One quiz attempt per user per group ensures fair results.
- Admins can monitor group activity and quiz completion.

---

## 🛠️ Tech Stack

- **Backend**: Python, Django, Django REST Framework  
- **Frontend**: HTMX, Tailwind CSS, Bootstrap  
- **Database**: PostgreSQL  
- **Authentication**: Django-Allauth  
- **Excel Integration**: Openpyxl  
- **AI Integration**: Google Gemini AI  

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/quizmaster.git
   cd quizmaster
````

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

---

## 👤 Team

* **Dirk** – Backend Developer
* **Essa** – Backend Developer
* **Juan** – Backend Developer
* **Sanja** – Backend Developer
* **Sumaya** – Backend Developer
* **Zoje** – Backend Developer

---

## ❓ Frequently Asked Questions

### How can I create a group and invite members?

From your dashboard, create a group and use the invite form to send invitations. Members can accept or decline. Once accepted, you can assign them quizzes.

### Can I upload questions using Excel?

Yes! Download the Excel template, fill in your questions, and upload them to import all at once.

### Can users take quizzes more than once?

Each user can attempt a quiz **only once per group** to maintain result fairness.

### How does AI quiz generation work?

Enter a topic, subject, or language, and our AI will generate questions for you instantly. You can review and update them before saving.

### What happens if I forget my password?

Use the password reset option on the login page. An email will be sent with instructions to reset it.

---

## 📎 License

MIT License – feel free to use and contribute.

---

## 💬 Get in Touch

Have suggestions or want to contribute? Feel free to open an issue or pull request.

```

---

Would you like me to format or optimize the badges, project structure section, or deployment instructions as well?
```
