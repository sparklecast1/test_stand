from elasticsearch import Elasticsearch
import requests
import logging
import json
import pymysql.cursors

#connect to our cluster
#while r.status_code == 200:
    #r = requests.get('http://swapi.co/api/people/'+ str(i))
    #es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    #es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def connect_mysql():
    #mysql.connector.connect(host='localhost',database='test',user='root',password='123456Aa')
    connection = pymysql.connect(host='localhost',
                             user='root',
                              password='123456Aa',
                               db='test',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
                                
    sql = "SELECT * FROM search "
    #connection = connection.getConnection()
    cursor = connection.cursor()
    
    # Выполнить sql и передать 1 параметр.
    #cursor.execute(sql, ( 10 ) )
    cursor.execute(sql)
    print ("cursor.description: ", cursor.description)

    for row in cursor:
        data = {
           "id": row["id"],
           "name": row["name"],
           "surname": row["surname"],
           "country": row["country"],
           "last_update": row["last_update"],
           "data": row["data"],
        }
        res = es.index(index='search', doc_type='members',  body=data)
        #return connection
        #id | name   | surname | country | last_update | data
        #print(row)
        #print (" ----------- ")
        #print("Row: ", row)
        #print ("id: ", row["id"])
        #print ("name: ", row["name"])
        #print ("surname: ", row["surname"])
        #print ("country: ", row["country"])
        #print ("last_update: ", row["last_update"])
        #print ("data: ", row["data"])



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
#                "dynamic": "strict",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "keyword"
                    },
                    "surname": {
                        "type": "keyword"
                    },
                    "country": {
                        "type": "keyword"
                    },
                    "last_update": {
                        "type": "date"
                    },
                    "data": {
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
    #connect and create index
    es = connect_elasticsearch()
    create_index(es, 'search')


    try:
        connect_mysql()
        print('Connect to mysql is seccesfull')
    except Exception as ex:
        print('Error connecting to mysql')


    #data = {
    #   "user_id": "1",
    #   "text": "test",
    #   "id_user": "23123",
    #}

    #try:
    #    #res = es.index(index="search", doc_type="members", id=1, body=data)
    #    res = es.index(index="search",  body=data)
    #    print('Data importing seccesfull')
    #except Exception as ex:
    #    print('Error in import data')



    if es is not None:
        search_object = '''{'query': {'match': {'id': '1'}}}'''
        #se = search(es, 'search', json.dumps(search_object))
        res = es.search(index="search", body={"query": {'match': {'id': '5'}}})
        #print(res['hits']['total']['value'])
        print(res)





