from django.db.models import Case, When

#
from elasticsearch import Elasticsearch
from jamo import h2j, j2hcj

#
from . import models
from . import search


def elasticsearch_search(keyword, store_type_list, amenity_list, theme_list, taste_list):

    query = search.query(keyword, store_type_list,
                         amenity_list, theme_list, taste_list)
    elasticsearch = Elasticsearch(
        "http://127.0.0.1:9200", http_auth=('elastic', 'elasticpassword'),)

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


def query(keyword, store_type_list,
          amenity_list, theme_list, taste_list):

    jamo = getJamo(keyword)

    if store_type_list == []:
        store_type_list.append("기본")
    if amenity_list == []:
        amenity_list.append("기본")
    if theme_list == []:
        theme_list.append("기본")
    if taste_list == []:
        taste_list.append("기본")

    query = {

        "bool": {

            "filter": [

                {
                    "terms": {"store_type": store_type_list}
                },

                {
                    "terms": {"amenity": amenity_list}
                },

                {
                    "terms": {"theme": theme_list}
                },

                {
                    "terms": {"taste": taste_list}
                }

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
