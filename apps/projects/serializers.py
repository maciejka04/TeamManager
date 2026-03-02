from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # 6) serializator zamienia obiekty bazy danych na JSON
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'priority', 'due_date']