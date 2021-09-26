from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TableRow
from .serializers import TableRowSerializer


class TableRowView(APIView):
    def get(self, request):
        order_by = request.GET.get('order_by', None)
        filter_by = request.GET.get('filter_by', None)
        condition = request.GET.get('condition', None)
        val = request.GET.get('val', None)
        table_rows = TableRow.objects.all()

        filter_key = None
        if filter_by is not None and condition is not None and val is not None:
            if condition == 'equal':
                filter_key = filter_by
            elif condition == 'greater':
                filter_key = filter_by + '__gt'
            elif condition == 'less':
                filter_key = filter_by + '__lt'
            elif condition == 'contains':
                filter_key = filter_by + '__contains'
        if filter_key is not None:
            filter_kwargs = {
                filter_key: val
            }
            table_rows = table_rows.filter(**filter_kwargs)
        # TODO try to fix later
        if order_by is not None and order_by in ['dt', 'name', 'amount', 'distance']:
            table_rows = table_rows.order_by(order_by)
        ser = TableRowSerializer(table_rows, many=True)

        return Response(ser.data)
