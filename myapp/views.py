from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
import time as t
from .utils import token_generator
from bs4 import BeautifulSoup
from .utils import token_generator
import requests
import pandas as pd
import json
import datetime
import os



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
        
# Create your views here.

def index(request):
    
    return render(request, 'index.html')


def sendm():
    now = dt.now()
    print('10 seconds')
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    send_mail(
    'Hello {}'.format(dt_string),
    'Auto email',
    'testw476@gmail.com',
    ['xieyuan.huang@yahoo.com', 'u3184174@gmail.com'],
    fail_silently=False,
    )

def profile(request):
    ruser= request.user
    return render(request, 'profile.html',  {'user': ruser})

def send_letter(request, user):
    #email= user.email
    uidb64= urlsafe_base64_encode(force_bytes(user.pk))
    domain= get_current_site(request).domain
    subject = "Activate your account"
    email_template_name = "activation_email.txt"
    c = {
        "email":user.email,
        'domain': domain,
	    'site_name': 'Website',
		"uid": urlsafe_base64_encode(force_bytes(user.pk)),
		"user": user,
		'token': token_generator.make_token(user),
		'protocol': 'http',}
    email2 = render_to_string(email_template_name, c)
    print('Going to SEND EMAILLLLLLLLL')
    try:
        
        send_mail(subject, email2, 'admin@example.com' , [user.email], fail_silently=False)
    except Exception as ex:
        print(ex)



def register(request):
    if request.method=='POST': 
        username= request.POST['email']
        email= request.POST['email']
        password= request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('register')
        else:
            user= User.objects.create_user(username=username, email= email, password= password)
            user.is_active=False
            user.save()
            print(user.pk)
            send_letter(request, user)
            messages.info(request, 'Activation email sent')
            return redirect('register')
        
    return render(request, 'register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            print("start of verifying")
            id= force_text(urlsafe_base64_decode(uidb64))
            print('get user')
            user= User.objects.get(pk=id)
            print('boolean')
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User has been activated')
            if user.is_active:
                return redirect('login')
            print('start to set true')
            user.is_active=True
            user.save()
            
        except Exception as ex:
            print(ex)
            pass
        return render(request, 'activation_success.html')

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('login')
    else: 

        return render(request, 'login.html' )

def logout(request):
    auth.logout(request)
    return redirect('index')

def activation_success(request):
    
    return render(request, 'activation_success.html' )

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                domain= get_current_site(request).domain
                
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':domain,
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Email not found')
                    return redirect("/password_reset/done/")
    
            else:
                messages.info(request, 'An invalid email has been entered.')
               
                return redirect('password_reset')
                
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})



from sqlalchemy import create_engine
from myapp.models import Weekly_Web
from sqlalchemy import create_engine
import sqlite3
def auto_call(request):

    ############Delete row module
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # delete all rows from table
    c.execute('DELETE FROM {};'.format("myapp_position_sk_post_sum"),)

    print('We have deleted', c.rowcount, 'records from the table.')

    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()
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
        print(previous , '\n')
        
    return HttpResponse("auto_call activated")

def clear_annual_set(request):
        #SQL table dictionary
    for i in jl:
        ############Delete row module
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()

        # delete all rows from table
        c.execute('DELETE FROM {};'.format(sk_tb[i]),)

        print('We have deleted', c.rowcount, 'records from {}.'.format(sk_tb[i]))

        #commit the changes to db			
        conn.commit()
        #close the connection
        conn.close()

    return HttpResponse('Annual data all clear')

