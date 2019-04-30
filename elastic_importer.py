from elasticsearch import Elasticsearch
import requests

#res = requests.get('http://localhost:9200')
#print(res.content)

#connect to our cluster
#while r.status_code == 200:
    #r = requests.get('http://swapi.co/api/people/'+ str(i))
    #es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    #es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def connect_elasticsearch():
    es = None
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
       print("Connect")
    else:
       print("it don't connected!")


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
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='search', body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))


#Connect_elasticsearch();
