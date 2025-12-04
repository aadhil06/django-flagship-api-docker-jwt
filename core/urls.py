from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # Application API Routes (CRUD for Tasks)
    path('api/', include('tasks.urls')),

    # JWT Authentication Endpoints (Simple Auth)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Note: For user registration, you would add a custom view here.
]