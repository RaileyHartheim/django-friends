from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CustomUserViewSet, RequestInViewSet, RequestOutViewSet
from .yasg import urlpatterns as doc_urls

app_name = 'api'

router = SimpleRouter()

router.register('users', CustomUserViewSet, basename='custom_user')
router.register('requests/incoming', RequestInViewSet,
                basename='incoming_requests')
router.register('requests/outcoming', RequestOutViewSet,
                basename='outcoming_requests')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
