from django.urls import path
from .views import chat, ChatBotView, UploadTrainingFileView

urlpatterns = [
    path('', chat, name='chat'),
    path('chatbot/', ChatBotView.as_view(), name='chatbot'),
    path('upload-training-file/', UploadTrainingFileView.as_view(), name='upload-training-file'),
]
