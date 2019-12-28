from datetime import datetime, timezone
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import KeyValStore
from .serializers import KeyValStoreSerializer

FIVE_MIN = 5 * 60

def check_expiration(ttls):
    now = datetime.now(timezone.utc)
    now = datetime.timestamp(now)
    items = []
    for time in ttls:
        time_diff = now - datetime.timestamp(time['ttl'])
        print('t_diff', time_diff)
        if time_diff >= FIVE_MIN:
            items.append(time['ttl'])
    return items


class KeyValViewSet(viewsets.ModelViewSet):

    serializer_class = KeyValStoreSerializer
    queryset = KeyValStore.objects.all()

    # filter_class = KeyValFilter

    # GET
    def list(self, request):
        keyParam = self.request.query_params.get('key', None)
        # print('keyParam:', keyParam)
        # TTL checks 
        ttls = KeyValStore.objects.values('ttl')
        items_to_delete = check_expiration(ttls)
        queryset = KeyValStore.objects.all()
        for row in queryset:
            # print('ttl', row.ttl)
            if row.ttl in items_to_delete:
                print('TTL is expare. so delete it')
                row.delete()
            else:
                KeyValStore.objects.filter(pk=row.id).update(ttl=datetime.now(timezone.utc))
                print('TTL is updated..')
        # ---
        queryset = KeyValStore.objects.all()
        if keyParam is not None:
            keyParam = keyParam.split(',')
            keyFilter = KeyValStore.objects.filter(key__in=keyParam)
            queryset= self.filter_queryset(keyFilter)
        print("Filterd queryset:",queryset)
        # For get data as chunk
        # page = self.paginate_queryset(queryset)
        serializer = KeyValStoreSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    # POST 
    def create(self, request):
        print('on create')  
        # print(dir(request))
        print('data', request.data)
        print('type', type(request.data))
        data = request.data
        if not isinstance(data, list):
            many = False
        else:
            many = True
        serializer = KeyValStoreSerializer(data=data, context={'request': request}, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET
    def retrieve(self, request, pk=None):
        print('on retrieve')
        # TTL checks 
        ttls = KeyValStore.objects.values('ttl')
        items_to_delete = check_expiration(ttls)
        queryset = KeyValStore.objects.all()
        for row in queryset:
            # print('ttl', row.ttl)
            if row.ttl in items_to_delete:
                print('TTL is expare. so delete it')
                row.delete()
            else:
                KeyValStore.objects.filter(pk=pk).update(ttl=datetime.now(timezone.utc))
                print('TTL is updated..')
        # --- 
        queryset = KeyValStore.objects.all()
        kye_obj = get_object_or_404(queryset, pk=pk)
        # print('kye_obj', kye_obj)

        serializer = KeyValStoreSerializer(kye_obj,  context={'request': request})
        return Response(serializer.data)

    # PUT
    def update(self, request, pk=None):
        print('update')

    # PATCH
    def partial_update(self, request, pk=None):
        print('partial_update')
        queryset = KeyValStore.objects.all()
        kye_obj = get_object_or_404(queryset, pk=pk)
 
        serializer = KeyValStoreSerializer(kye_obj, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def destroy(self, request, pk=None):
        print('on destroy')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)