from rest_framework.routers import DefaultRouter
from app_engineers.views import PersonViewSet, ContactViewSet, EngineerViewSet

router = DefaultRouter()
# router.register('members', MembersViewSet, basename='members')
# router.register('document-types', DocumentTypeViewSet, basename='document-types')

router.register('persons', PersonViewSet, basename='persons')
router.register('contacts', ContactViewSet, basename='contacts')
router.register('engineers', EngineerViewSet, basename='engineers')



urlpatterns = router.urls
