from rest_framework.routers import DefaultRouter
from app_ingenieros.views import MembersViewSet, EngineersViewSet, DocumentTypeViewSet

router = DefaultRouter()
router.register('members', MembersViewSet, basename='members')
router.register('engineers', EngineersViewSet, basename='engineers')
router.register('document-types', DocumentTypeViewSet, basename='document-types')

urlpatterns = router.urls
