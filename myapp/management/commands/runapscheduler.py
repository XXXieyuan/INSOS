# runapscheduler.py
import logging
from datetime import datetime as dt
from pickle import TRUE
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from sqlalchemy import create_engine
from myapp.models import *
import pandas as pd
import json
import pytz
import sqlite3
from bs4 import BeautifulSoup
import requests
import time as t
import datetime



sk_tb = {
            'web-developer': 'myapp_web_developer_sk_annual',
            'software-engineer': 'myapp_software_engineer_sk_annual',
            'data-analyst': 'myapp_data_analyst_sk_annual',
            'network-engineer': 'myapp_network_engineer_sk_annual',
            'cloud-architect': 'myapp_cloud_architect_sk_annual',
            'software-tester': 'myapp_software_tester_sk_annual',
            'developer-programmer': 'myapp_developer_programmer_sk_annual',
            'analyst-programmer': 'myapp_analyst_programmer_sk_annual',
            'ict-security-specialist': 'myapp_ict_security_specialist_sk_annual',
            'network-administrator': 'myapp_network_administrator_sk_annual',
            #'network-analyst': 'myapp_network_analyst_sk_annual',
            'ict-support-engineer': 'myapp_ict_support_engineer_sk_annual'
            }

jl=['web-developer', 'software-engineer', 'data-analyst', 'network-engineer', 'cloud-architect','software-tester','developer-programmer','analyst-programmer','ict-security-specialist','network-administrator','ict-support-engineer']

job_skill_dict = {
            
    'web-developer': ['HTML', 'CSS', 'JAVASCRIPT', 'PHP', 'ANGULAR', 'REACT', 'JQUERY', 'BOOTSTRAP', 'WORDPRESS', 'ASP.NET','NET', 'NODEJS', 'AWS', 'AZURE', 'SQL', 'C#','MVC','WCF','WEBAPI','REST API','TYPESCRIPT'],
            
    'software-engineer': ['C#', '.NET', 'C++', 'HTML', 'CSS', 'JAVA', 'JAVASCRIPT', 'PHP', 'ANGULAR', 'JQUERY', 'REACT', 'REACT JS', 'BOOTSTRAP', 'WORDPRESS', 'OWASP', 'WCAG', 'DEV OPS', 'SQL', 'AWS', 'AZURE', 'CLOUD', 'PYTHON', 'LINUX', 'REST API', 'API', 'GITHUB', 'ASP.NET', 'NODEJS'],
            
    'data-analyst': ['SQL', 'POWER BI', 'TABLEAU', 'PYTHON', 'R', 'AWS', 'AZURE', 'LAMBDA', 'EXCEL', 'MATLAB', 'SAS', 'AGILE'],
            
    'network-engineer': ['AWS', 'AZURE', 'SQL', 'PYTHON', 'JAVA', 'NET'],
            
    'cloud-architect': ['AWS', 'AZURE', 'JAVA', 'NET'],

    'software-tester': ['PHP','XML','MAGENTO','ORO','SYMFONY','AGILE','JAVASCRIPT','WORDPRESS','NODE JS','SELENIUM','C#','CYPRESS','NIGHTWATCH','API','JAVA','SQL','XPATH','GHERKIN','CUCUMBER','REST ASSURED','JUNIT','TESTNG','JIRA','UNIX','BITBUCKET','POSTMAN','BUGZILLA'],

    'developer-programmer':['C#', '.NET', 'C++', 'HTML', 'CSS', 'JAVA', 'JAVASCRIPT', 'PHP', 'ANGULAR', 'JQUERY', 'REACT', 'REACT JS','.NET CORE' 'BOOTSTRAP', 'WORDPRESS', 'OWASP', 'WCAG', 'DEV OPS', 'SQL', 'AWS', 'AZURE', 'CLOUD', 'PYTHON', 'LINUX', 'REST API', 'API', 'GITHUB', 'ASP.NET', 'NODEJS','VUEJS','NEM','WEM'],

    'analyst-programmer':['CITRIX','MICROSOFT TEAMS','OFFICE 365','WMS','SQL','MANDALAY','CLEARWEIGH','WASTEMAN','WRAP','SWMS','C#','NET 4','CRM','SHAREPOINT','JS','HTML','CSS','MVC','WCF','WEBAPI','REST API','TYPESCRIPT','AGILE'],

    'ict-security-specialist':['AZURE SENTINEL','AZURE AD','SHAREPOINT','SECURITY POLICY','AWS','SPLUNK','MICROSOFT SECURITY','ITIL FRAMEWORK','CISM CERTIFICATION'],

    'network-administrator':['CISCO','MICROSOFT AZURE','MICROSOFT OFFICE 365','VMWARE','ITIL FRAMEWORK','MICROSOFT HYPER V','MICROSOFT ACTIVE DIRECTORY','MICROSOFT WINDOWS SERVER','FIREWALLS','TCP/IP','DNS','LAN','WAN'],

    #'network-analyst':['VLAN','FIREWALLS','NAT','SIP','SDWAN','CLOUD','CISCO','AWS','CHECKPOINT','MICROSOFT','ITIL','SPLUNK','LINUX','SCRIPTING','TCP/IP','DNS','PACKET ANALYSIS','LAN','WAN'],

    'ict-support-engineer':['UBIQUITI','WATCHGUARD FIREWALLS','SENTINEL1','CAMBIUM/XIRRUS','RMM','3CX','MSP','CONNECTWISE','AZURE','MFA','MICROSOFT OFFICE','SHAREPOINT'],}
        

