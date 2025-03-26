from django.urls import path
from .views import CreateTransferView

urlpatterns = [
    path('', CreateTransferView.as_view(), name='create-transfer'),
]
