from rest_framework import serializers

from task_instance.models import TaskInstance


class TaskInstanceSerializer(serializers.ModelSerializer):
    task_title = serializers.StringRelatedField(source='task.title', read_only=True)
    project_title = serializers.StringRelatedField(source='task.project.title', read_only=True)

    class Meta:
        model = TaskInstance
        fields = '__all__'
        read_only_fields = ['duration_worked']
