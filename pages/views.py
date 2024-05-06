"""
This module contains the views for the pages app.

The module contains the following classes:
    ``HomeView`` - This class is a view for the homepage.
"""


from django.http import (
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
)
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserSearchForm
from django.apps import apps


class HomeView(View):
    """A view for the homepage.

    Attributes:
        template_name (str): The name of the template to render.
        form_class (class): The form class to use for user search.
    """

    template_name = "home.html"
    form_class = UserSearchForm

    def get(self, request, *args, **kwargs):
        """Called when a GET request is made to this
        view. It renders the ``home.html`` template with a UserSearchForm
        instance.

        Args:
            request (HttpRequest): The request that was made.
            *args: Additional arguments passed to the function.
            **kwargs: Additional keyword arguments passed to the function.

        Returns:
            HttpResponse: The response that will be sent to the client.
        """
        user_search_form = self.form_class()
        context = {"user_search_form": user_search_form}

        return render(request, "home.html", context)

    def post(self, request, *args, **kwargs):
        """Called when a POST request is made to this
        view. It processes the submitted form and either redirects
        to the user details page if the user exists or to the user not
        found page if the user does not exist.

        Args:
            request (HttpRequest): The request that was made.
            *args: Additional arguments passed to the function.
            **kwargs: Additional keyword arguments passed to the function.

        Returns:
            HttpResponse: The response that will be sent to the client.
        """
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

