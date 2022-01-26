from django.db.models import Case, When

#
from elasticsearch import Elasticsearch
from jamo import h2j, j2hcj

#
from . import models
from . import search


def elasticsearch_search(keyword, amenity_list, theme_list, taste_list):

    query = search.query(keyword, amenity_list, theme_list, taste_list)
    elasticsearch = Elasticsearch(
        "http://127.17.0.1:9200", http_auth=('elastic', 'elasticpassword'),)

    response = elasticsearch.search(
        index="waiting_2022_01_11__stores_store__v1",
        query=query
    )

    result_list = []
    for hit in response['hits']['hits']:
        result_list.append(hit["_source"]["id"])

    order = Case(*[When(id=id, then=pos)
                   for pos, id in enumerate(result_list)])

    queryset = models.Store.objects.filter(
        id__in=result_list).order_by(order)
    
    return queryset


def getJamo(keyword):

    jamo_str = j2hcj(h2j(keyword))

    return jamo_str


def query(keyword, amenity_list, theme_list, taste_list):

    jamo = getJamo(keyword)
    
    #if store_type_list == []:
    #    store = {'terms': {'store_type': ['기본']}}
    #else:
    #    store = {'terms': {'store_type': store_type_list}}

    if amenity_list == []:
        amenity = {'terms': {'amenity': ['기본']}}
    else:
        amenity = {'terms': {'amenity': amenity_list}}

    if theme_list == []:
        theme = {'terms': {'theme': ['기본']}}
    else:
        theme = {'terms': {'theme': theme_list}}

    if taste_list == []:
        taste = {'terms': {'taste': ['기본']}}
    else:
        taste = {'terms': {'taste': taste_list}}
        
    query = {

        "bool": {

            "filter": [
                amenity,
                theme,
                taste
            ],

            "should": [

                {
                    "match": {"nameNori": keyword}
                }

            ],

            "minimum_should_match": 1
        }

    }

    return query
