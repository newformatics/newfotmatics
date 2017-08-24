from rest_framework import serializers
from .models import Task, Answer


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())
    solutions = serializers.DictField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Task
        fields = ('url', 'id', 'author', 'name', 'description', 'tags', 'solutions')
        read_only_fields = ('id', )


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    task = serializers.HyperlinkedRelatedField(view_name='task-detail', queryset=Task.objects.all())
    code = serializers.SerializerMethodField('code')
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Answer
        fields = ('url', 'id', 'author', 'language', 'is_right', 'task', 'code')
        read_only_fields = ('id', 'is_right')

    def code(self, obj):
        user = self.context.get('request').user
        if obj.author != user or not user.is_staff:
            return 'hidden'
        return obj.code
