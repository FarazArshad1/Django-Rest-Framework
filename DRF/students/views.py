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
        return Response(student_deatil_serializer.data, status.HTTP_200_OK)
    except Students.DoesNotExist:
        return JsonResponse(
            {"response": "Student with the given name does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
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
        return Response(all_student_deatil_serializer.data, safe=False)
    except Exception as e:
        return Response(
            {"response": f"An Error Occured While Fetching all the deatils: {e}"}
        )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def student_details(request, pk):
    try:
        serializer = Students.objects.get(pk=pk)
    except Students.DoesNotExist:
        return Response(
            {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        try:
            serializer = StudentSerializer(Students)
            return Response({"message": "Success"}, serializer.data)
        except Students.DoesNotExist:
            return Response(
                {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == "PUT":
        try:
            serializer = StudentSerializer(Students, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(
                {"message": "Student Record Updated"}, status=status.HTTP_200_OK
            )
        except Students.DoesNotExist:
            return Response(
                {"message": "User doesn't exits for this Id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": f"An Error Occured while updating the Record {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "PATCH":
        try:
            serializer = StudentSerializer(Students, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(
                {"message": "Student Record Updated", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Students.DoesNotExist:
            return Response(
                {"message": "User doesn't exits for this Id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": f"An Error Occured while updating the Record {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    elif request.method == "DELETE":
        try:
            Students.delete()
            return Response(
                {"message": "Student Record Deleted"},
                status=status.HTTP_200_OK,
            )
        except Students.DoesNotExist:
            return Response(
                {"message": "User doesn't exits for this Id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"message": f"An Error Occured while Deleting the Record {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
