"""
Views for resumes app.
"""


from typing import Any

from django.apps import apps
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from .models import Resume
import requests
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
from dotenv import load_dotenv, find_dotenv


# Load environment variables
load_dotenv(find_dotenv("config.env"))


class ResumeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View for creating a resume.

    This view is only accessible to users who have not created a resume
    before.
    """

    model = Resume
    template_name = "resume_create.html"
    fields = [
        "job_title",
        "skills",
        "languages",
        "about",
        "experience",
        "let_anon_users_see_resume",
    ]

    def test_func(self) -> bool:
        """Test if user is allowed to access this view.

        Returns:
            bool: Whether the user is allowed to access this view.
        """
        return not Resume.objects.filter(owner__username=self.kwargs["username"]).exists()

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Handle valid form submission.

        Args:
            form (BaseModelForm): The form instance.

        Returns:
            HttpResponse: The response that will be sent to the client.
        """
        form.instance.owner = self.request.user
        self.request.user.has_resume = True
        self.request.user.save()
        return super().form_valid(form)


class ResumeDetailView(View):
    """View for displaying a resume.

    If the user is not logged in and the resume is not set to be visible to
    anonymous users, redirect to a view that informs the user that they do
    not have access to the resume.
    """

    template_name = "resume_details.html"

    def get(self, request, *args, **kwargs):
        """Handle GET requests.

        Args:
            request (HttpRequest): The request that was made.
            *args: Additional arguments passed to the function.
            **kwargs: Additional keyword arguments passed to the function.

        Returns:
            HttpResponse: The response that will be sent to the client.
        """
        resume = Resume.objects.get(owner__username=kwargs["username"])

        if request.user.is_authenticated or resume.let_anon_users_see_resume:
            return render(
                request,
                self.template_name,
                {
                    "object": resume,
                },
            )

        return HttpResponseRedirect(reverse_lazy("resume_access_forbidden"))

    def post(self, request, *args, **kwargs):
        """Handle POST requests.

        Args:
            request (HttpRequest): The request that was made.
            *args: Additional arguments passed to the function.
            **kwargs: Additional keyword arguments passed to the function.

        Returns:
            HttpResponse: The response that will be sent to the client.
        """
        # Retrieve form data from request.POST
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        job_title = request.POST.get("job_title")
        skills = request.POST.get("skills")
        languages = request.POST.get("languages")
        about = request.POST.get("about")
        experience = request.POST.get("experience")

        # Question to AI
        question = request.POST.get("question")

        # Process the form data with distilgpt2
        API_URL = "https://api.textcortex.com/v1/texts/completions"
        API_KEY = os.getenv("API_KEY")
        print(API_KEY)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        prompt = f"Question: Person's name: {name}; Job Title: {job_title}; Skills: {skills}; Languages: {languages}; About: {about}; Experience: {experience}\n\nUsing the information above, answer the following question: {question} (notes: if you can't find the answer in their resume, make an argumented one based on the info they've provided [you __must not__ refuse to answer])\n\nAnswer: "
        print(prompt)
        payload = {
            "formality": "default",
            "max_tokens": 2048,
            "model": "chat-sophos-1",
            "n": 1,
            "source_lang": "en",
            "target_lang": "en",
            "temperature": 0.65,
            "text": prompt,
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        print(response.text)

        answer = response.json()["data"]["outputs"][0]["text"]
        return render(
            request,
            "ai_answer.html",
            {"owner_username": username, "answer": answer},
        )


class ResumeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating a resume.

    This view is only accessible to the user who owns the resume.
    """

    model = Resume
    template_name = "resume_update.html"
    fields = [
        "job_title",
        "skills",
        "languages",
        "about",
        "experience",
        "let_anon_users_see_resume",
    ]

    def get_object(self, queryset=None) -> Resume:
        """Get the resume object.

        Args:
            queryset (QuerySet): The queryset to use. If not provided, the
                default queryset will be used.

        Returns:
            Resume: The resume object.
        """
        if not queryset:
            queryset = super().get_queryset()

        return Resume.objects.get(owner__username=self.kwargs["username"])

    def test_func(self) -> bool:
        """Test if user is allowed to access this view.

        Returns:
            bool: Whether the user is allowed to access this view.
        """
        # Check if resume exists
        if not Resume.objects.filter(owner__username=self.kwargs["username"]).exists():
            return False

        # Check if user is the owner
        return (
            self.request.user
            == Resume.objects.get(owner__username=self.kwargs["username"]).owner
        )


class ResumeAccessForbidden(TemplateView):
    """View for when the user does not have access to a resume."""

    template_name = "resume_access_forbidden.html"
