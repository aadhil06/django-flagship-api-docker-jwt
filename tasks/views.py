from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer

# Define the constants for the business rule
CRITICAL_PRIORITY = 5
CRITICAL_TASK_LIMIT = 3

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, viewing, and editing tasks.
    It includes the business rule check during task creation.
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Ensures users can only see their own tasks.
        """
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Sets the owner of the task to the currently logged-in user
        AND enforces the non-trivial business rule.
        """
        # 1. Enforce Business Rule: Limit on Critical Tasks (Priority 5)
        
        # Check if the task being created is a Critical Task
        if serializer.validated_data.get('priority') == CRITICAL_PRIORITY:
            
            # Count the user's existing, active Critical Tasks (not completed)
            critical_tasks_count = Task.objects.filter(
                Q(owner=self.request.user) & 
                Q(priority=CRITICAL_PRIORITY) & 
                Q(is_completed=False)
            ).count()

            if critical_tasks_count >= CRITICAL_TASK_LIMIT:
                # If limit reached, raise a custom validation error (HTTP 400)
                raise ValidationError({
                    'detail': f'Cannot create Critical Task (Priority {CRITICAL_PRIORITY}). '
                              f'You have reached the limit of {CRITICAL_TASK_LIMIT} active critical tasks.'
                })

        # 2. Save the task, associating it with the current user
        serializer.save(owner=self.request.user)