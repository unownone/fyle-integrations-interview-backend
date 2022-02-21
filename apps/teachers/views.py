from rest_framework import generics, status
from rest_framework.response import Response

from apps.teachers.models import Teacher

from apps.students.models import Assignment

from .serializers import TeacherAssignmentSerializer
# Create your views here.

def ErrorResponse400(message):
    return Response(
        data={'non_field_errors': message},
        status=status.HTTP_400_BAD_REQUEST
    )

class AssignmentsView(generics.ListCreateAPIView):
    serializer_class = TeacherAssignmentSerializer
    
    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)
        
        return Response(
            data = self.serializer_class(assignments, many=True).data,
            status = status.HTTP_200_OK
        )
        
    def patch(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=request.user)
        request.data['teacher'] = teacher.id
        try:
            assignment = Assignment.objects.get(
                pk=int(request.data['id'])
            )
        except Assignment.DoesNotExist:
            return ErrorResponse400(['Assignment Not Found/Access Denied'])        
        except ValueError:            
            return ErrorResponse400(['Assignment ID cannot be a string'])
        except KeyError:
            return ErrorResponse400(['No Assignment ID Provided'])

        serializer = self.serializer_class(assignment,data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                data = serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            data = serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )