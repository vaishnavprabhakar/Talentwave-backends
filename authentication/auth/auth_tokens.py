from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),  # getting the refresh token for user.
        "access": str(refresh.access_token),  # getting the access token for user.
    }
