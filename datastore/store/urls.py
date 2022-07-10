from rest_framework.routers import DefaultRouter

from store.views import (
    FormViewSet, QuestionViewSet, ResponseViewSet,
)

app_name = 'store'

router = DefaultRouter()
router.register(r'forms', FormViewSet, basename='form')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'responses', ResponseViewSet, basename='response')
urlpatterns = router.urls
