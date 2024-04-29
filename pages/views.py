from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
)
from django.shortcuts import redirect, render
from django.views import View, generic
from .forms import UserSearchForm
from django.apps import apps


# Create your views here.
class HomeView(View):
    template_name = "home.html"
    form_class = UserSearchForm

    def get(self, request, *args, **kwargs):
        user_search_form = self.form_class()
        context = {"user_search_form": user_search_form}

        return render(request, "home.html", context)

    def post(self, request, *args, **kwargs):
        submitted_form = self.form_class(self.request.POST)

        # Check if submitted form is valid
        if not submitted_form.is_valid():
            return redirect("home")

        if "username" in submitted_form.cleaned_data:
            searched_username = submitted_form.cleaned_data["username"]
        else:
            return redirect("home")

        # Show searched user if exists
        if (
                apps.get_model("accounts", "CustomUser")
                        .objects.filter(username=searched_username)
                        .exists()
        ):
            return redirect("user_details", searched_username)
        else:
            return redirect("user_not_found")


class AboutUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "about_us.html")


class ContactsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "contacts.html")


from django.http import HttpResponse
from django.shortcuts import render


def load_page(request, page_name):
    try:
        content = render(request, page_name)
        return HttpResponse(content)
    except Exception as e:
        return HttpResponse(status=500)