def stop_auto(request):
    
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
                
                if 'hours' in time:
                        
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
            send_mail(
                'No Jobs posted today {}'.format(title),
                'auto email',
                'testw476@gmail.com',
                ['xieyuan.huang@yahoo.com'],
                fail_silently=False,
                )
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
                send_mail(
                'No Jobs after filter {}'.format(title),
                'auto email',
                'testw476@gmail.com',
                ['xieyuan.huang@yahoo.com'],
                fail_silently=False,
                )
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
        print(previous.loc[previous['position'] == title]['dataframe'].values)
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
        send_mail(
        'old_pool is',
        '{}'.format(old_pool.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )

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
        send_mail(
        'raw has been stored',
        '{}'.format(old_pool.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )

        #update jobspool
        engine= create_engine('sqlite:///db.sqlite3')
        old_pool.to_sql(name="myapp_jobs_pool", if_exists='replace', con=engine, index=False)

        send_mail(
        'combine_pool is',
        '{}'.format(old_pool.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )
            
    send_mail(
        'position_sk_post_sum is',
        '{}'.format(gg.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )
    
    

    
    print('###################### \n',gg, '\n ######################' )
    

    #Check whether thisday
    today= datetime.date.today()
    from datetime import datetime as dt
    now = dt.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if today.day==29:
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
            send_mail(
            'Previous is',
            '{}'.format(previous.to_json(orient= 'records')),
            'testw476@gmail.com',
            ['xieyuan.huang@yahoo.com'],
            fail_silently=False,
            )
            print(previous , '\n')
        
            

    return HttpResponse("started")


########################################################################################################
def space_parser(position):
    dash = '-'
    text = dash.join(position.split())
    return text
def integrate_link(source, position, area):
    item = "-jobs/"
    text= "https:"+"//www."+source+".com.au/"+space_parser(position) + item + area + "?"
    return text
     
def counter(request):
    #import time as t
    #if request.user.is_authenticated: 
    #SQL table dictionary
    # conn = sqlite3.connect('db.sqlite3')
    # c = conn.cursor()

    # # delete all rows from table
    # c.execute('DELETE FROM {};'.format("myapp_jobs_pool"),)

    # print('We have deleted', c.rowcount, 'records from jobs_pool')

    # #commit the changes to db			
    # conn.commit()
    # #close the connection
    # conn.close()
    start = t.time()
    title=request.POST['position']
    jobs_pool= pd.read_sql("myapp_jobs_pool", 'sqlite:///db.sqlite3')
    target= jobs_pool.loc[jobs_pool['Tags'] == title]
    json_records= target.reset_index().to_json(orient= 'records')
    arr= []
    arr= json.loads(json_records)
    end = t.time()
    execute_time= end-start
    total_jobs= len(target)
    #fit_jobs= len(df)
        
    context= {'d':arr, 'time': round(execute_time,2), 'total_jobs': total_jobs, 'position':title }
    
    

    return render(request, 'counter.html', context)
    # else:
    #     return render(request, 'login.html')

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

def analysis(request):

    def numberOfDays(y, m):
        leap = 0
        if y% 400 == 0:
            leap = 1
        elif y % 100 == 0:
            leap = 0
        elif y% 4 == 0:
            leap = 1
        if m==2:
            return 28 + leap
        list = [1,3,5,7,8,10,12]
        if m in list:
            return 31
        return 30
    #P.S. Defualty, current post amount = the last element of list of quantity change
    #E.g. list of quantity change = [12,13,14,145] then current post amount = 145 (used 
    #in job percentage graph)

    # web_developer = {123: [12,131,324,123],'current_month": [Mon  th list],'managing': 60, 'designing': 30, 'teamwork': 20, 'html':5}
    output=[]
    for title in jl:
        

        #Check whether thisday
        today= datetime.date.today()
        #today= datetime.date.today()+datetime.timedelta(days=43)
        now = dt.now()
        dt_string = today.strftime("%m/%Y")
        #init
        current_m=''
        dic= {}
        #load data
        df=pd.read_sql(sk_tb[title],'sqlite:///db.sqlite3')
        #conn=sqlite3.connect('db.sqlite3',timeout=6000);
        #c = conn.cursor();
        #c.execute('''select * from {} order by month asc'''.format(sk_tb[title]))
        #c.commit();

        #sort month
        #-----------------------old version------------------
        df['month']=pd.to_datetime(df['month'], format="%m/%Y")
        df.sort_values(by='month', inplace=True, ascending=[True])
        df['month']=df['month'].dt.strftime('%m/%Y')
        month_list= df['month'].tolist()
        if dt_string in month_list:
            #get current month
            current_m= dt_string
        else:

        #?
            from datetime import date
            day = numberOfDays(date.today().year, date.today().month)
            today=today-datetime.timedelta(days=day)
            dt_string = today.strftime("%m/%Y")
            # data_month= str((today-datetime.timedelta(days=15)).month)
            # data_year= str((today-datetime.timedelta(days=15)).year)
            # dt_string= '0'+data_month+'/'+data_year
            #get current month
            current_m= dt_string
            
        ##append month on dictionary
        dic[current_m]= month_list
        #-----------------------End--------------------------
        #current_m = sqlite3.object.aggregate(Max('month'));
        #month_list = sqlite3.object.values("month");
        #append month on dictionary
        #dic[current_m]= month_list;

        #-----------------------get latest avaiable month
        latest_m= month_list[len(month_list)-1]

        #-----------------------old version------------------
        ##get current post
        current_p= df.loc[df['month'] == latest_m]['post'].values[0].item()
        
        print(current_p)

        #get post list
        post_list= df['post'].tolist()
        #append post on dictionary
        dic[current_p]= post_list
        #get skill list
        df_sk= df.loc[df['month'] == latest_m]['dataframe'].values[0]
        df_sk= pd.read_json(df_sk)
        #-----------------------End--------------------------
        #current_p     = sqlite3.object.filter(month = current_m).values("post").first;
        #post_list     = sqlite3.object.values("post");
        #dic[current_p]= post_list;
        #df_sk         = sqlite3.object.filter(month = current_m).values("dataframe");
        
        num = 0
        for i in range(0, len(df_sk)):
            dic[df_sk['Skills'][i]]= int(df_sk['Amount'][i])
            if title == "software-engineer":
                print(dic,'\n',"-----------------", num)
                num = num+1
        output.append(dic)

    return render(request, 'analysis.html', {
        'web_developer': json.dumps(output[0]),
        'software_engineer': json.dumps(output[1]),
        'data_analyst': json.dumps(output[2]),
        'network_engineer': json.dumps(output[3]),
        'cloud_architect': json.dumps(output[4]),
        'software_tester': json.dumps(output[5]),
        'developer_programmer': json.dumps(output[6]),
        'analyst_programmer': json.dumps(output[7]),
        'ict_security_specialist': json.dumps(output[8]),
        'network_administrator': json.dumps(output[9]),
        'ict_support_engineer': json.dumps(output[10])
        })


def show_positions_analysis(request):
    #SQL table dictionary
    name= request.GET['name']
    data= pd.read_sql(sk_tb[name], 'sqlite:///db.sqlite3')
    sl_sum=data['dataframe'].values[0]
    post= data['post'].values[0]
    month=data['month']
    arr= []
    arr= json.loads(sl_sum)
    name=name.split('-')
    name=' '.join(name)
    context={'data':arr, 'post':post, 'name':name}
    return render(request, 'analysis.html', context)

def show_temp_var(request):
    data= pd.read_sql('myapp_position_sk_post_sum', 'sqlite:///db.sqlite3')
    df= data.to_json(orient= 'records')
    print(df)
    context={'df':df}
    return render(request, 'analysis.html', context)

from apscheduler.schedulers.background import BackgroundScheduler

def my_job2():

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
               
                if 'hours' in time:
                        
                        name=job.a.text
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
            send_mail(
                'No Jobs posted today {}'.format(title),
                'auto email',
                'testw476@gmail.com',
                ['xieyuan.huang@yahoo.com'],
                fail_silently=False,
                )
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
                send_mail(
                'No Jobs after filter {}'.format(title),
                'auto email',
                'testw476@gmail.com',
                ['xieyuan.huang@yahoo.com'],
                fail_silently=False,
                )
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
        #update old pool
        # thirtyDs_droplist=[]
        # for i in range(0,len(old_pool)):
        #     day= str((pd.Timestamp('{} 00:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).days)
        #     hour= str((pd.Timestamp('{} 00:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).seconds//3600)
        #     adUpDays= pd.Timestamp('{}'.format(datetime.datetime.now().strftime("%Y-%m-%d"))) - old_pool['SpecificT'][i]
            
        #     if day=='1':
        #         old_pool.Released_Date[i]= 'Listed {} day ago'.format(day)
        #     elif day=='0':
        #         old_pool.Released_Date[i]= 'Listed {} hours ago'.format(hour)
        #     elif adUpDays.days >= 30:
        #         thirtyDs_droplist.append(i)   
        #     else:
        #         old_pool.Released_Date[i]= 'Listed {} days ago'.format(day)
        #         # print(thirtyDs_droplist)
        # old_pool = old_pool.drop(thirtyDs_droplist).reset_index().drop(['index'],axis=1)
        # print('before append---------------------------------------\n',old_pool['URL'])
        # send_mail(
        # 'New_pool is',
        # '{}'.format(new_pool.to_json(orient= 'records')),
        # 'testw476@gmail.com',
        # ['xieyuan.huang@yahoo.com'],
        # fail_silently=False,
        # )
        send_mail(
        'old_pool is',
        '{}'.format(old_pool.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )

        #combine old and new
        for i in new_pool:
            print(type(i['SpecificT']))
            old_pool= old_pool.append(i)
        
       
        thirtyDs_droplist=[]
        for i in range(0,len(old_pool)):
            day= str((pd.Timestamp('{} 14:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).days)
            hour= str((pd.Timestamp('{} 14:00:00'.format(datetime.datetime.now().strftime("%Y-%m-%d")))- old_pool['SpecificT'][i]).seconds//3600)
            adUpDays= pd.Timestamp('{}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) - old_pool['SpecificT'][i]
            
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
        print('after append---------------------------------------\n',old_pool['URL'])
        old_pool.sort_values(by='SpecificT', inplace=True, ascending=[False])
        old_pool= old_pool.reset_index().drop(['index'],axis=1)
        #Convert back to string type
        old_pool['SpecificT']=old_pool['SpecificT'].dt.strftime('%Y-%m-%d %H:%M:%S ') 
        
        ####
        print('SSSSSSSSSSSSSShape',old_pool.shape)
        #delete duplicate
        droprow= old_pool.duplicated(subset=['URL', 'Tags'])
        deletelist=[]
        print('_+++++++___droprow=================================\n', droprow)
        for i in range(0, len(droprow)):
           
            if droprow.values[i]==True:
                
                deletelist.append(i)
        print('*******************************************************************************************droprow\n', droprow, '******************************')
        # Drop list
        old_pool = old_pool.drop(deletelist).reset_index().drop(['index'],axis=1)
        
        print('??????????????????????Old Pool??????????????????????')
        print('no dup---------------------------------------\n',old_pool['URL'])
        send_mail(
        'raw has been stored',
        '{}'.format(old_pool.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )

        #update jobspool
        engine= create_engine('sqlite:///db.sqlite3')
        old_pool.to_sql(name="myapp_jobs_pool", if_exists='replace', con=engine, index=False)

        send_mail(
        'combine_pool is',
        '{}'.format(old_pool.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )
            
    send_mail(
        'position_sk_post_sum is',
        '{}'.format(gg.to_json(orient= 'records')),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )
    
    print('###################### \n',gg, '\n ######################' )
    

    #Check whether thisday
    today= datetime.date.today()
    from datetime import datetime as dt
    now = dt.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if today.day==29:
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
            send_mail(
            'Previous is',
            '{}'.format(previous.to_json(orient= 'records')),
            'testw476@gmail.com',
            ['xieyuan.huang@yahoo.com'],
            fail_silently=False,
            )
            print(previous , '\n')

#my_job2()

        
from datetime import datetime as dt
now = dt.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# send_mail(
#         'The time is {}'.format(dt_string),
#         'Auto email',
#         'testw476@gmail.com',
#         ['xieyuan.huang@yahoo.com'],
#         fail_silently=False,
#         )
def test_au():
    try:
        now = dt.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        send_mail(
        'daily task started {}'.format(dt_string),
        'Auto email',
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )

        my_job2()
        

        print('!!!!!!!!!!!!!!!autmation task done!!!!!!!!!!!!!!!!!!!!')
        now = dt.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        send_mail(
        'daily task done {}'.format(dt_string),
        'Auto email',
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )
    except Exception as e:
        send_mail(
        'Error occur on automation task',
        'Auto email {}'.format(e),
        'testw476@gmail.com',
        ['xieyuan.huang@yahoo.com'],
        fail_silently=False,
        )



# scheduler = BackgroundScheduler()
# scheduler.add_job(test_au, trigger='cron', day_of_week='mon-sun', hour=4, minute=00, max_instances=1)
# scheduler.start()