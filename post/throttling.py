from datetime import time
from rest_framework.throttling import UserRateThrottle
from authentication.models import User
from django.db.models import Q


class OnePostPerDay(UserRateThrottle):
    scope = "one_post_per_day"

    def allow_request(self, request, view):
        current_user = request.user
        try:
            last_posted_time = (
                User.objects.filter(Q(email=current_user))
                .prefetch_related("posts")
                .last()
            )
            if last_posted_time:
                last_posted_time.posts.last().created_at
        except Exception:
            pass
        return super().allow_request(request, view)

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}
