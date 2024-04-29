from django.urls import reverse
from django.db import models


# Create your models here.
class Resume(models.Model):
    owner = models.OneToOneField("accounts.CustomUser", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20)
    birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    experience = models.TextField(default="", null=False, blank=False)
    skills = models.TextField(default="", null=False, blank=False)
    languages = models.TextField(default="", null=False, blank=False)
    let_anon_users_see_resume = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.job_title

    def get_absolute_url(self) -> str:
        return reverse("resume_details", kwargs={"username": self.owner.username})