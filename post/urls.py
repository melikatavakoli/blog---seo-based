from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
#---------------------------------------------

router = DefaultRouter()

router.register(r'categories', CategoryView, basename='category')
router.register(r"tags", TagsView, basename="tags")
router.register(r'posts', PostViewSet, basename='posts')

app_name="post"

urlpatterns=[
    path('', include(router.urls)),
# =========================== Contact Us Message ================================
    path("user-contact-us/", ContactUsUserView.as_view(), name="contact_us"),
    path("admin-contact-us/", ContactUsAdminView.as_view(), name="contact_us"),
]