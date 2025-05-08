from rest_framework.routers import DefaultRouter
from app_engineers.views import PersonViewSet

router = DefaultRouter()
# router.register('members', MembersViewSet, basename='members')
# router.register('document-types', DocumentTypeViewSet, basename='document-types')

router.register('persons', PersonViewSet, basename='persons')

urlpatterns = router.urls
