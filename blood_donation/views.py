__author__ = 'naveenkumar'

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch
from mappings import *

es_host = "http://localhost:9200"

es_client = Elasticsearch(es_host, timeout=30)
es_index = "blood_donation_index"

@api_view(['GET'])
def get_started(request):
    return Response(data={"status": 1}, status=status.HTTP_201_CREATED, content_type='application/json')

@api_view(['POST'])
def signup(request):
    data = request.data
    body = {
        "unique_id" : data.get("unique_id"),
        "name": data['name'],
        "email": data.get("email", ""),
        "blood_group": data['blood_group'],
        "last_donation_date": data.get("last_donation_date", None),
        "locations": data["locations"]
    }
    res = es_client.create(es_index, doc_type=get_user_mapping(), body=body)
    return Response(data=res, status=status.HTTP_201_CREATED, content_type='application/json')


@api_view(['POST'])
def new_blood_req(request):
    pass

@api_view(['POST'])
def donor_response(request):
    pass

@api_view(['POST'])
def recipeint_feedback(request):
    pass


@api_view(['POST'])
def find_coupon(request):
    data = request.data
    mer = data.get("merchant")
    min_order = data.get("min_order")
    user_type = data.get("user_type")
    cat = data.get("cat")
    recipient_id = data.get("recipient_id")
    detail_type = data.get("detail_type")

    body = {
        "from": 0,
        "size": 10,
       "query": {
           "filtered": {
              "query": {
                  "bool": {
                      "should": [
                         {
                             "match": {
                                "description": cat
                             }
                         },
                         {
                             "multi_match": {
                                "query": "minimum purchase value " + min_order,
                                "fields": [
                                   "descrption", "short_description"
                                ]
                             }
                         },
                         {
                             "multi_match": {
                                "query": "valid on purchase of " + min_order + "and above",
                                "fields": [
                                   "descrption", "short_description"
                                ]
                             }
                         }
                      ]
                  }
              },
              "filter": {
                  "bool": {
                  "should": [
                     {
                         "term": {
                            "merchant": mer
                         }
                     },
                     {
                        "term":{
                             "tags": cat
                         }
                     }
                  ]
                  }
              }
           }
       }
    }
    res = es_client.search(index="coupons_index", doc_type="coupon", body=body)
    hits = res['hits']['hits']
    res_to_be_sent = []
    for hit in hits:
        source = hit['_source']
        each_res_body = {
            "company": source['merchant'],
            "coupon_code": source["code"],
            "discount": source["discount"],
            "descption": source["description"]
        }
        res_to_be_sent.append(each_res_body)
    print(res_to_be_sent)
    res_final =  {
        "detail_type": detail_type,
        "recipient_id": recipient_id,
        "coupons": res_to_be_sent
    }
    return Response(data=res_final, status=status.HTTP_200_OK, content_type='application/json')
