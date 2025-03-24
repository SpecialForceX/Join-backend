from django.shortcuts import render
from rest_framework import viewsets
from .models import Contact, Task, SubTask, LoginData
from .serializers import ContactSerializer, TaskSerializer, SubTaskSerializer, LoginDataSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import date


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ VALIDATION ERROR:", serializer.errors)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class LoginDataViewSet(viewsets.ModelViewSet):
    queryset = LoginData.objects.all()
    serializer_class = LoginDataSerializer


@api_view(['GET'])
def summary_view(request):
    all_tasks = Task.objects.all()

    todo = all_tasks.filter(status='todo').count()
    done = all_tasks.filter(status='done').count()
    urgent_tasks = all_tasks.filter(prio='urgent')
    urgent_count = urgent_tasks.count()
    in_board = all_tasks.count()
    in_progress = all_tasks.filter(status='in_progress').count()
    awaiting_feedback = all_tasks.filter(status='awaiting_feedback').count()

    # 🔍 Früheste Deadline (falls vorhanden)
    upcoming_dates = urgent_tasks.values_list('date', flat=True).filter(
        date__gte=date.today()).order_by('date')
    if upcoming_dates:
        earliest = upcoming_dates[0].strftime('%B %d, %Y')
    else:
        earliest = None

    return Response({
        "todo": todo,
        "done": done,
        "urgent": urgent_count,
        "earliest_deadline": earliest,
        "in_board": in_board,
        "in_progress": in_progress,
        "awaiting_feedback": awaiting_feedback
    })
