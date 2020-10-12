
from coronadisplay import chart, summarydata, sqldataformating, makebarchart,getplace,getdailydifference,getfactsdata,googleDataCalc
from django.shortcuts import render
import numpy as np
import mysql.connector as m
import time
from django.db.models import Max
from flask import json
import datetime
from .models import Coronastatedaily ,Districtdaily
from django.db.models import Q

def indiadashboard(request):
    subdate = Coronastatedaily.objects.aggregate(Max('date'))
    con = m.connect(host="localhost", user="username", passwd='svasnnmsjdcfjdDFGH!5548)', database="vikas")
    cur = con.cursor()
    cur.execute("desc coronastatedaily;")
    headeralldata = cur.fetchall()
    headerdata = np.array(headeralldata)
    header = headerdata[0:len(headerdata), 0]

    command2 = '''select * from coronastatedaily where date =(select max(date) from coronastatedaily);'''
    cur = con.cursor()
    cur.execute(command2)
    alldata = cur.fetchall()
    cur.close()
    con.close()
    completedatatorender = sqldataformating(alldata, header)

    p = summarydata()
    facts = getfactsdata("Coronaworld1", "India")
    
    stats=[]
    stats={'[India] Death Rate':"{:.2f}".format((p[3])/(p[3]+p[9])*100),'[India] Recovery Rate':"{:.2f}".format(p[9]/(p[3]+p[9])*100),'[India] Cases per Million':p[11],
'[World] Death Rate':"{:.2f}".format((p[1])/(p[10]+p[1])*100),'[World] Recovery Rate':"{:.2f}".format(p[10]/(p[10]+p[1])*100),'[World] Cases per Million':"{:.0f}".format(p[0]/6800)}
    
    obj=[]
    obj.append(Coronastatedaily.objects.filter(
        date=subdate['date__max']).values('loc', 'totalconfirmed',"discharged").order_by('-totalconfirmed')[:10])
    obj.append(Coronastatedaily.objects.filter(
        date=subdate['date__max']).values('loc', 'deaths').order_by('-deaths')[:60])



    googledata=googleDataCalc(obj[0],["State","Cases","Recovered"])
    googledata3=googleDataCalc(obj[1],["State","Deaths"])



    differencedata = getdailydifference('Coronaworld1', 'cases', 'date', fc1="country_name", pk1="India", orderby='-date', limit=60)
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j.date())
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","New cases"])
    googledata2=json.dumps(dd,default=str)
    
    differencedata = getdailydifference('Coronaworld1', 'deaths', 'date', fc1="country_name", pk1="India", orderby='-date', limit=60)
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j.date())
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","Daily Deaths"])
    googledata1=json.dumps(dd,default=str)

    
    return render(request, 'india.html',
                  { 'data1': completedatatorender[0], 'header1': completedatatorender[1][0],
                   'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4],'facts':facts,'stats':stats,
                                 'googledata':googledata,'title1':'States with Max Cases and Recoveries','type1':'bar','xlable1':"",
                                'googledata1':googledata1,'title2':'Daily Deaths','type2':'line','xlable2':'',
                                'googledata2':googledata2,'title3':'Daily cases','type3':'line','xlable3':"",
                                'googledata3':googledata3,'title4':'States with max Deaths','type4':'bar','xlable4':'','path':['India'],'a':p[2],'b':p[3],

                })






