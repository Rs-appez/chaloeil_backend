from typing import override
from rest_framework.permissions import BasePermission


class CanFlagQuestion(BasePermission):
    message = "You do not have permission to flag questions."

    @override
    def has_permission(self, request, view):
        return request.user.has_perm("question.can_flag_question")

    # Optional: object-level permission
    @override
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("question.can_flag_question")
