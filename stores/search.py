from django.db.models import Case, When

#
from elasticsearch import Elasticsearch

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
    print(result_list)
    order = Case(*[When(id=id, then=pos)
                   for pos, id in enumerate(result_list)])

    queryset = models.Store.objects.filter(
        id__in=result_list).order_by(order)

    return queryset


def query(keyword, store_type_list,
          amenity_list, theme_list, taste_list):

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
                },

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
