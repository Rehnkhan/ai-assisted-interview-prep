import os
from django.db import models

def resume_upload_path(instance, filename):
	return os.path.join('resumes', filename)

class Resume(models.Model):
	file = models.FileField(upload_to=resume_upload_path)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	skills = models.JSONField(default=list, blank=True)
	questions = models.JSONField(default=list, blank=True)

	def __str__(self):
		return f"Resume {self.id}"
from django.db import models

# Create your models here.
