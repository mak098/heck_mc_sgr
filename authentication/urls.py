from django.urls import include, path
from rest_framework import routers

from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSets, basename ='user')
router.register(r'users-signup', views.UserSignupViewSets, basename ='user-signup')

urlpatterns = [
    path('', include(router.urls)),
    path('signin/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.UserViewSets.as_view({'post': 'logout'}), name='logout'),
    path('update-password/', views.UserViewSets.as_view({'post': 'update_password'}), name='update_password'),
    path('update-profil-image/', views.UserViewSets.as_view({'post': 'upload_profil_image'}), name='upload_profil_image'),
    path('update-profil-info/', views.UserViewSets.as_view({'post': 'update_info'}), name='update_info'),
    path('signup/', views.UserSignupViewSets.as_view({'post': 'signup'}), name='signup'),

  ]