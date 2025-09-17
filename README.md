# AI Interview Prep Project

This repository contains a full-stack application for AI-assisted interview preparation. It enables users to upload their resumes, automatically extracts relevant skills, and generates tailored interview questions using AI.

## Repository Structure

- **backend/**: Django REST API for resume parsing and question generation.
- **ai_interview_prep_frontend/**: React app for uploading resumes and displaying generated questions.

## Features

- **Resume Upload:** Users can upload resumes in PDF or DOCX format.
- **Resume Parsing:** The backend extracts skills from resumes using keyword matching and basic NLP.
- **Skill Extraction:** Automatically identifies technical and soft skills from the resume text.
- **AI Question Generation:** Integrates with the Gemini API to generate interview questions based on resume content and job description.
- **Interactive UI:** The frontend displays extracted skills and AI-generated questions, allowing users to practice.

## Technologies Used

- **Backend:** Django, Django REST Framework, pdfplumber, python-docx
- **Frontend:** React, Axios
- **AI Integration:** Gemini API (Google Generative Language)
- **Database:** SQLite (default for Django)

## Implementation Overview

### Backend (`backend/`)

- **Resume Parsing:** Uses pdfplumber for PDFs and python-docx for DOCX files. Skills are extracted using a predefined keyword list.
- **Skill Extraction:** Custom logic matches keywords in the resume text.
- **Question Generation:** Sends parsed resume and job description to Gemini API for question generation.
- **API Endpoint:** `/api/upload_resume/` accepts resume file and job description, returns extracted skills and generated questions.

### Frontend (`ai_interview_prep_frontend/`)

- **Resume Upload Form:** Users select a resume file and enter a job description.
- **Question Display:** Shows AI-generated questions organized by section (Introduction, Projects, Work Experience, Data-based).
- **Skill Sidebar:** Displays extracted skills from the uploaded resume.
- **Error Handling:** Shows errors for unsupported file types, missing job description, or upload failures.

## Setup Instructions

### Backend

1. Navigate to `backend`
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run migrations:
    ```bash
    python manage.py migrate
    ```
4. Start the server:
    ```bash
    python manage.py runserver
    ```
5. (Optional) Set environment variables for Gemini API keys if needed.

### Frontend

1. Navigate to `ai_interview_prep_frontend`
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm start
    ```

## Folder Structure

```
backend/
    ├── resume_parser/
    ├── migrations/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── manage.py
    ├── requirements.txt
ai_interview_prep_frontend/
    ├── src/
        ├── App.js
        ├── index.js
    ├── package.json
    ├── public/
        ├── index.html
```

## How It Works

1. **User uploads a resume and provides a job description via the frontend.**
2. **Frontend sends the file and description to the backend API.**
3. **Backend parses the resume, extracts skills, and sends data to Gemini API for question generation.**
4. **Backend returns extracted skills and questions to the frontend.**
5. **Frontend displays skills and organizes questions for user practice.**

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

---

**Explanation:**  
This README describes a full-stack AI Interview Prep application. The backend uses Django to parse resumes and extract skills, then calls the Gemini API to generate interview questions. The frontend, built with React, allows users to upload resumes, view extracted skills, and practice with AI-generated questions. Setup instructions are provided for both backend and frontend, and the folder structure is outlined for clarity.