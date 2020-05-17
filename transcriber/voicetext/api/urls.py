from django.urls import include,path
from rest_framework.routers import DefaultRouter
from voicetext.api import views as qv

router = DefaultRouter()
router.register(r"voicetext",qv.VoiceViewSet)
# router.register(r"segment",qv.SegmentViewSet)

urlpatterns=[
    path("",include(router.urls)),

    # testing use case
    # path("voicetext/<int:voice_id>/segment/",
    #     qv.SegmentCreateAPIView.as_view(),name="segment-view"),

    path("usersegment/",qv.SegmentListView.as_view(),name="user-segment"),
    path("usersegment/<int:pk>/",qv.SegmentAPIView.as_view(),name="user-segment-details"),
] 