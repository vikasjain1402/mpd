from django.shortcuts import render
from coronadisplay import summarydata
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
import time
import datetime

def about(request):
    t1=time.perf_counter()
    def uuu():
        client.vikas.about.remove()
        p=summarydata()
        newtimediffer=(datetime.datetime.now()-p[-1])
        x='{:.0f} minutes'.format ((  (newtimediffer.days*3600*24)+newtimediffer.seconds ) /60)
        data={'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': x}
        client.vikas.about.insert_one(data)
        return data 


    p = summarydata(check="world")
    oldValue=client.vikas.about.find_one({"wt":p[0]},{"_id":0})

    if oldValue is not None:
        if oldValue['wt']==p[0]:
            data=oldValue
            newtimediffer=(datetime.datetime.now()-p[-1])
            x='{:.0f} minutes'.format ((  (newtimediffer.days*3600*24)+newtimediffer.seconds ) /60)
            data['d']=x

        else:
            data=uuu()
    else:
        data=uuu()
    print("about",time.perf_counter()-t1)
    return render(request, 'about1.html',data)

    '''
    p = summarydata()

    return render(request, 'about1.html',{'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4]})
    '''

def tac(request):
    print("tac")
    return render(request, 'tac.html')



def search(request):
    p=summarydata()
    import mysql.connector as m
    con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")
    cur = con.cursor()
    commands=[]
    commands.append("select distinct(country_name) from coronaworld1 where date=(select max(date) from coronaworld1);")
    commands.append("select distinct(loc) from coronastatedaily where date=(select max(date) from coronastatedaily);")
    commands.append("select distinct state,district from districtdaily where date=(select max(date) from districtdaily);")

    data1={}
    cur.execute(commands[1])
    data = cur.fetchall()
    for  i in data:
        data1[i[0]]=f'/india/state?name={i[0]}'.replace(" ","%20") 
    cur.execute(commands[2])
    data = cur.fetchall()
    for  i in data:
        data1["["+i[0]+"] "+i[1]]=f'/india/districtdetail?name={i[0]+" "+i[1]}'.replace(" ","%20")

    cur.execute(commands[0])
    data = cur.fetchall()
    for  i in data:
        data1[i[0]]=f'/world/country?name={i[0]}'.replace(" ","%20")




    return render(request, 'search.html',{'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4],'data':data1,'path':['Search',]})
