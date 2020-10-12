
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import datetime
import mysql.connector as m
from mysql.connector import Error
matplotlib.use('Agg')
from pytz import timezone
from flask import json


def googleDataCalc(twoDArray,colList):
    uu=[]
    for k in twoDArray:
        u=[]
        for key,value in k.items():
            try:
                temp=eval(value)
            except:
                if isinstance(value,datetime.datetime):
                    value=value.date()
                u.append(value)
            else:
                u.append(temp)
        uu.append(u)
    uu.insert(0,colList)
    return json.dumps(uu,default=str)



def sqldataformating(sqldata, header=[]):
    npdata1 = np.array(sqldata)
    length = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0]
    for i in npdata1:
        for j in range(len(i)):
            if length[j] < len(str(i[j])):
                length[j] = len(str(i[j]))

    for j in range(len(header)):

        if length[j] < len(str(header[j])):
            length[j] = len(str(header[j]))

    renderdata = []
    headerdata = []
    for i in range(len(npdata1)):
        renderdata.append("  ".join(
            list(map(lambda j, k: [str(j).ljust(k), str(j).rjust(k)][isinstance(j, int)], npdata1[i], length))))
    for i in range(len(header)):
        headerdata.append("  ".join(list(map(lambda j, k: str(j).capitalize().center(k), header, length))))
    return [renderdata, headerdata]


def makebarchart(command, title="", xlable="", ylable="", filename="anonymus",chart_type="barh"):
    con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")
    cur = con.cursor()
 
    try:
        cur.execute(command)
    except Error as e:
        print(e)
        cur.close()
        con.close()
    else:
        data = cur.fetchall()
        npdata = np.array(data)

        plt.title(title,color="#ac77f9",fontsize=18)
        plt.tick_params(colors="white")
        plt.grid(color='black', linestyle='-.', linewidth=.2)
        plt.xlabel(xlable,color="white",fontsize=14)
        plt.ylabel(ylable,color="white",fontsize=14)
        plt.xticks(rotation=60,ha='right')
  
        axis2 = list(map(lambda i: str(i.item()), npdata[0:, 1:2]))[::-1]
        axis1 = list(map(lambda i: str(i.item()), npdata[0:, 0:1]))[::-1]
        if isinstance(axis1[0], datetime.date):
            axis1 = list(map(lambda i: str(i.year) + ":" + str(i.month) + ":" + str(i.day), axis1))
        if isinstance(axis2[0], datetime.date):
            axis2 = list(map(lambda i: str(i.year) + ":" + str(i.month) + ":" + str(i.day), axis2))

        try:
            eval(axis1[0])
        except:
            eval(axis2[0])
            axis2 = list(map(lambda i: int(i), axis2))

            if chart_type=="barh":
                plt.barh(axis1, axis2, align="center", color="#ac77f9")
            elif chart_type=="bar":
                plt.bar(axis1, axis2, align="center", color="#ac77f9")
            elif chart_type=="plot":
                plt.plot(axis1, axis2, color="b",  linewidth=3)



        else:
            axis1 = list(map(lambda i: int(i), axis1))
            plt.xlim(0, max(axis1) * 1.01)


            if chart_type == "barh":
                plt.barh(axis2, axis1, align="center", color="#ac77f9")

            elif chart_type == "bar":
                plt.bar(axis2, axis1, align="center", color="#ac77f9")

            elif chart_type=="plot":
                plt.plot(axis2, axis1, color="#ac77f9", linewidth=3)


        plt.savefig("/mpd/site/public/static/{}.png".format(filename), dpi=90, bbox_inches='tight', transparent=True)
        t = datetime.datetime.now()
        plt.close()

        return "{}.png".format(filename) + "?" + str(t)


