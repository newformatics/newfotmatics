from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from .models import Task, Answer
from .serializers import TaskSerializer, AnswerSerializer
from .permissions import IsOwnerOrReadOnly
from django.http import JsonResponse, HttpResponseRedirect

import logging

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request=request, *args, **kwargs)
        logger.error('Here is the code: %s' % self.request.data['code'])
        return JsonResponse({'created': True})
