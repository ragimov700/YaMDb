from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class NewViewSet(GenericViewSet, CreateModelMixin,
                 ListModelMixin, DestroyModelMixin):
    pass
