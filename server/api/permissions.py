from rest_framework import permissions
import logging
logger = logging.getLogger(__name__)

from .utils import (
    analyzeMethod,
)


class IsMyselfOrReadOnly(permissions.BasePermission):
    """
    自分以外はREADオンリーのオブジェクトレベルpermission
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
