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


class BlockListPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        logger.debug('===============BlockListPermission===============')
        logger.debug(self)
        logger.debug(request.user)
        logger.debug(view)
        logger.debug(obj)
        return True
