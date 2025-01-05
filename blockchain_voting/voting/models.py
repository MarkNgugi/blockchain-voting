from django.db import models
from django.db import models
from django.contrib.auth.models import User


class ValidAdmissionNumber(models.Model):
    admission_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.admission_number


class Student(models.Model):
    admission_number = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link the student to a Django User
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.admission_number


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    vote_count = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='candidate_images/', blank=True, null=True)
    blockchain_id = models.IntegerField(null=True, blank=True)  # New field for the blockchain ID

    def __str__(self):
        return self.name


class VotingTimeframe(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Voting from {self.start_time} to {self.end_time}"


