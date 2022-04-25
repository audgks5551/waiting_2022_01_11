from django.db.models import Case, When

#
from elasticsearch import Elasticsearch
from jamo import h2j, j2hcj

#
from . import models
from . import search


def elasticsearch_search(keyword, amenity_list, theme_list, taste_list):

    query = search.search_query(keyword, amenity_list, theme_list, taste_list)
    elasticsearch = Elasticsearch(
        "http://118.67.143.41:9200", http_auth=('elastic', 'elasticpassword'),)

    response = elasticsearch.search(
        index="waiting_2022_01_11__stores_store__v1",
        query=query,
        _source=["id", "name", "highlight"],
        size=100
    )

    result_list_1 = []
    for hit in response['hits']['hits']:
        try:
            result_list_1.append(hit["highlight"]["nameNgram"])
        except:
            result_list_1.append(hit["_source"]["name"])

    result_list_2 = []
    for hit in response['hits']['hits']:
        result_list_2.append(hit["_source"]["id"])

    order = Case(*[When(id=id, then=pos)
                   for pos, id in enumerate(result_list_2)])

    queryset = models.Store.objects.filter(
        id__in=result_list_2).order_by(order)

    return queryset, result_list_1


def elasticsearch_completion(keyword):

    query = search.completion_query(keyword)
    elasticsearch = Elasticsearch(
        "http://101.101.216.187:9200", http_auth=('elastic', 'elasticpassword'),)

    response = elasticsearch.search(
        index="waiting_2022_01_11__stores_store__v1",
        query=query,
        size=10,
        highlight={
            "fields": {
                "nameNgram": {}
            }
        },
        _source=["id", "name", "highlight"]
    )

    result_list = []
    for hit in response['hits']['hits']:
        try:
            result_list.append(hit["highlight"]["nameNgram"])
        except:
            result_list.append(hit["_source"]["name"])
    print(result_list)
    return result_list


def getJamo(keyword):

    jamo_str = j2hcj(h2j(keyword))

    return jamo_str


def getChosung(text):

    CHOSUNG_START_LETTER = 4352
    JAMO_START_LETTER = 44032
    JAMO_END_LETTER = 55203
    JAMO_CYCLE = 588

    def isHangul(ch):

        return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER

    result = ""

    for ch in text:

        if isHangul(ch):  # 한글이 아닌 글자는 걸러냅니다.

            # python2: result += unichr((ord(ch) - JAMO_START_LETTER)/JAMO_CYCLE + CHOSUNG_START_LETTER)

            result += chr(int((ord(ch) - JAMO_START_LETTER) /
                          JAMO_CYCLE + CHOSUNG_START_LETTER))

    return result


def search_query(keyword, amenity_list, theme_list, taste_list):

    jamo = getJamo(keyword)

    # if store_type_list == []:
    #    store = {'terms': {'store_type': ['기본']}}
    # else:
    #    store = {'terms': {'store_type': store_type_list}}

    if amenity_list == []:
        amenity = {"terms": {"amenity": ["기본"]}}
    else:
        amenity = {"terms": {"amenity": amenity_list}}

    if theme_list == []:
        theme = {"terms": {"theme": ["기본"]}}
    else:
        theme = {'terms': {'theme': theme_list}}

    if taste_list == []:
        taste = {"terms": {"taste": ["기본"]}}
    else:
        taste = {"terms": {"taste": taste_list}}

    query = {

        "bool": {
            "filter": [amenity, theme, taste],

            "should": [
                {"match": {"nameNori": keyword}},
                {"term": {"nameChosung": keyword}},
                {"term": {"nameJamo": keyword}},

                {"match": {"menuNori": keyword}},
                {"term": {"menuChosung": keyword}},
                {"term": {"menuJamo": keyword}},

                {"match": {"storetypeNori": keyword}},
                {"term": {"storetypeChosung": keyword}},
                {"term": {"storetypeJamo": keyword}},

                {"match": {"foodtypeNori": keyword}},
                {"term": {"foodtypeChosung": keyword}},
                {"term": {"foodtypeJamo": keyword}},

                {"match": {"amenityNori": keyword}},
                {"term": {"amenityChosung": keyword}},
                {"term": {"amenityJamo": keyword}},

                {"match": {"tasteNori": keyword}},
                {"term": {"tasteChosung": keyword}},
                {"term": {"tasteJamo": keyword}},

                {"match": {"themeNori": keyword}},
                {"term": {"themeChosung": keyword}},
                {"term": {"themeJamo": keyword}},

                {"match": {"addressNori": keyword}}

            ],

            "minimum_should_match": 1
        }

    }

    return query


def completion_query(keyword):

    jamo = getJamo(keyword)
    chusong = getChosung(keyword)

    query = {
        "bool": {

            "should": [
                {"prefix": {"name": keyword}},
                {"term": {"name": keyword}},
                {"term": {"nameNgram": keyword}},
                {"term": {"nameNgramEdge": keyword}},
                {"term": {"nameNgramEdgeBack": keyword}},
                {"term": {"nameChosung": keyword}},
                {"term": {"nameJamo": keyword}}
            ],

            "minimum_should_match": 1
        }

    }

    return query
