from django.urls import path
from .views import TableRowView

urlpatterns = [
    path('', TableRowView.as_view())
]