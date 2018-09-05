import datetime
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

def histogram_by_topic(topic, start=None, end=None, interval='5s'):

    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=15)
    if not start:
        start = int((now - delta).timestamp() * 1000)
    if not end:
        end = int(now.timestamp() * 1000)
    query = {
            "aggs": {
                "histo": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "interval": int(interval),
                        "time_zone": "Asia/Tokyo",
                        "min_doc_count": 0,
                        "extended_bounds": {
                            "min": int(start),
                            "max": int(end),
                            }
                        }
                    }
                },
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {}
                            },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": start,
                                    "lte": end,
                                    "format": "epoch_millis"
                                    }
                                }
                            }
                        ],
                    }
                },
            }

    es = Elasticsearch(settings.ELASTICSEARCH_HOSTS)
    es_res = es.search(index=topic+"*", body=query)
    return [{'x': b['key_as_string'],'y': b['doc_count'], 'gruop': 0} for b in es_res['aggregations']['histo']['buckets']]
