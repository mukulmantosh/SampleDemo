from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response

from organization.models import Organization
from . import serializer


class OrganizationAPI(ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = serializer.OrganizationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True,
                         "message": "Organization Added !",
                         "data": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class OrganizationRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(id=self.kwargs.get('pk', None))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"status": True, "message": "Organization Updated !", "data": serializer.data})