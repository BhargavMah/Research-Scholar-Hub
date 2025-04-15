from django.db import models
from django.contrib.auth.models import User

class ResearcherProfile(models.Model):
    ACADEMIC_TITLE_CHOICES = [
        ('INT_PHD', 'Integrated PhD'),
        ('PHD', 'PhD'),
        ('POST_DOC', 'Post Doctoral'),
        ('PROF', 'Professor'),
        ('ASST_PROF', 'Assistant Professor'),
        ('ASSOC_PROF', 'Associate Professor'),
        ('RES_SCHOLAR', 'Research Scholar'),
        ('SCIENTIST', 'Scientist'),
        ('SR_SCIENTIST', 'Senior Scientist'),
        ('PRINCIPAL', 'Principal Investigator'),
        ('OTHER', 'Other')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    academic_title = models.CharField(max_length=20, choices=ACADEMIC_TITLE_CHOICES, default='RES_SCHOLAR')
    other_academic_title = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    research_field = models.CharField(max_length=100)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    country = models.CharField(max_length=100, default='')
    other_country = models.CharField(max_length=100, blank=True, null=True)
class Research(models.Model):
    CATEGORY_CHOICES = [
        ('HYD', 'Hydrogen'),
        ('SOL', 'Solar'),
        ('NUC', 'Nuclear'),
        ('OTH', 'Other')
    ]
    
    researcher = models.ForeignKey(ResearcherProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    efficiency_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    methodology = models.TextField()
    results = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    research_paper = models.FileField(upload_to='research_papers/')
    
    def __str__(self):
        return self.title
