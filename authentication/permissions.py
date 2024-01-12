from rest_framework.permissions import BasePermission
from authentication.models import RecruiterProfile


class RecruitersOnly(BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     print(view,obj)
    #     if obj is not isinstance(obj, RecruiterProfile):
    #         return False
    #     return True

    def has_permission(self, request, view):
        if request.user.account_type == 'jobseeker':
            return False
        return True