def indiastatedashboard(request):


    state1 = request.GET['name'].split(" ")
    state=getplace(state1)


    con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")
    cur = con.cursor()
    cur.execute("desc coronastatedaily;")
    headeralldata = cur.fetchall()
    headerdata = np.array(headeralldata)
    header = headerdata[0:len(headerdata), 0]
    command2 = '''select * from coronastatedaily where loc like "%{}%";'''.format(state)
    cur = con.cursor()
    cur.execute(command2)
    alldata = cur.fetchall()
    cur.close()
    con.close()
    completedatatorender = sqldataformating(alldata, header)
    p = summarydata(state=state)

    facts = getfactsdata("Coronastatedaily", state)

    obj=[]
    obj.append(Coronastatedaily.objects.filter(loc=f'{state}').values('date', 'totalconfirmed','discharged').order_by('-date')[:60:-1])
    googledata=googleDataCalc(obj[0],['Date','Cases','Recovered'])

    facts = getfactsdata("Coronastatedaily", state)
    differencedata = getdailydifference('Coronastatedaily', 'totalconfirmed', 'date', fc1="loc", pk1=state, orderby='-date', limit=60)
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j)
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","daily cases"])
    googledata1=json.dumps(dd,default=str)
    
    differencedata = getdailydifference('Coronastatedaily', 'deaths', 'date', fc1="loc", pk1=state, orderby='-date', limit=60)
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j)
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","daily Deaths"])
    googledata2=json.dumps(dd,default=str)
    '''
    ld=Coronastatedaily.objects.filter(loc=f'{state}').values('date', 'deaths','discharged','totalconfirmed').order_by('-date')[:1:-1]
    d=ld[0]['deaths']
    r=ld[0]['discharged']
    c=ld[0]['totalconfirmed']
    #p=ld[0]['population']
    #t=ld[0]['tested']
    print(d,r,c)

    if d==r!=0 or d!=r:
        stats={'Total cases':c,'Total Deaths':d,'Total Recovered':r,'Death Rate':"{:.2f}".format((d)/(d+r)*100),'Recovery Rate':"{:.2f}".format(r/(r+d)*100)}
    else:
        stats={'Total cases':c,'Total Deaths':d,'Total Recovered':r,'Death Rate':"NA",'Recovery Rate':"NA"}
    print(stats)



    return render(request, 'state.html',
                  {'data1': completedatatorender[0], 'header1': completedatatorender[1][0],
                   'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4],'facts':facts,
                        'googledata1':googledata1,'title2':'Daily cases','type2':'line','xlable2':"",
                         'googledata':googledata,'title1':'Total Cases','type1':'area','xlable1':"",
                           'googledata2':googledata2,'title3':'Daily Deaths','type3':'line','xlable3':"",'path':['India',state],'a':p[12],'b':p[13],'stats':stats,
                        
    '''
    differencedata = getdailydifference('Coronastatedaily', 'tested', 'date', fc1="loc", pk1=state, orderby='-date', limit=60)
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j)
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","daily tests"])
    googledata3=json.dumps(dd,default=str)

    ld=Coronastatedaily.objects.filter(loc=f'{state}').values('date', 'deaths','discharged','totalconfirmed','population','tested').order_by('-date')[:1:-1]
    d=ld[0]['deaths']
    r=ld[0]['discharged']
    c=ld[0]['totalconfirmed']
    po=ld[0]['population']
    te=ld[0]['tested']
    if d==r!=0 or d!=r:
        stats={'Total cases':c,'Total Deaths':d,'Total Recovered':r,'Death Rate':"{:.2f}".format((d)/(d+r)*100),'Recovery Rate':"{:.2f}".format(r/(r+d)*100),'Total Tests /1M':'{:.0f}'.format(te/po*1000000),'Deaths /1M Population':'{:.2f}'.format(d/po*1000000)}

    else:
        stats={'Total cases':c,'Total Deaths':d,'Total Recovered':r,'Death Rate':"NA",'Recovery Rate':"NA"}

    print(stats)

    return render(request, 'state.html',
                  {'data1': completedatatorender[0], 'header1': completedatatorender[1][0],
                   'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4],'facts':facts,
                        'googledata1':googledata1,'title2':'Daily cases','type2':'line','xlable2':"",
                         'googledata':googledata,'title1':'Total Cases','type1':'area','xlable1':"",
                           'googledata2':googledata2,'title3':'Daily Deaths','type3':'line','xlable3':"",'path':['India',state],'a':p[12],'b':p[13],'stats':stats,
                        'googledata3':googledata3,'title4':'Daily tests','type4':'line','xlable4':"",

})





