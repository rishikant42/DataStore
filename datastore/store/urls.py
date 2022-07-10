from rest_framework.routers import DefaultRouter

from store.views import FormViewSet

app_name = 'store'

router = DefaultRouter()
router.register(r'forms', FormViewSet, basename='form')
urlpatterns = router.urls