logger = logging.getLogger(__name__)
tz=pytz.timezone('Australia/Sydney')


# ## Here is the code for counting key skills of web developer for international students
def convert_time(rdate):
    numdict = {
      "zero": '0',
      "one": "1",
      "two": '2',
      "three": '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': '10',
        'eleven': '11',
        'twelve': '12',
        'thirteen': '13',
        'fourteen': '14',
        'fifteen': '15',
        'sixteen': '16',
        'seventeen': '17',
        'eighteen': '18',
        'nineteen': '19',
        'twenty': '2',
        'thirty': '3',
        'forty': '4',
        'fifty': '5',
        'sixty':'6',
        'seventy':'7',
        'eighty':'8',
        'ninety':'9',
        
    }
    check=" second or seconds or minute or minutes or hours or hour or day or days or month or months or ago"
    tis=['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty' , 'ninety']
    memory=[]
    for i in range(0, len(rdate)):
        
        if rdate[i] in check:
            if rdate[i]=='day':
                rdate[i]= 'days'
                break
            elif rdate[i]=='hour':
                rdate[i]= 'hours'
                break
            elif rdate[i]=='month':
                rdate[i]=='months'
                break
            elif rdate[i]=='minute':
                rdate[i]=='minutes'
                break
            elif rdate[i]=='ago':
                break

        else:

            memory.append(rdate[i])
            rdate[i]= numdict[rdate[i]]
    
    rdate= ' '.join(rdate)  
    
    # delete space
    
    for i in range(0, len(rdate)):
        flag=False
        if rdate[i] ==' ':
            if rdate[i-1].isdigit() and rdate[i+1].isdigit():
                rdate =  rdate[:i] + rdate[i+1:]
                break
            elif rdate[i-1].isdigit() and rdate[i+1].isdigit()==False:
                for mem in memory:
                    if mem not in tis and len(memory)==1 :
                        flag=True
                if flag==False:

                    rdate =  rdate[:i] + '0' + rdate[i:]
                    break
            
            
    return rdate
    
