from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    #path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]
