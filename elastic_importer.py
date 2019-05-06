from elasticsearch import Elasticsearch
import requests
import logging
import json

#connect to our cluster
#while r.status_code == 200:
    #r = requests.get('http://swapi.co/api/people/'+ str(i))
    #es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    #es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
       print("Connect")
    else:
       print("it don't connected!")
    return _es

def create_index(es_object, index_name='search'):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "members": {
                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "id_user": {
                        "type": "integer"
                    },
                    "text": {
                        "type": "text"
                    },
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        else:
            print('Failed creation')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='search', body=record)
        print('Importing succesfull')
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        
def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    es = connect_elasticsearch()
    create_index(es, 'search')
    data = {
       'user_id': '1',
       'test': 'test'
    }
    store_record(es, 'search', data)
    #if es is not None:
    search_object = {'query': {'match': {'iser_id': '1'}}}
    se = search(es, 'search', json.dumps(search_object))
    print(se)
        
    