def my_job2():

    from datetime import datetime as dt
    now = dt.now()
    # dd/mm/YY H:M:S
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # send_mail(
    #         'Auto task started at {}'.format(dt_string),
    #         'Auto email',
    #         'testw476@gmail.com',
    #         ['xieyuan.huang@yahoo.com'],
    #         fail_silently=False,
    #         )
    # email=EmailMessage(
    # 'nidaye {}'.format(2333),
    # '',
    # 'testw476@gmail.com',
    # ['xieyuan.huang@yahoo.com', 'u3184174@gmail.com']
    #     )
    # email.send(fail_silently=False)

    #Set up job list
    html_txt = requests.get('https://www.seek.com.au/web-developer-jobs/in-All-Canberra-ACT').text
    soup = BeautifulSoup(html_txt, 'html.parser')
    jobs = soup.find_all("article", {"data-automation": "normalJob"})

    job= jobs[0]
    date_time_tag=''
    date_time_class=''
    tags = {tag.name for tag in job.find_all()}

    for tag in tags:
    
        # find all element of tag
        for te in job.find_all( tag ):
    
            # if tag has attribute of class
            if te.has_attr( "class" ) and 'listed' in te.text.lower():
                date_time_tag=tag
                #print(tag)
                date_time_class= " ".join( te['class'])
    
    result=[]
    new_pool=[]
    for i in job_skill_dict:
        

        sl = job_skill_dict[i]
        title= i
        Canberra_region="https://www.seek.com.au/{}-jobs/in-All-Canberra-ACT?".format(title)
        DA_links=[]
         #Search the page from 1 to 5. You can change the amount of pages by changing the range(start, end)

        for pages in range(1,30):
            DA_links.append(Canberra_region+'page={}'.format(pages))
            
        # "raw" is to store the data from seek
        raw={'Title':[],
            'Released_Date':[],
            'URL':[]
        } 
    
        # "WD" is to store the result of counting key skills in web developer
        WD={'Skills':[],
         'Amounts':[],
         }
    
        #Declare Dataframe
        raw=pd.DataFrame(raw)
        WD= pd.DataFrame(WD)
        print(title)
        #construct dataframe
        WD['Skills']=sl
        WD['Amounts']=0



        for i in range(0,len(DA_links)):
            html_txt= requests.get(DA_links[i]).text
            soup= BeautifulSoup(html_txt, 'html.parser')
            jobs= soup.find_all("article", {"data-automation": "normalJob"})

            for job in jobs:
                
                time= job.find(date_time_tag, {"class": date_time_class}).get_text(strip=True)
               
                #if 'hour' in time:
                if 'more' not in time:
                        
                        name=job.find('a', {"data-automation": "jobTitle"}).get_text(strip=True)
                        #Testing purpose
                        
                        url= job.a['href']

                        
                        gg= pd.DataFrame([[name,time,url]], columns=list(raw.columns))
                        raw= raw.append(gg, ignore_index=True)
                        
                        
                else:
                        
                        pass 

        


        # send_mail(
        # 'Droplist for ready'.format(title),
        # '{}'.format(droplist),
        # 'testw476@gmail.com',
        # ['xieyuan.huang@yahoo.com'],
        # fail_silently=False,
        # )
        # send_mail(
        # 'Raw {} is ready'.format(title),
        # '{}'.format(raw.to_json(orient= 'records')),
        # 'testw476@gmail.com',
        # ['xieyuan.huang@yahoo.com'],
        # fail_silently=False,
        # )
        
        #Now, the jobs in "raw" are all suitable for international student
        #Create the sum of post for this position
        if raw.empty:
            # old_pool= pd.read_sql('myapp_jobs_pool','sqlite:///db.sqlite3')
            # old_pool['SpecificT']=pd.to_datetime(old_pool['SpecificT'], format='%Y-%m-%d %H:%M:%S')
            # for i in range(0,len(old_pool)):
            #         day= str((pd.Timestamp('{} 04:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).days)
            #         hour= str((pd.Timestamp('{} 04:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).seconds//3600)
                    
            #         if day=='1':
            #             old_pool.Released_Date[i]= 'Listed {} day ago'.format(day)
            #         elif day=='0':
            #             old_pool.Released_Date[i]= 'Listed {} hours ago'.format(hour)
            #         else:
            #             old_pool.Released_Date[i]= 'Listed {} days ago'.format(day)
            # send_mail(
            #     'No Jobs posted today {}'.format(title),
            #     'auto email',
            #     'testw476@gmail.com',
            #     ['xieyuan.huang@yahoo.com'],
            #     fail_silently=False,
            #     )
            PP=0
            
        else:
            #Extend URL
            if 'https://www.seek.com' not in raw['URL'][0]:
                raw['URL']= 'https://www.seek.com'+ raw['URL']
            
            # send_mail(
            # 'Raw {} before filter'.format(title),
            # '{}'.format(raw),
            # 'testw476@gmail.com',
            # ['xieyuan.huang@yahoo.com'],
            # fail_silently=False,
            # )

            ###########Drop
            droplist=[]
            for i in range(0,len(raw)):
                html_detail= requests.get(raw['URL'][i]).text
                #detail= BeautifulSoup(html_detail, 'lxml')
                detail= BeautifulSoup(html_detail, 'html.parser')
                reqs= detail.find_all('ul')
                descrs= detail.find_all('p')
                tags = {tag.name for tag in detail.find_all()}

                for tag in tags:
                    # find all element of tag
                    for te in detail.find_all( tag ):
                        if 'nv1' in te.text.lower():
                            droplist.append(i)
                


                        elif 'clearance' in te.text.lower():
                            droplist.append(i)
                


                        elif 'citizen' in te.text.lower():
                            droplist.append(i)
                        
                        elif 'nv2' in te.text.lower():
                            droplist.append(i)
                        elif 'aps' in te.text.lower():
                            droplist.append(i)
        
            ## filtered dataframe
            raw=raw.drop(droplist).reset_index().drop(['index'],axis=1)
            if raw.empty:
                # old_pool= pd.read_sql('myapp_jobs_pool','sqlite:///db.sqlite3')
                # old_pool['SpecificT']=pd.to_datetime(old_pool['SpecificT'], format='%Y-%m-%d %H:%M:%S')
                # #update old pool
                # for i in range(0,len(old_pool)):
                #     day= str((pd.Timestamp('{} 04:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).days)
                #     hour= str((pd.Timestamp('{} 04:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).seconds//3600)
                    
                #     if day=='1':
                #         old_pool.Released_Date[i]= 'Listed {} day ago'.format(day)
                #     elif day=='0':
                #         old_pool.Released_Date[i]= 'Listed {} hours ago'.format(hour)
                #     else:
                #         old_pool.Released_Date[i]= 'Listed {} days ago'.format(day)


                # send_mail(
                # 'No Jobs after filter {}'.format(title),
                # 'auto email',
                # 'testw476@gmail.com',
                # ['xieyuan.huang@yahoo.com'],
                # fail_silently=False,
                # )
                PP=0
            else:
                ConvTime=[]
                SpecificT=[]
                #Gap_day=[]
                for rd in raw['Released_Date']:
                        rd= rd.split(' ',1)[1].split(' ')
                        ConvTime.append(convert_time(rd)) 
                
                for s in ConvTime:
                        parsed_s = [s.split()[:2]]
                        time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
                        
                        dt = datetime.timedelta(**time_dict)
                        past_time = datetime.datetime.now() - dt
                        #gap_day= dt.seconds//3600
                        past_time= past_time.strftime("%Y-%m-%d %H:%M:%S")
                        
                        SpecificT.append(past_time)

                
                raw['SpecificT']= SpecificT
                #raw['Gap_day']= Gap_day
                raw['SpecificT']= pd.to_datetime(raw['SpecificT'], format='%Y-%m-%d %H:%M:%S')
                raw.sort_values(by='SpecificT', inplace=True, ascending=[False])
                raw['Tags']= title
                new_pool.append(raw)
                #raw = raw.reset_index().drop(['index'],axis=1)     
                
                
                PP= len(raw)
                #Count the key skills
                for i in range(0,len(raw)):
                    html_detail= requests.get(raw['URL'][i]).text
                    detail= BeautifulSoup(html_detail, 'html.parser')
                    #flags is a switch to make sure each skill only count once in each job
                    flags=[True]*len(sl)

                    #print(raw['URL'][i])
                    tags = {tag.name for tag in detail.find_all()}

                    for tag in tags:
                        # find all element of tag
                        for te in detail.find_all( tag ):

                            #get amounts
                            for index in range(0, len(flags)):

                                if sl[index] in te.text.upper() and flags[index]==True:

                                    WD.at[index,'Amounts']+=1
                                    flags[index]=False
                                    #print(flags[index],'and', WD.at[index,'Skills'],WD.at[index,'Amounts'])

                #Now sort the skills
                WD=WD.sort_values('Amounts',ascending=[False]).reset_index().drop(['index'],axis=1)
            
        #get previous data from sql
        previous= pd.read_sql('myapp_position_sk_post_sum','sqlite:///db.sqlite3')
        #Now previous has previous number of posts and skill_list_dataframe
        #get previous dataframe
        previous_dataframe=previous.loc[previous['position'] == title]['dataframe'].values[0]
        previous_dataframe=pd.read_json(previous_dataframe)
        #get previous number of post
        previous_post= previous.loc[previous['position'] == title]['post'].values[0]
        #Add new today's and previous data together

        print('Previous post amount:', previous_post)
        print('new post amount:', PP)
        previous_dataframe['Amount']=previous_dataframe['Amount']+WD['Amounts']
            
        new_dataframe=  previous_dataframe.to_json(orient= 'records')
        #print(new_dataframe,'\n', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(pd.read_json(new_dataframe))
        print('---------------------------------------------------------')
        new_post= PP+previous_post
        new= {'position':[title],
                'dataframe':[new_dataframe],
                'post': [new_post]
                } 
        new= pd.DataFrame(new)
        result.append(new)

    for re in result:
        print('_+_+_+_+_+_+_+_+_+_+_+_+\n',re)
    # ############Delete row module
    conn = sqlite3.connect('db.sqlite3',timeout=6000)
    c = conn.cursor()
    # delete corresponding rows from table
    c.execute('DELETE FROM {};'.format("myapp_position_sk_post_sum"),)
    conn.commit()
    conn.close()
    print('We have deleted', c.rowcount, 'records from the table.')
    engine= create_engine('sqlite:///db.sqlite3')
        
    for i in result:
        print('start to store back')
        i.to_sql(name="myapp_position_sk_post_sum", if_exists='append', con=engine, index=False)
    gg=pd.read_sql("myapp_position_sk_post_sum", 'sqlite:///db.sqlite3')

    #update old pool
    old_pool= pd.read_sql('myapp_jobs_pool','sqlite:///db.sqlite3')

    if old_pool.empty:

        print('no old poooooooooooooooooooool')
        # Restrict 1 day!!
        for i in new_pool:
            # for j in range(0, len(i)):
            #     hour= str((pd.Timestamp('{} 00:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- i['SpecificT'][j]).seconds//3600)
            #     i.Released_Date[j]= 'Listed {} hours ago'.format(hour)
            i['SpecificT']=i['SpecificT'].dt.strftime('%Y-%m-%d %H:%M:%S ') 
            i.to_sql(name="myapp_jobs_pool", if_exists='append', con=engine, index=False)

        #For all data source

    
    else:
        print('have old poooooooooooooooooool')
        old_pool['SpecificT']=pd.to_datetime(old_pool['SpecificT'], format='%Y-%m-%d %H:%M:%S')
        
        
        # send_mail(
        # 'New_pool is',
        # '{}'.format(new_pool.to_json(orient= 'records')),
        # 'testw476@gmail.com',
        # ['xieyuan.huang@yahoo.com'],
        # fail_silently=False,
        # )
        # send_mail(
        # 'old_pool is',
        # '{}'.format(old_pool.to_json(orient= 'records')),
        # 'testw476@gmail.com',
        # ['xieyuan.huang@yahoo.com'],
        # fail_silently=False,
        # )

        #combine old and new
        for i in new_pool:
            old_pool= old_pool.append(i)
        old_pool= old_pool.reset_index().drop(['index'],axis=1)
        #update old pool
        thirtyDs_droplist=[]
        for i in range(0,len(old_pool)):
            # day= str((pd.Timestamp('{} 15:40:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).days)
            # hour= str((pd.Timestamp('{} 15:40:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).seconds//3600)
            # adUpDays= pd.Timestamp('{}'.format(datetime.datetime.now().strftime("%Y-%m-%d"))) - old_pool['SpecificT'][i]
            day= str((pd.Timestamp('{}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")))- old_pool['SpecificT'][i]).days)
            hour= str((pd.Timestamp('{}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")))- old_pool['SpecificT'][i]).seconds//3600)
            adUpDays= pd.Timestamp('{}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S "))) - old_pool['SpecificT'][i]
            
            if day=='1':
                old_pool.Released_Date[i]= 'Listed {} day ago'.format(day)
            elif day=='0':
                old_pool.Released_Date[i]= 'Listed {} hours ago'.format(hour)
            elif adUpDays.days >= 30:
                thirtyDs_droplist.append(i)   
            else:
                old_pool.Released_Date[i]= 'Listed {} days ago'.format(day)
                # print(thirtyDs_droplist)
        old_pool = old_pool.drop(thirtyDs_droplist).reset_index().drop(['index'],axis=1)
        old_pool.sort_values(by='SpecificT', inplace=True, ascending=[False])
       
        #Convert back to string type
        old_pool['SpecificT']=old_pool['SpecificT'].dt.strftime('%Y-%m-%d %H:%M:%S ') 
        print('after append new---------------------------------------\n',old_pool['URL'])

        #delete duplicate
        # droprow= old_pool.duplicated(subset=['URL','Tags'])
        # deletelist=[]
        # print('_+++++++___droprow=================================\n', droprow)
        # for i in range(0, len(droprow)):
           
        #     if droprow.values[i]==True:
                
        #         deletelist.append(i)
        #         print(i)
        # # Drop list
        # old_pool = old_pool.drop(deletelist).reset_index().drop(['index'],axis=1)
        old_pool=old_pool.drop_duplicates(subset=['URL', 'Tags', 'Title'], keep='last')
        
        print('??????????????????????Old Pool??????????????????????')
        print('no dup---------------------------------------\n',old_pool['URL'])
        # send_mail(
        # 'raw has been stored',
        # '{}'.format(old_pool.to_json(orient= 'records')),
        # 'testw476@gmail.com',
        # ['xieyuan.huang@yahoo.com'],
        # fail_silently=False,
        # )

        #update jobspool
        engine= create_engine('sqlite:///db.sqlite3')
        old_pool.to_sql(name="myapp_jobs_pool", if_exists='replace', con=engine, index=False)

        # send_mail(
        # 'combine_pool is',
        # '{}'.format(old_pool.to_json(orient= 'records')),
        # 'testw476@gmail.com',
        # ['xieyuan.huang@yahoo.com'],
        # fail_silently=False,
        # )
            
    # send_mail(
    #     'position_sk_post_sum is',
    #     '{}'.format(gg.to_json(orient= 'records')),
    #     'testw476@gmail.com',
    #     ['xieyuan.huang@yahoo.com'],
    #     fail_silently=False,
    #     )
    
    print('###################### \n',gg, '\n ######################' )
    

    #Check whether thisday
    today= datetime.date.today()
    from datetime import datetime as dt
    now = dt.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if today.day==1:
        print('start testing')
        data_month= str((today-datetime.timedelta(days=15)).month)
        data_year= str((today-datetime.timedelta(days=15)).year)
        data_date= data_month+'/'+data_year
        #store position sk post data to corresponding tablee
        for i in job_skill_dict:
            #consruct dataframe
            df={'month':[data_date],
                'dataframe':[gg.loc[gg['position'] == i]['dataframe'].values[0]],
                'post': [gg.loc[gg['position'] == i]['post'].values[0]]
                } 
            df= pd.DataFrame(df)
            before= pd.read_sql(sk_tb[i],'sqlite:///db.sqlite3')
            print(df)
            print(before)
            before= before.append(df, ignore_index=True)
            print(before)
            # ############Delete row module
            conn = sqlite3.connect('db.sqlite3',timeout=6000)
            c = conn.cursor()
            # delete corresponding rows from table
            c.execute('DELETE FROM {};'.format(sk_tb[i]),)
            conn.commit()
            conn.close()
            print('We have deleted', c.rowcount, 'records from {}.'.format(sk_tb[i]))
            engine= create_engine('sqlite:///db.sqlite3')
            print('+++++++++++++++++++++++++++++++++++++++++++++')
            
            before.to_sql(name=sk_tb[i],if_exists='append', con=engine, index=False)
            
        print('--------------Start to clear position sk sum-------------------')
        #Clear position_sk_sum
        #Delete row module
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()

        # delete all rows from table
        c.execute('DELETE FROM {};'.format("myapp_position_sk_post_sum"),)

        print('We have deleted', c.rowcount, 'records from myapp_position_sk_post_sum.')

        #commit the changes to db			
        conn.commit()
        #close the connection
        conn.close()
        #Append the default content to positon sk sum
        for i in jl:
            
            tablee= "myapp_position_sk_post_sum"
            
            sk_zero={'Skills':job_skill_dict[i],
                'Amount':0*len(job_skill_dict[i])  
            } 
            sk_zero=pd.DataFrame(sk_zero)
            
            sk_zero= sk_zero.reset_index().to_json(orient= 'records')
            raw={'position':[i],
                'dataframe':[sk_zero],
                'post': [0]
                } 

            raw=pd.DataFrame(raw)
            engine= create_engine('sqlite:///db.sqlite3')
            raw.to_sql(name=tablee, if_exists='append', con=engine, index=False)
            previous= pd.read_sql(tablee, 'sqlite:///db.sqlite3')
            # send_mail(
            # 'Previous is',
            # '{}'.format(previous.to_json(orient= 'records')),
            # 'testw476@gmail.com',
            # ['xieyuan.huang@yahoo.com'],
            # fail_silently=False,
            # )
            print(previous , '\n')

            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            email=EmailMessage(
            'Database updated {}'.format(dt_string),
            '',
            'testw476@gmail.com',
            ['xieyuan.huang@yahoo.com', 'u3184174@gmail.com']
                )
            email.attach_file('db.sqlite3')
            print(email)
            email.send(fail_silently=False)
    else:
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        email=EmailMessage(
        'Database updated {}'.format(dt_string),
        '',
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com']
            )
        email.attach_file('db.sqlite3')
        print(email)
        email.send(fail_silently=False)
        



# from datetime import datetime as dt
# now = dt.now()
# # dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# send_mail(
#         'The time is {}'.format(dt_string),
#         'Auto email',
#         'testw476@gmail.com',
#         ['xieyuan.huang@yahoo.com'],
#         fail_silently=False,
#         )
# def test_au():
#     try:
#         now = dt.now()
#         # dd/mm/YY H:M:S
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         send_mail(
#         'daily task started {}'.format(dt_string),
#         'Auto email',
#         'testw476@gmail.com',
#         ['xieyuan.huang@yahoo.com'],
#         fail_silently=False,
#         )

#         my_job2()
        

#         print('!!!!!!!!!!!!!!!autmation task done!!!!!!!!!!!!!!!!!!!!')
#         now = dt.now()
#         # dd/mm/YY H:M:S
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         send_mail(
#         'daily task done {}'.format(dt_string),
#         'Auto email',
#         'testw476@gmail.com',
#         ['xieyuan.huang@yahoo.com'],
#         fail_silently=False,
#         )
#     except Exception as e:
#         send_mail(
#         'Error occur on automation task',
#         'Auto email {}'.format(e),
#         'testw476@gmail.com',
#         ['xieyuan.huang@yahoo.com'],
#         fail_silently=False,
#         )

def sendm():
    now = dt.now()
    print('10 seconds')
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    send_mail(
    'daily task started {}'.format(dt_string),
    'Auto email',
    'testw476@gmail.com',
    ['xieyuan.huang@yahoo.com', 'u3184174@gmail.com'],
    fail_silently=False,
    )

# The `close_old_connections` decorator ensures that database connections, that have become unusable or are obsolete,
# are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database. It helps to prevent the
    database from filling up with old historical records that are no longer useful.

    :param max_age: The maximum length of time to retain historical job execution records. Defaults
                    to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job2,
            trigger=CronTrigger(year='*', month='*', day="*", week='*', day_of_week='*', hour=21, minute=15, second=30), # Every 10 seconds
            #id="my_job2",  # The `id` assigned to each job MUST be unique
            misfire_grace_time= None,
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        # scheduler.add_job(
        #     delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week="mon", hour="00", minute="00"
        #     ),  # Midnight on Monday, before start of the next work week.
        #     id="delete_old_job_executions",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info(
        #     "Added weekly job: 'delete_old_job_executions'."
        # )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")