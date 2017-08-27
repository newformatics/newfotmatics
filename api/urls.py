from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'tasks', views.TaskViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^tasks/$', views.TaskList().as_view(), name='task-list'),
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskDetail().as_view(), name='task-detail')
]
