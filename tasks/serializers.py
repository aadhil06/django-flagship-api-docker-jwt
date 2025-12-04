from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Read-only fields provide useful context without allowing direct modification.
    """
    # owner is a read-only field that displays the owner's username
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = (
            'id', 'owner', 'title', 'description', 
            'priority', 'is_completed', 'due_date', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at',)