from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, TaskViewSet, SubTaskViewSet, LoginDataViewSet, summary_view

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)
router.register(r'loginData', LoginDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', summary_view, name='summary'),

]
