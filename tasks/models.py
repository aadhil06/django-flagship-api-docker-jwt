from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    """
    A simple task model linked to a user.
    """
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Urgent'),
        (5, 'Critical'), # Priority 5 triggers the non-trivial business rule
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'due_date', 'created_at'] # Sort by highest priority first

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title} by {self.owner.username}"