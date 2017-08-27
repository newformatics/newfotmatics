from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from .models import Task, Answer
from .serializers import TaskSerializer, AnswerSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import mixins, generics, viewsets, response
import memcache
import logging

cache = memcache.Client(['unix:/home/misha/Desktop/webprojects/newformatics/newformatics_memcached.sock'], debug=0)
logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        data = cache.get('task_%s' % pk)
        if data is None:
            logger.error('CRITICAL CACHE DOES NOT EXIST')
            request_result = Task.objects.get(pk=pk)
            serialized_request_result = TaskSerializer(request_result, context={'request': request}).data
            cache.set('task_%s' % pk, serialized_request_result, 60)
            data = serialized_request_result
        return response.Response(data)

    def update(self, request, *args, **kwargs):
        super().update(request=request, *args, **kwargs)
        url = '%s' % request._request.path
        id = int(url.split('/')[-2])
        old_object_in_cache = cache.get('task_%s' % id)
        if old_object_in_cache:
            data = request.data
            data['author'] = old_object_in_cache['author']
            data['id'] = old_object_in_cache['id']
            data['url'] = old_object_in_cache['url']
            cache.set('task_%s' % id, data, 30)

    def delete(self, request, *args, **kwargs):
        super().delete(request=request, *args, **kwargs)
        url = '%s' % request._request.path
        id = int(url.split('/')[-2])
        cache.delete('task_%s' % id)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request=request, *args, **kwargs)
        logger.error('Here is the code: %s' % self.request.data['code'])
        return response.Response({'created': True})

"""
{
    "tags": [
        "learningToCode",
        "beginnerLevel"
    ],
    "name": "Reverse string",
    "description": "There is a string data in input and string's reversed copy in output",
    "solutions": {
        "visible": [
            {
                " output": "abc",
                "input": "cba"
            }
        ],
        "hidden": [
            {
                "input": "pepe",
                "output": "epep"
            }
        ]
    }
}
"""