def summarydata(state='', district='',country='',check=''):
    
    commands=[]
    if check=="world":
         commands.append("select sum(cases) from coronaworld1 where date=(select max(date) from coronaworld1);")
         commands.append("select max(date) from coronaworld1;")
    else:
        commands=[]
        commands.append("select sum(cases) from coronaworld1 where date=(select max(date) from coronaworld1);")
        commands.append("select sum(deaths) from coronaworld1 where date=(select max(date) from coronaworld1);")
        commands.append("select sum(cases) from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
        commands.append("select sum(deaths) from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
        commands.append("select max(date) from coronaworld1;")

        commands.append("select sum(new_deaths) from coronaworld1 where date=(select max(date) from coronaworld1);")
        commands.append("select sum(new_cases) from coronaworld1 where date=(select max(date) from coronaworld1);")
        commands.append("select new_cases from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
        commands.append("select new_deaths from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
        commands.append("select total_recovered from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
        commands.append("select sum(total_recovered) from coronaworld1 where date=(select max(date) from coronaworld1);")
        commands.append("select total_cases_per_1m_population from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
    ''' 
    commands=[]
    commands.append("select sum(cases) from coronaworld1 where date=(select max(date) from coronaworld1);")
    commands.append("select sum(deaths) from coronaworld1 where date=(select max(date) from coronaworld1);")
    commands.append("select sum(cases) from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
    commands.append("select sum(deaths) from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
    commands.append("select max(date) from coronaworld1;")

    commands.append("select sum(new_deaths) from coronaworld1 where date=(select max(date) from coronaworld1);")
    commands.append("select sum(new_cases) from coronaworld1 where date=(select max(date) from coronaworld1);")
    commands.append("select new_cases from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
    commands.append("select new_deaths from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
    commands.append("select total_recovered from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
    commands.append("select sum(total_recovered) from coronaworld1 where date=(select max(date) from coronaworld1);")
    commands.append("select total_cases_per_1m_population from coronaworld1 where date=(select max(date) from coronaworld1) and country_name='India';")
    '''
    if district!='' and state!='':
        commands.append(f"select confirmed,deceased from districtdaily where date=(select max(date) from districtdaily) and state ='{state}' and district='{district}';")
    if district=='' and state!='':
        commands.append(f"select totalconfirmed,deaths from coronastatedaily where date=(select max(date) from coronastatedaily) and loc ='{state}';")
    if country!='' and state=="":
        commands.append(f"select cases,deaths from coronaworld1 where date=(select max(date) from coronaworld1 ) and country_name='{country}';")
   
    con = m.connect(host="localhost", user="username", passwd="svasnnmsjdcfjdDFGH!5548)", database="vikas")
    cur = con.cursor()

    result = []
    for command in commands:
        try:
          
            cur.execute(command)
        except Error as e:
            print(e)
        else:
            data = cur.fetchall()
            if len(data[0])==2:
                result.append(int(data[0][0]))
                result.append(int(data[0][1]))
            else:
                try:
                    result.append(int(data[0][0]))
                except:
                    newtimediffer=(datetime.datetime.now()-data[0][0])
                    x=data[0][0]
                    a='{:.0f} minutes'.format ((  (newtimediffer.days*3600*24)+newtimediffer.seconds ) /60)
                    result.append(a)
    result.append(x)
    cur.close()
    con.close()
    return result


def chart(axis1,axis2=[],filename="annonous",chart_type="barh", title="", xlable="", ylable=""):

    if isinstance(axis1[0], datetime.date):
        axis1 = list(map(lambda i: str(i.year) + ":" + str(i.month) + ":" + str(i.day), axis1))
    if isinstance(axis2[0], datetime.date):
        axis2 = list(map(lambda i: str(i.year) + ":" + str(i.month) + ":" + str(i.day), axis2))

  
    plt.xlabel(xlable, color="white",fontsize=14)
    plt.ylabel(ylable, color="white",fontsize=14)
    plt.title(title, color="#ac77f9",fontsize=18)
    plt.xticks(rotation=60,ha='right')
    plt.grid(color='black', linestyle='-.', linewidth=.2)
    try:
        eval(axis1[0])
    except:
        eval(axis2[0])
        axis2 = list(map(lambda i: int(i), axis2))

        if chart_type == "barh":
            plt.barh(axis1, axis2, align="center", color="#ac77f9")
            plt.tick_params(colors='white')

        elif chart_type == "bar":
            plt.bar(axis1, axis2, align="center", color="#ac77f9")

            plt.tick_params(colors='red')

        elif chart_type == "plot":
            plt.plot(axis1, axis2, color="b", linewidth=3)

            plt.tick_params(colors='white')

    else:
        axis1 = list(map(lambda i: int(i), axis1))

        if chart_type == "barh":
            plt.barh(axis2, axis1, align="center", color="#ac77f9")
            plt.tick_params(colors='white')

        elif chart_type == "bar":
            plt.bar(axis2, axis1, align="center", color="#ac77f9")
            plt.tick_params(colors='white')

        elif chart_type == "plot":
            plt.plot(axis2, axis1, color="b", linewidth=3)
            plt.xticks(rotation=60)
            plt.tick_params(colors='white')

    plt.savefig("/mpd/site/public/static/{}.png".format(filename), dpi=90, bbox_inches='tight', transparent=True)
    t = datetime.datetime.now()
    plt.close()

    return "{}.png".format(filename) + "?" + str(t)


def getplace(string):
    place=""
    cou=True
    for i in string:
        try:
            isinstance(int(i),int)
            if cou==False:
                break
        except:
            if not("-" in i or i =="" ):
                place=place+" "+i
                cou=False
    place=place.strip(" ")

    return place


def getdailydifference(table,integeraxis,stringaxis,
                       fc1="state",pk1="Haryana",fc2="district",pk2="faridaad",orderby='-date',limit=15):
    '''
    :param table: Districtdaily (capitalize format)
    :param integeraxis:
    :param stringaxis:
    :param fc1: filter column1 name (state)
    :param pk1: promary key value (Delhi)
    :param fc2: filter column2 name (District)
    :param pk2: primary key value (Shadara)
    :param orderby: (Default -desc)
    :param limit: (Default 15)
    :return: [[list_string],[list_value(in string format)]]
    '''
    from india.models import Coronastatedaily, Districtdaily,Coronaworld1
    #from world.models import Coronaworld1
    if "Districtdaily" in table:
        alldata=Districtdaily.objects.filter(**{fc1:pk1},**{fc2:pk2}).values(integeraxis,stringaxis).order_by(orderby)[:limit+1]
    if "Coronastatedaily" in table:
        alldata = Coronastatedaily.objects.filter(**{fc1: pk1}).values(integeraxis, stringaxis).order_by(
            orderby)[:limit]
    if "Coronaworld1" in table:
        alldata = Coronaworld1.objects.filter(**{fc1: pk1}).values(integeraxis, stringaxis).order_by(
            orderby)[:limit]


    axis1=list(map(lambda a:a[stringaxis],alldata))
    axis2=list(map(lambda a:a[integeraxis],alldata))

    for i in range(len(axis2)-1):
        axis2[i]=str(int(axis2[i])-int(axis2[i+1]))

    return [axis1[-2::-1],axis2[-2::-1]]

def rank(i):
    suf="th"
    if i%10==1:
        suf="st"
    if i%10==2:
        suf="nd"
    if i%10==3:
        suf="rd"
    if (i%100)//10==1:
        suf="th"
    return suf


def getfactsdata(table,string,substring=""):
    from india.models import Coronastatedaily, Districtdaily,Coronaworld1
    #from world.models import Coronaworld1
    from django.db.models import Max
    
    subdate = Districtdaily.objects.aggregate(Max('date'))
    factlist=[]


    if table=="Districtdaily":
        for criteria in ('active','confirmed','deceased','recovered'):
            alldata=Districtdaily.objects.filter(state=string,date=subdate['date__max']).values("district",criteria).order_by(criteria)
            rank=1
            for i in alldata:
                if i['district']==substring:
                    break
                else:
                    rank=rank+1
            factlist.append({'rank':len(alldata)-rank+1,'total':len(alldata),'critaria':criteria.capitalize(),'location':substring,'parentlocation':string})
    if table=="Coronastatedaily":
        subdate = Coronastatedaily.objects.aggregate(Max('date'))
        for criteria in ('totalconfirmed','deaths','discharged'):

            alldata=Coronastatedaily.objects.filter(date=subdate['date__max']).values("loc",criteria).order_by(criteria)

            rank=1
            for i in alldata:
                if i['loc']==string:
                    break
                else:
                    rank=rank+1
            if criteria=="totalconfirmed":
                criteria="total confirmed"
            factlist.append({'rank':len(alldata)-rank+1,'total':len(alldata),'critaria':criteria.capitalize(),'location':string,'parentlocation':'India'})
    if table == "Coronaworld1":
        subdate = Coronaworld1.objects.aggregate(Max('date'))
        for criteria in ('cases', 'deaths', 'active_cases','total_cases_per_1m_population','tests_per_1m_population','deaths_per_1m_population'):

            alldata=Coronaworld1.objects.filter(date=subdate['date__max']).values("country_name", criteria).order_by(criteria)

            rank = 1
            for i in alldata:
                if i['country_name'] == string:
                    break
                else:
                    rank = rank + 1
            factlist.append({'rank': len(alldata)-rank+1, 'total': len(alldata), 'critaria': criteria.replace("_"," ").capitalize(), 'location': string,
                             'parentlocation': 'Globe'})

    return factlist

