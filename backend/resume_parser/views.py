import re
SKILL_KEYWORDS = [
	'python', 'django', 'react', 'machine learning', 'nlp', 'sql', 'javascript', 'aws', 'docker', 'git', 'linux',
	'tensorflow', 'pytorch', 'data analysis', 'excel', 'communication', 'leadership', 'project management',
	'node.js', 'spring', 'hibernate', 'mongodb', 'mysql', 'docker', 'rest', 'api', 'java', 'c++', 'c#', 'html', 'css', 'javascript', 'typescript', 'flask', 'fastapi', 'pandas', 'numpy', 'matplotlib', 'scikit-learn', 'keras', 'cloud', 'azure', 'gcp', 'kubernetes', 'devops', 'oop', 'oop concepts', 'data structures', 'algorithms', 'problem solving', 'debugging', 'testing', 'unit testing', 'integration testing', 'agile', 'scrum', 'kanban', 'jira', 'gitlab', 'github', 'bitbucket', 'ci/cd', 'jenkins', 'ansible', 'terraform', 'networking', 'security', 'encryption', 'cryptography', 'steganography', 'restful', 'api', 'microservices', 'grpc', 'docker-compose', 'virtualization', 'vmware', 'hyper-v', 'aws lambda', 's3', 'ec2', 'cloudformation', 'cloudwatch', 'cloudfront', 'sns', 'sqs', 'firebase', 'heroku', 'vercel', 'netlify', 'websockets', 'socket.io', 'redux', 'mobx', 'vue', 'angular', 'bootstrap', 'tailwind', 'material-ui', 'ant-design', 'primefaces', 'selenium', 'cypress', 'playwright', 'pytest', 'unittest', 'junit', 'mocha', 'chai', 'jest', 'enzyme', 'robot framework', 'postman', 'swagger', 'openapi', 'graphql', 'apollo', 'rest api', 'api design', 'api testing', 'api documentation', 'api security', 'api gateway', 'api management', 'api monitoring', 'api analytics', 'api performance', 'api scalability', 'api reliability', 'api availability', 'api maintainability', 'api usability', 'api versioning', 'api deprecation', 'api migration', 'api integration', 'api orchestration', 'api automation', 'api deployment', 'api configuration', 'api discovery', 'api registration', 'api deregistration', 'api authentication', 'api authorization', 'api access control', 'api rate limiting', 'api throttling', 'api caching', 'api logging', 'api tracing', 'api monitoring', 'api alerting', 'api notification', 'api reporting', 'api billing', 'api metering', 'api monetization', 'api marketplace', 'api developer portal', 'api documentation', 'api sdk', 'api cli', 'api testing', 'api mocking', 'api simulation', 'api virtualization', 'api sandbox', 'api staging', 'api production', 'api deployment', 'api rollback', 'api blue-green deployment', 'api canary deployment', 'api feature flag', 'api ab testing', 'api chaos engineering', 'api resilience', 'api fault tolerance', 'api circuit breaker', 'api bulkhead', 'api retry', 'api timeout', 'api fallback', 'api degradation', 'api failover', 'api disaster recovery', 'api backup', 'api restore', 'api migration', 'api upgrade', 'api downgrade', 'api patch', 'api hotfix', 'api bugfix', 'api enhancement', 'api improvement', 'api optimization', 'api refactoring', 'api reengineering', 'api modernization', 'api transformation', 'api innovation', 'api disruption', 'api revolution', 'api evolution', 'api future', 'api trend', 'api prediction', 'api forecast', 'api roadmap', 'api vision', 'api mission', 'api goal', 'api objective', 'api strategy', 'api plan', 'api initiative', 'api project', 'api program', 'api portfolio', 'api product', 'api service', 'api solution', 'api platform', 'api ecosystem', 'api community', 'api partner', 'api customer', 'api user', 'api developer', 'api tester', 'api architect', 'api manager', 'api owner', 'api sponsor', 'api stakeholder', 'api champion', 'api advocate', 'api evangelist', 'api ambassador', 'api influencer', 'api leader', 'api expert', 'api specialist', 'api consultant', 'api advisor', 'api mentor', 'api coach', 'api trainer', 'api teacher', 'api student', 'api learner', 'api researcher', 'api analyst', 'api scientist', 'api engineer', 'api developer', 'api tester', 'api architect', 'api manager', 'api owner', 'api sponsor', 'api stakeholder', 'api champion', 'api advocate', 'api evangelist', 'api ambassador', 'api influencer', 'api leader', 'api expert', 'api specialist', 'api consultant', 'api advisor', 'api mentor', 'api coach', 'api trainer', 'api teacher', 'api student', 'api learner', 'api researcher', 'api analyst', 'api scientist', 'api engineer'
]

