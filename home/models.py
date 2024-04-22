from django.db import models

class SignUp(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    education = models.CharField(max_length=20, choices=[('high_school', 'High School'), ('college', 'College'), ('university', 'University'), ('other', 'Other')])
    reason_to_learn = models.CharField(max_length=50, choices=[('personal_growth', 'Personal Growth'), ('career_advancement', 'Career Advancement'), ('travel', 'Travel'), ('other', 'Other')])
    language_level = models.CharField(max_length=20, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    
    def __str__(self):
        return self.full_name

class SignIn(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.email