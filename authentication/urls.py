from django.urls import path
from . import views


urlpatterns = [
    path("profile/", views.UserProfileApi.as_view(), name="profile"),
    path("verify_otp/", views.VerifyOtp.as_view(), name="verifyotp"),
    path(
        "re/profile/", views.RecruiterProfileApiView.as_view(), name="recruiter_profile"
    ),
]
