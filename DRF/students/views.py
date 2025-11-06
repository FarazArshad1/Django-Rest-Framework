from django.shortcuts import render
from .serializers import StudentSerializer
from .models import Students
from django.http import JsonResponse

# Create your views here.

def student_deatil(request):
    try:
        student_deatil = Students.objects.get(name="Faraz")
        student_deatil_serializer = StudentSerializer(student_deatil)
        return JsonResponse(student_deatil_serializer.data)
    except Exception as e:
        return JsonResponse({"response" : f"An Error Occured : {e}"})


def all_student_deatils(request):
    try:
        all_student_deatil = Students.objects.all()
        all_student_deatil_serializer = StudentSerializer(all_student_deatil, many=True)
        return JsonResponse(all_student_deatil_serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({"response": f"An Error Occured While Fetching all the deatils: {e}"})
