from django.urls import path
from .views import (
    CreateUserView,
    LoginUserView,
    RenewAccessTokenView,
    UpdateUserView,
    VerifyEmailView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", CreateUserView.as_view(), name="create-user"),
    path("login/", LoginUserView.as_view(), name="login-user"),
    path(
        "token/renew_access/", RenewAccessTokenView.as_view(), name="renew-access-token"
    ),
    path("<str:username>/update/", UpdateUserView.as_view(), name="update-user"),
    path("verify_email/", VerifyEmailView.as_view(), name="verify-email"),
]

# TODO: remove this! I dont think this is being used anywhere now I have tidied up the routes
