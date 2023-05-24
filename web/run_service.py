from flask import Flask,request
import json

from flask_restful import reqparse,abort,Api,Resource
import torch
import jieba
from transformers import BertTokenizerFast
from models.model import MRC_model
from mrc import predictfunc
from service import search

import socket

app=Flask(__name__)
api=Api(app)

app=Flask(__name__)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizerFast.from_pretrained("bert-base-chinese")
fine_tunning_model = "output/best_model.pkl"
model = MRC_model("bert-base-chinese")
model.to(device)
model.load_state_dict(torch.load(fine_tunning_model))
model.eval()

def get_answer(title,context,question):
    core = {'qas': [{'question': question, 'id': 'test'}], 'context': context, 'title': title}
    testdata = [{'title': '', 'paragraphs': [core]}]
    return predictfunc(testdata,model,tokenizer)


@app.route("/test",methods=["post"])
def check():
    get_data=request.get_data()
    param=get_data.decode('utf-8')
    parameter=json.loads(param)
    print(parameter)
    if parameter is not None:
        keys=parameter['data'][0]
        docs=search(keys)
        if docs=='no result':
            return json.dumps({'code':500,'error_info':'no result'},ensure_ascii=False)
        if docs == 'no search keys':
            json.dumps({'code': 500, 'error_info': 'no search keys'}, ensure_ascii=False)
        if docs == 'search error':
            json.dumps({'code': 500, 'error_info': 'search error'}, ensure_ascii=False)
        title=docs[0]['title']
        context=docs[0]['description']
        answer=get_answer(title,context,keys)
        return json.dumps({'code':200,'docs':docs,'qa':{'question':keys,'answer':answer,'source':title,'context':context}},ensure_ascii=False)
    else:
        print('参数为空')
        return json.dumps({'code':500,'error_info':'no parameter'},ensure_ascii=False)




def get_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    jieba.initialize()
    ip=get_ip()
    app.run(debug=True,host=ip,port=5003)



