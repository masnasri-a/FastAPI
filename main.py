from elasticsearch import Elasticsearch
from fastapi import FastAPI
import uvicorn
import json

app = FastAPI()
es = Elasticsearch('http://localhost:9200/')


@app.get("/get_account")
def read_root():
    data = es.search(index="ta_identity",body={"query":{"match_all":{}}})
    hits = data['hits']['hits']
    return hits

@app.get("/search_account")
def search_id(username: str, password: str):
    data = es.search(index="ta_identity",body={"query":{"bool":{"must":[{"match":{"data.id":username}},{"match":{"data.password":password}}]}}})
    return data['hits']['hits']

@app.post("/register_account")
def register(name:str,username:str,email:str,password:str,number:str):
    total = es.search(index="ta_identity",body={"query":{"match_all":{}}})
    totals = total['hits']['total']
    val = totals['value']
    newId = val + 1
    data = es.index(index="ta_identity",id=newId, body={"data":{"name":name,"id":username,"email":email,"password":password,"number":number}})
    return {"status":"data has been created"}

@app.delete("/delete_account")
def delete_account(username:str):
    get_id = es.search(index="ta_identity",body={"query":{"match":{"data.id":username}}})
    data = json.dumps(get_id['hits']['hits'])
    x= json.loads(data)
    id = x[0]['_id']
    es.delete(index="ta_identity", id=id)
    return "delete "+id+" has success"

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8899)

