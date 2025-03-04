from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chatbot.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("chatbot-app/", include("chatbot_app.urls")),
]
