from django.urls import path
from .views import IndexView, FileView, FileCreateView, FileUpdateView, FileDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('file/<int:pk>/', FileView.as_view(), name='file_detail'),
    path('files/create/', FileCreateView.as_view(), name='file_create'),
    path('file/<int:pk>/update/', FileUpdateView.as_view(), name='file_update'),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='file_delete'),
]