def indiadistrictdashboard(request):


    state1 = request.GET['name'].split(" ")
    state=getplace(state1)

    commandlist=[{"command":f"select district,confirmed from districtdaily where state like '%{state}%' and date =(select max(date) from districtdaily ) order by confirmed desc limit 15;","xlable":"states","ylable":"Total Confirmed Cases","title":f"{str(state).upper()}-- TOTAL CONFIRMED CASES","chart_type":"bar"},
                 {"command":f"select district,active from districtdaily where state like '%{state}%' and date =(select max(date) from districtdaily ) order by active desc limit 15;","xlable":"Daily active Cases","ylable":"District","title":"TOP 15 Districts :Active Cases ","chart_type":"barh"}]
    paths = []
    for i in range(len(commandlist)):
        paths.append(
            makebarchart(commandlist[i]["command"], title=commandlist[i]["title"], xlable=commandlist[i]["xlable"],
                         ylable=commandlist[i]["ylable"], filename="district" + str(i + 1),chart_type=commandlist[i]["chart_type"]))

    con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")
    cur = con.cursor()
    cur.execute("desc districtdaily;")
    headeralldata = cur.fetchall()
    headerdata = np.array(headeralldata)
    header = headerdata[0:len(headerdata), 0]

    command2 = '''select * from districtdaily where state like "%{}%" and date =(select max(date) from districtdaily);'''.format(state)

    cur = con.cursor()
    cur.execute(command2)
    alldata = cur.fetchall()

    cur.close()
    con.close()
    completedatatorender = sqldataformating(alldata, header)
    p = summarydata(state=state)

    return render(request, 'district.html',
                  {'user_images': paths, 'data1': completedatatorender[0], 'header1': completedatatorender[1][0],
                   'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4],'path':['India',state],'a':p[12],'b':p[13],})


def indiadistrictdetaildashboard(request):
    district1 = request.GET['name'].split(" ")
    statedistrict=getplace(district1).split(" ")
    con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")
    cur = con.cursor()
    partition_index=0
    leng=0
    for i in range(1,9):
        state=" ".join(statedistrict[:i])
        district=" ".join(statedistrict[i:])

        command2 = '''select * from districtdaily where state = "{}" and district ="{}" ;'''.format(state,district)

        cur = con.cursor()
        cur.execute(command2)
        alldata = cur.fetchall()
        if len(alldata)>leng:
            leng = len(alldata)
            partition_index=i
    state = " ".join(statedistrict[:partition_index])
    district = " ".join(statedistrict[partition_index:])


    subdate = Districtdaily.objects.aggregate(Max('date'))
    obj=[]
    obj.append(Districtdaily.objects.filter (district=f'{district}').filter(state=f'{state}').values('date', 'confirmed').order_by('-date')[:60:-1])
    googledata=googleDataCalc(obj[0],['date','Cases'])


    cur.execute("desc districtdaily;")
    headeralldata = cur.fetchall()
    headerdata = np.array(headeralldata)
    header = headerdata[0:len(headerdata), 0]

    command2 = '''select * from districtdaily where state ="{}"  and district ="{}" order by date desc;'''.format(state,district)

    cur = con.cursor()
    cur.execute(command2)
    alldata = cur.fetchall()

    cur.close()
    con.close()
    completedatatorender = sqldataformating(alldata, header)

    p = summarydata(state=state,district=district)

    facts=getfactsdata("Districtdaily",state,district)
    differencedata=getdailydifference('Districtdaily', 'confirmed', 'date',fc1="state", pk1=state,fc2="district", pk2=district, orderby='-date', limit=60)
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j)
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","New cases"])
    googledata2=json.dumps(dd,default=str)

    differencedata=getdailydifference('Districtdaily', 'deceased', 'date',fc1="state", pk1=state,fc2="district", pk2=district, orderby='-date', limit=60)
    nar=[]
    nar2=[]
    for i in differencedata[1]:
        nar.append(int(i))
    for j in differencedata[0]:
        nar2.append(j)
    dd=list(map(lambda i:list(i),list(zip(nar2,nar))))
    dd.insert(0,["Date","New Deaths"])
    googledata1=json.dumps(dd,default=str)

    ld=Districtdaily.objects.filter (district=f'{district}').filter(state=f'{state}').values('date', 'deceased','recovered','confirmed','active','population','tested').order_by('-date')[:1:-1]
    d=ld[0]['deceased']
    r=ld[0]['recovered']
    c=ld[0]['confirmed']
    a=ld[0]['active']
    po=ld[0]['population']
    te=ld[0]['tested']

    stats={'Total cases':c,'Active Cases':a,'Total Deaths':d,'Total Recovered':r}
    try:
        stats['Death Rate']="{:.2f}".format((d)/(d+r)*100)
    except:
        pass
    try:
        stats['Tests per 1M Population']="{:.0f}".format((te)/po*1000000)
    except:
        pass
    try:
        stats['Deaths Per 1M Population']="{:.2f}".format((d)/po*1000000)
    except:
        pass



    adddata={'add':0}
    if district=="Jaipur" or district=="Gurugram": 
        adddata={"add":1,"image":"gurgaon.jpg",'href':"https://legacytech.in"}

    return render(request, 'districtdata.html',
                  { 'data1': completedatatorender[0], 'header1': completedatatorender[1][0],
                   'wt': p[0], 'wd': p[1], 'it': p[2], 'id': p[3], 'd': p[4],'facts':facts,
                                 'googledata':googledata,'title1':'Total Cases','type1':'area','xlable1':"",
                                 'googledata2':googledata2,'title3':'Daily Cases','type3':'line','xlable3':"",
                                 'googledata1':googledata1,'title2':'Daily Deaths','type2':'line','xlable2':"",'path':['India',state,district],'a':p[12],'b':p[13],'adddata':adddata,'stats':stats,

})








