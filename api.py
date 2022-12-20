# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 13:50:14 2022

@author: victor
"""

from flask import Flask,jsonify,request,render_template
import datetime
import time
import json
from requests import get

import os
import pandas as pd

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId #這東西在透過ObjectID去尋找的時候會用到

import pandas as pd
import requests

import numpy as np

from datetime import datetime
from datetime import timedelta
from datetime import date
MongoConnectUrl="mongodb://admin:bmwee8097218@140.118.122.115:30415/"
def MongoDB_ReadDataFromDB(DB, Collection, Search={}, Display={}, Sort=[]):
    # input範例
    # DB = 'xinxing_dispenser'
    # Collection = 'raw_data'
    # Search={'Timming':{'$gte': From, '$lte': To}, 'Dispenser':{'$regex':"^xinxing"}, 'CardID':CardID}
    # 比較複雜的Search
    # Search = {"Date":Date, 'Name':{'$not':re.compile("^any.*")}, '$and':[{"Percent":{'$ne':"nan%"}}, {"Percent":{'$ne':"0.0%"}}]}
    # Display={"CardID":1}
    # Sort=[("CardID",1)]
    # 正則表達式更多範例:
    # search = {"sort":"Program", "key":{'$regex':"^DS:A.*-ProgramStatus$"}} 
    # ^DS:A --> 以「DS:A」開頭 
    # .*    --> 這個部分隨便
    # -ProgramStatus$ --> 以「-ProgramStatus」結尾
    global MongoConnectUrl
    try:
        conn = MongoClient(MongoConnectUrl) 
        db = conn[DB]
        collection = db[Collection]
        if Sort!=[]:
            if Display == {}: #cursor裡面不要放Display不然會變成空白
                cursor = collection.find(Search).sort(Sort)
            else:
                cursor = collection.find(Search, Display).sort(Sort)
        else:
            if Display == {}: #cursor裡面不要放Display不然會變成空白
                cursor = collection.find(Search)
            else:
                cursor = collection.find(Search, Display)
    except:
        try:
            conn = MongoClient(MongoConnectUrl) 
            db = conn[DB]
            collection = db[Collection]
            if Sort!=[]:
                if Display == {}: #cursor裡面不要放Display不然會變成空白
                    cursor = collection.find(Search).sort(Sort)
                else:
                    cursor = collection.find(Search, Display).sort(Sort)
            else:
                if Display == {}: #cursor裡面不要放Display不然會變成空白
                    cursor = collection.find(Search)
                else:
                    cursor = collection.find(Search, Display)
        except:
            conn = MongoClient(MongoConnectUrl) 
            db = conn[DB]
            collection = db[Collection]
            if Sort!=[]:
                if Display == {}: #cursor裡面不要放Display不然會變成空白
                    cursor = collection.find(Search).sort(Sort)
                else:
                    cursor = collection.find(Search, Display).sort(Sort)
            else:
                if Display == {}: #cursor裡面不要放Display不然會變成空白
                    cursor = collection.find(Search)
                else:
                    cursor = collection.find(Search, Display)            
            
    #此處須注意，其回傳的並不是資料本身，你必須在迴圈中逐一讀出來的過程中，它才真的會去資料庫把資料撈出來給你。
    data = [d for d in cursor] #這樣才能真正從資料庫把資料庫撈到python的暫存記憶體中。
    if data==[]:
        return False
    else:
        return data

app = Flask(__name__)
PUBLIC_IP=get('https://api.ipify.org/').text
@app.route('/upload',methods=['POST'])
def SupplyuploadRawdata():
    global MongoConnectUrl
    request_data = request.get_json()
    Data={
            'Name': request_data['Name'],
            'Password': request_data['Password']
        }
    
    conn = MongoClient(MongoConnectUrl) 
    db = conn["victortry"]
    collection = db["Log"]
    collection.insert(Data)
    return jsonify("Success")
@app.route('/get', methods=['POST'])
def GET():
    try:
        _json = request.json
        _Id = _json['Name']
        print(_Id)
        data = MongoDB_ReadDataFromDB('victortry','Log',Search={'Name':_Id})
        if data==False:
            data="Nodata"
        else:
            for i in data:
    	        del i['_id']
    	
        print(data)
        res = jsonify({
                'code':200,
		'result':'Success!',
		'Data': data
		})
        return res
    except Exception as e:
        print(e)
app.run(host="140.118.122.115", port=5000) #host=PUBLIC_IP, 