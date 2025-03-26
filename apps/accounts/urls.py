from django.urls import path
from .views import CreateAccountView, GetAccountView, ListAccountsView

urlpatterns = [
    path('', CreateAccountView.as_view(), name='create-account'),
    path('<int:id>/', GetAccountView.as_view(), name='get-account'),
    path('list/', ListAccountsView.as_view(), name='list-accounts'),
]

# TODO: probably need to delete this!