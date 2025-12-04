from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# --- Helper Function for JWT Authentication ---
def get_tokens_for_user(user):
    """Generates JWT tokens for a given user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class TaskAPITestCase(APITestCase):
    """
    Unit tests for the Task CRUD endpoints and the critical business rule.
    """

    def setUp(self):
        # 1. Create a primary test user
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.token1 = get_tokens_for_user(self.user1)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        
        # 2. Create a second user for ownership/permission tests
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

        # 3. Define the base URL for the list/create endpoint
        self.list_url = reverse('task-list')
        
        # 4. Create a sample task for the primary user
        self.task_data = {
            'title': 'Test Task Title',
            'priority': 2,
            'is_completed': False
        }
        self.task1 = Task.objects.create(owner=self.user1, **self.task_data)
        self.detail_url = reverse('task-detail', kwargs={'pk': self.task1.pk})


    # --- Test Authentication and Permissions ---
    
    def test_list_tasks_unauthenticated(self):
        """Ensure unauthenticated access is denied."""
        self.client.credentials() # Clear credentials
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tasks_authenticated(self):
        """Ensure authenticated user can list tasks and only sees their own."""
        # Create a task for user2
        Task.objects.create(owner=self.user2, title='User 2 Task', priority=1)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User 1 should only see the task they created (self.task1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.task1.title)

    # --- Test CRUD Functionality ---

    def test_create_task(self):
        """Test successful task creation."""
        response = self.client.post(self.list_url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2) # Original task + new task
        self.assertEqual(response.data['owner'], self.user1.username) # Check ownership is set

    def test_retrieve_task(self):
        """Test retrieving a single task."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task1.title)

    def test_update_task(self):
        """Test updating a task title."""
        new_title = "Updated Task Title"
        response = self.client.patch(self.detail_url, {'title': new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, new_title)

    def test_delete_task(self):
        """Test deleting a task."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0) # Only one task existed, now it's zero

    # --- Test Non-Trivial Business Rule ---

    def test_business_rule_critical_task_limit(self):
        """
        Test the rule: max 3 active Critical Tasks (Priority 5).
        """
        # Create 3 active Critical Tasks (Priority 5)
        for i in range(3):
            Task.objects.create(
                owner=self.user1, 
                title=f'Critical Task {i+1}', 
                priority=5, 
                is_completed=False
            )
        
        # Attempt to create a 4th Critical Task
        critical_data = {'title': '4th Critical Task Attempt', 'priority': 5}
        response = self.client.post(self.list_url, critical_data, format='json')
        
        # Assert the request is blocked with a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot create Critical Task', response.data['detail'])
        
        # Ensure only the initial task + the 3 critical tasks were created (total 4)
        self.assertEqual(Task.objects.filter(owner=self.user1).count(), 4) 

    def test_business_rule_critical_task_completed_allows_new_one(self):
        """
        Test that completing a critical task allows a new one to be created.
        """
        # 1. Create 3 active Critical Tasks
        for i in range(3):
            Task.objects.create(
                owner=self.user1, 
                title=f'Critical Task {i}', 
                priority=5, 
                is_completed=False
            )
        
        # 2. Mark one critical task as completed (making the count 2 active)
        Task.objects.filter(owner=self.user1, priority=5).first().is_completed = True
        Task.objects.filter(owner=self.user1, priority=5).first().save()

        # 3. Attempt to create a 4th Critical Task (which is now allowed)
        critical_data = {'title': 'New Critical Task Allowed', 'priority': 5}
        response = self.client.post(self.list_url, critical_data, format='json')
        
        # Assert success (HTTP 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(owner=self.user1, priority=5, is_completed=False).count(), 3)