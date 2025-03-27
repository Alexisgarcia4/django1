from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, PedidoViewSet, RegistroView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
