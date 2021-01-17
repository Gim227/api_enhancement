from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum
from api_app.models import TableOutput
import json, dateutil.parser
from itertools import groupby
from operator import itemgetter

def _is_missing_request_params(fields_list, req_body):
    for field in fields_list:
        if field not in req_body:
            return True
    return False

@csrf_exempt
def getlineItemUnblendedCost(request):
    '''    
        Get lineItem/UnblendedCost grouping by product/productname
        Output
        {
            "{product/productname_A}": "sum(lineitem/unblendedcost)",
            "{product/productname_B}": "sum(lineitem/unblendedcost)",
            ...
        }
    '''
    fields = ["lineitem/usageaccountid"]
    body = json.loads(request.body.decode('utf-8'))
    if not request.method == "POST":
        return JsonResponse(status=405, data={"Result": "Fail", "Code": "405"})

    if _is_missing_request_params(fields, body):
        return JsonResponse(status=400, data={"Result": "Fail", "Code": "400", "message":"missing required paremeters"})

    try :
        result = TableOutput.objects.values('product_ProductName').order_by('product_ProductName').annotate(sum=Sum('lineItem_UnblendedCost'))
        response_data={
            "result": "Success", 
            "code": "0",
            "output": {},
        }
        for i in result :
            response_data["output"][i['product_ProductName']] = i['sum']
        return JsonResponse(status=400, data=response_data)
    except Exception as e:
        print(e)
        return JsonResponse(status=400, data={"result": "Fail", "code": "400"})

@csrf_exempt
def getDailyLineItemUsageAmount(request):
    '''    
        Get daily lineItem/UsageAmount grouping by product/productname
        {
        "{product/productname_A}": {
            "YYYY/MM/01": "sum(lineItem/UsageAmount)",
            "YYYY/MM/02": "sum(lineItem/UsageAmount)",
            "YYYY/MM/03": "sum(lineItem/UsageAmount)",
            ...
        },
        "{product/productname_B}": {
            "YYYY/MM/01": "sum(lineItem/UsageAmount)",
            "YYYY/MM/02": "sum(lineItem/UsageAmount)",
            "YYYY/MM/03": "sum(lineItem/UsageAmount)",
            ...
        },
    }
    '''
    fields = ["lineitem/usageaccountid"]
    body = json.loads(request.body.decode('utf-8'))
    if not request.method == "POST":
        return JsonResponse(status=405, data={"Result": "Fail", "Code": "405"})

    if _is_missing_request_params(fields, body):
        return JsonResponse(status=400, data={"Result": "Fail", "Code": "400", "message":"missing required paremeters"})

    try :
        result = TableOutput.objects.values('product_ProductName','lineItem_UsageStartDate').order_by().annotate(sum=Sum('lineItem_UsageAmount'))
        response_data={
            "result": "Success", 
            "code": "0",
            "output": {},
        }        
        for c, l in groupby(result, itemgetter('product_ProductName')) :
            print(c, l)
            response_data["output"][c] = { dateutil.parser.parse(li['lineItem_UsageStartDate']).strftime('%Y-%m-%d') : li['sum'] for li in l }

        return JsonResponse(status=400, data=response_data)
    except Exception as e:
        print(e)
        return JsonResponse(status=400, data={"result": "Fail", "code": "400"})