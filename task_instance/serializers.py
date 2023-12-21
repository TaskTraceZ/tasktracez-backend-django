from rest_framework import serializers

from task_instance.models import TaskInstance


class TaskInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = '__all__'
