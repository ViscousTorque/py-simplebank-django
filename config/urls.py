from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse
from apps.users.views import CreateUserView, UpdateUserView, LoginUserView, VerifyEmailView
from apps.accounts.views import CreateAccountView, ListAccountsView, GetAccountView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

def root_view(request):
    return JsonResponse({"message": "Welcome to the SimpleBank API!"})

# TODO: Refactor path / routes
urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('v1/create_user', CreateUserView.as_view(), name='create-user'),
    path('v1/update_user', UpdateUserView.as_view(), name='update-user'),
    path('v1/login_user', LoginUserView.as_view(), name='login-user'),
    path('v1/verify_email', VerifyEmailView.as_view(), name='verify-email'),

    path('v1/create_account', CreateAccountView.as_view(), name='create-account'),
    path('v1/list_accounts', ListAccountsView.as_view(), name='view-accounts'),
    path('v1/get_account/<int:id>', GetAccountView.as_view(), name='view-account'),
    
    path('v1/transfers', include('apps.transactions.urls')),

    path('v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('v1/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('v1/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

