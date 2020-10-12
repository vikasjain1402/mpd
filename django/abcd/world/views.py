from django.shortcuts import render
from .models import picture,Coronaworld1
import numpy as np
from coronadisplay import chart, summarydata, sqldataformating, getplace,getdailydifference,googleDataCalc
from django.db.models import Max
import mysql.connector as m
from flask import json
import datetime
import time
def worlddashboard(request):

    return render(request,'sitemap.xml')


def countrydashboard(request):
    
    country1=request.GET['name'].split(" ")
    country=getplace(country1)
    print(country)
    subdate = Coronaworld1.objects.aggregate(Max('date'))
    obj=[]
    obj.append(Coronaworld1.objects.filter(
        country_name__contains='{}'.format(country)).values('date', 'cases').order_by('-date')[:20:-1])
    obj.append(Coronaworld1.objects.filter(
        date=subdate['date__max']).values('country_name', 'cases','total_recovered').order_by('-cases')[:20])
    googledata=googleDataCalc(obj[0],["Date","Cases"])
    googledata1=googleDataCalc(obj[1],["Country","Cases","Total Recovered"])

    con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")
    cur = con.cursor()
    cur.execute("desc coronaworld1;")
    headeralldata = cur.fetchall()
    headerdata = np.array(headeralldata)
    header = headerdata[0:len(headerdata), 0]

    command2 = '''select * from coronaworld1 where country_name like "%{}%" ;'''.format(country)
    cur = con.cursor()
    cur.execute(command2)
    alldata = cur.fetchall()
    cur.close()
    con.close()

    completedatatorender = sqldataformating(alldata, header)
    p = summarydata(country=country)

    
    differencedata = getdailydifference('Coronaworld1', 'cases', 'date', fc1="country_name", pk1=country,orderby='-date', limit=20)
    
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j.date())
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","New cases"])
    googledata2=json.dumps(dd,default=str)
    print(p)
   
    return render(request, 'country.html',
                  {'data1': completedatatorender[0],
                'header1': completedatatorender[1][0],
                   'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4],
                                'googledata':googledata,'title1':'Total Cases','type1':'area',
                                'googledata1':googledata1,'title2':'Top countries with max cases','type2':'bar','xlable2':'countries',
                                'googledata2':googledata2,'title3':'Daily cases','type3':'line','path':['world',country],'a':p[12],'b':p[13],

                })
   
