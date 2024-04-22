from django.urls import path
from .views import AuthenticateView, VerifyCodeView, ProfileView, ActivateInviteCodeView

urlpatterns = [
    path('authenticate/', AuthenticateView.as_view(), name='authenticate'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('activate-invite-code/', ActivateInviteCodeView.as_view(), name='activate_invite_code'),
]
