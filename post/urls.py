from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
#---------------------------------------------

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')
router.register(r'categories', CategoryView, basename='category')
router.register(r"tags", TagsView, basename="tags")
router.register(r"redirect", RedirectViewSet, basename="redirect")
router.register("schemas", SchemaViewSet, basename="schemas")
router.register("media", MediaViewSet, basename="media")

app_name="post"

urlpatterns=[
    path('', include(router.urls)),
    path("create-tags/", TagsView.as_view({'post': 'create'}), name="tags"),
# =========================== Contact Us Message ================================
    path("user-contact-us/", ContactMessageCreateView.as_view(), name="create-contact_us"),
    # path("list-contact-us/", ContactUsView.as_view(), name="list-contact_us"),
    # path('admin-read-status/<uuid:pk>/', ContactMessageReadStatusUpdateView.as_view(),
    #      name='contact-read-status'),
# =========================== post =============================
    path("create-update-post/", CreateUpdatePostAPIView.as_view(), name="create-update-post"),
    path("list-post/", ListPostAPIView.as_view(), name="list-post"),
    path("detail-post/<str:id>", PostRetrieveAPIView.as_view(), name="detail-post"),
    path("<str:slug>/", PostDetailBySlugAPIView.as_view(), name="post_detail_slug"),
]