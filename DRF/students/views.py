from django.shortcuts import render
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from .models import Students
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework import status

@api_view(["GET"])
def get_student_deatil(request):
    try:
        student_deatil = Students.objects.get(name="Faraz")
        student_deatil_serializer = StudentSerializer(student_deatil)
        return JsonResponse(student_deatil_serializer.data, status.HTTP_200_OK)
    except Students.DoesNotExist:
        return JsonResponse(
            {"response": "Student with the given name does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return JsonResponse(
            {
                "response": f"Error: {e}",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )


@api_view(["GET"])
def get_all_student_deatils(request):
    try:
        all_student_deatil = Students.objects.all()
        all_student_deatil_serializer = StudentSerializer(all_student_deatil, many=True)
        return JsonResponse(all_student_deatil_serializer.data, safe=False)
    except Exception as e:
        return JsonResponse(
            {"response": f"An Error Occured While Fetching all the deatils: {e}"}
        )


@api_view(["POST"])
def create_student(request):
    try:
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"response": f"An Error Occured While Creating Student: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
