from django.urls import path
from authentication.views import UserProfileApi, VerifyOtp


urlpatterns = [
    path("profile/", UserProfileApi.as_view(), name="profile"),
    path("verify_otp/", VerifyOtp.as_view(), name="verifyotp"),
]
