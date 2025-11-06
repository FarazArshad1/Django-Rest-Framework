from django.urls import path
from . import views

urlpatterns = [
    path(route="", view=views.student_deatil, name="Get Single Student Detail by name"),
    path(route="all/", view=views.all_student_deatils, name="Get all student Details"),
]
