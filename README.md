
```markdown
# College Document Managenment System

A Django-based web application for managing document operations including student, teacher, and staff records, document management, and user roles.

## 🌐 Live Demo (Hosted on PythonAnywhere)

Access the deployed application: [https://samarthpansare.pythonanywhere.com](https://samarthpansare.pythonanywhere.com]

### 👥 Demo User Credentials


**Teachers:**
1. Math Principal/Vice-Principal/HOD
   - Username: `teacher1`
   - Password: `teacherpass123`
2. Computer Science HOD
   - Username: `teacher2`
   - Password: `teacherpass123`
3. Physics HOD/IQUAC
   - Username: `teacher3`
   - Password: `teacherpass123`
4. English Exam
   - Username: `teacher4`
   - Password: `teacherpass123`

**Students:**
1. Computer Science Student
   - Username: `student1`
   - Password: `studentpass123`
2. Mathematics Student
   - Username: `student2`
   - Password: `studentpass123`
3. Physics Student
   - Username: `student3`
   - Password: `studentpass123`
4. English Student
   - Username: `student4`
   - Password: `studentpass123`


## 🛠 Developer Setup Guide

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/SamarthPansare/SPC.git
   cd SPC
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file:
   ```ini
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost/school_db
   ```

5. **Set up database**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data**
   ```bash
   python manage.py loaddata initial_data.json
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```


## 📂 Project Structure
```
school-management-system/
├── documents/          # Document management app
├── users/              # User profiles and authentication
├── static/             # Static files
├── templates/          # Base templates
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🔧 Key Features
- Role-based access control
- Department-wise document management
- Student academic records
- Teacher role assignments
- Staff management


## ✉️ Contact
For questions or support, contact [samarth.pansare20002@gmail.com](mailto:samarth.pansare20002@gmail.com)
```

### Key Sections Included:

1. **Live Demo Section** - With direct link and ready-to-use credentials
2. **Developer Setup** - Detailed local installation instructions
3. **Project Structure** - Overview of important directories
4. **Feature List** - Highlights of what the system does


