from django.shortcuts import render
from coronadisplay import sqldataformating,summarydata,makebarchart,googleDataCalc
import mysql.connector as m
import numpy as np
import time
from django.db.models import Max
from flask import json
import datetime
from .models import Coronaworld1


from pymongo import MongoClient
client = MongoClient('localhost', 27017)

def home(request):
    def uuu():
            p=summarydata()
            client.vikas.world.remove()
            subdate = Coronaworld1.objects.aggregate(Max('date'))
            obj=[]
            obj.append(Coronaworld1.objects.filter(
                date=subdate['date__max']).values('country_name', 'cases','total_recovered').order_by('-cases')[:20])
            obj.append(Coronaworld1.objects.filter(
                date=subdate['date__max']).values('country_name', 'total_cases_per_1m_population').order_by('-total_cases_per_1m_population')[:20])
            obj.append(Coronaworld1.objects.filter(
                date=subdate['date__max']).values('country_name', 'deaths_per_1m_population').order_by('-deaths_per_1m_population')[:20])

            googledata1=googleDataCalc(obj[0],["Country","Cases","Recovered"])
            googledata2=googleDataCalc(obj[1],["Country","Cases / 1M"])
            googledata=googleDataCalc(obj[2],["Country","Deaths  /1M"])
            con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")

 
            cur = con.cursor()
            cur.execute("desc coronaworld1;")
            headeralldata = cur.fetchall()
            headerdata = np.array(headeralldata)
            header = headerdata[0:len(headerdata),0]

            command2 = '''select * from coronaworld1 where date=(select max(date) from coronaworld1);'''
            cur = con.cursor()
            cur.execute(command2)
            alldata = cur.fetchall()
            cur.close()
            con.close()
            completedatatorender = sqldataformating(alldata, header)
            newtimediffer=(datetime.datetime.now()-p[-1])
            x='{:.0f} minutes'.format ((  (newtimediffer.days*3600*24)+newtimediffer.seconds ) /60)
            data={'data1': completedatatorender[0],
                'header1': completedatatorender[1][0],
                   'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': x,
                                'googledata1':googledata1,'title2':'Top countries with max cases/Recoveries','type2':'bar','xlable2':'',
                                'googledata2':googledata2,'title3':'Top countries with max cases per Million ','type3':'bar','xlable3':'',
            'googledata':googledata,'title1':'Top countries with max Deaths per Million ','type1':'bar','xlable1':'','path':['World'],'a':p[0],'b':p[1]}
            client.vikas.world.insert_one(data)

            return data

    p=summarydata(check="world")
    oldValue=client.vikas.world.find_one({"wt":p[0]},{"_id":0})
    if oldValue is not None:    
        if oldValue['wt']==p[0]:
            data=oldValue
            newtimediffer=(datetime.datetime.now()-p[-1])
            x='{:.0f} minutes'.format ((  (newtimediffer.days*3600*24)+newtimediffer.seconds ) /60)
            data["d"]=x
        else:
            data=uuu()
    else:
        data=uuu()
    return render(request, 'home.html',data)



