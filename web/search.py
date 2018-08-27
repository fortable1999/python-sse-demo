from elasticsearch import Elasticsearch
import settings

def search_by_querystr(query_str):
    query = {
        "query": {
            "query_string" : {
                "default_field" : "message",
                "query" : query_str
            }
        }
    }
    es = Elasticsearch(settings.ELASTICSEARCH_HOSTS)
    es_res = es.search(index="*", body=query)
    return [hit['_source']['message'] for hit in es_res['hits']['hits']]