def extract_skills(text):
	text_lower = text.lower()
	found = set()
	for skill in SKILL_KEYWORDS:
		if skill in text_lower:
			found.add(skill)
		 # Temporary addition to avoid empty skill list; remove or modify as needed
	return sorted(found)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Resume
from .serializers import ResumeSerializer
import pdfplumber
import docx
import os

def extract_text_from_pdf(file_path):
	with pdfplumber.open(file_path) as pdf:
		return '\n'.join(page.extract_text() or '' for page in pdf.pages)

def extract_text_from_docx(file_path):
	doc = docx.Document(file_path)
	return '\n'.join([para.text for para in doc.paragraphs])

class ResumeUploadView(APIView):
	parser_classes = (MultiPartParser, FormParser)

	def post(self, request, format=None):
		file_obj = request.FILES.get('file')
		job_desc = request.data.get('job_description', '').strip()
		if not file_obj:
			return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
		if not job_desc:
			return Response({'error': 'No job description provided.'}, status=status.HTTP_400_BAD_REQUEST)

		resume = Resume.objects.create(file=file_obj)
		file_path = resume.file.path
		ext = os.path.splitext(file_path)[1].lower()
		if ext == '.pdf':
			text = extract_text_from_pdf(file_path)
		elif ext in ['.docx', '.doc']:
			text = extract_text_from_docx(file_path)
		else:
			resume.delete()
			return Response({'error': 'Unsupported file type.'}, status=status.HTTP_400_BAD_REQUEST)

		# --- Extract skills from resume text ---
		extracted_skills = extract_skills(text)

		# --- Gemini API integration ---
		gemini_questions = []
		gemini_raw = None
		try:
			import requests
			GEMINI_API_URL = os.environ.get('GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent')
			GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyALjSQuSzn1SdqBNe45eRif3KnJnIXSncQ')
			prompt = f"Resume Data (parsed):\n{text}\n\nJob Description and custom instructions:\n{job_desc}\n\nGenerate interview questions for this candidate based only on the data parsed from the resume and the job description. Format the questions in sections: Introduction, Projects, Work Experience (if any), and Data-based questions. Do not use generic skill-based questions."
			payload = {
				"contents": [{"parts": [{"text": prompt}]}]
			}
			headers = {"Content-Type": "application/json"}
			response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=payload, headers=headers, timeout=30)
			if response.ok:
				data = response.json()
				gemini_raw = data
				candidates = data.get('candidates', [])
				if candidates:
					gemini_text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
					gemini_questions = [q.strip() for q in gemini_text.split('\n') if q.strip()]
		except Exception as e:
			return Response({'error': f"Gemini API error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		if not gemini_questions:
			return Response({'error': 'No questions generated by Gemini API.', 'gemini_raw': gemini_raw}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		resume.skills = extracted_skills
		resume.questions = gemini_questions
		resume.save()
		serializer = ResumeSerializer(resume)
		# Add skills to response for frontend
		response_data = serializer.data
		response_data['skills'] = extracted_skills
		return Response(response_data, status=status.HTTP_201_CREATED)
	
