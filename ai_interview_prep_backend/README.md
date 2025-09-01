# Backend for AI Interview Prep

This Django project will provide APIs to:
- Upload and parse PDF/DOCX resumes
- Extract skills using spaCy
- Return skill-based interview questions

## Setup
1. Create a virtual environment and activate it:
   python -m venv venv
   venv\Scripts\activate
2. Install dependencies:
   pip install django djangorestframework pdfplumber python-docx spacy
   python -m spacy download en_core_web_sm
3. Start the Django project:
   django-admin startproject backend .

## API Endpoints
- /api/upload_resume/ : Upload a resume and get questions
