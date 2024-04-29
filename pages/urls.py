from django.urls import path
from .views import HomeView, AboutUsView, ContactsView
from .views import load_page

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path('load_page/<str:page_name>/', load_page, name='load_page'),
]
