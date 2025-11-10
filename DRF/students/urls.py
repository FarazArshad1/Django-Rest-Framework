from django.urls import path
from . import views

urlpatterns = [
    path(
        route="",
        view=views.get_student_deatil,
        name="Get Single Student Detail by name",
    ),
    path(
        route="all/", view=views.get_all_student_deatils, name="Get all student Details"
    ),
    path(
        route="student_details/",
        view=views.student_details,
        name="Create student record",
    ),
]
