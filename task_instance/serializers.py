from rest_framework import serializers

from task_instance.models import TaskInstance


class TaskInstanceSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(source='task.title', read_only=True)

    class Meta:
        model = TaskInstance
        fields = '__all__'
