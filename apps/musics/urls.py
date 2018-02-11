from rest_framework import routers
from .views import MusicViewSet

router = routers.DefaultRouter()
# 音乐
router.register(r'music', MusicViewSet, base_name='music')

urlpatterns = router.urls
