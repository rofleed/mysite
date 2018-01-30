#coding = utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse

from cmdb.cloud_atlas import test_run
from cmdb.cloud_atlas import channel_check
from cmdb.cloud_atlas import datamanager
from django.core import  serializers
from cmdb import  models
import  time
import  sys
import json
reload(sys)
sys.setdefaultencoding("utf8")





# Create your views here.

# conn = http.client.HTTPConnection("www.baidu.com")
# conn.request("GET","/")
# r1=conn.getresponse()
# print(r1.status,r1.reason


def index(request):

    Testlist=[{},]
    result=[]
    if request.method=="POST":
        app_key = request.POST.get("app_key",None)
        proctime = request.POST.get("proctime",None)
        datanum = request.POST.get("datanum",None)
        env = request.POST.get("env", None)
        mode = request.POST.get("checkbox1",None)
        sqlorder = request.POST.get("checkbox2",None)
        print mode
        nowtime =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))



        models.HistoryInfo8.objects.create(app_key=app_key,proctime= proctime,datanum = datanum,env =env,nowtime = nowtime)

        case = test_run.SimulateCloudTest()
        result = case.test_autorun(app_key, proctime,datanum,env,mode,sqlorder)
    TestList = models.HistoryInfo8.objects.all()

    print TestList
    return  render(request, "index.html", {"App_key":TestList,"result":result})

def datacheck(request):

    dt =[]


    info ="\n"
    if request.method == "GET":
        app_info = datamanager.DataManager().test_get_applist()
        dt=[]
        # print app_info
        for (m,n,z) in app_info:
            temp = {}
            temp["key"] = m
            temp["value"] = n
            # temp[m] = n
            dt.append(temp)
            # dt.setdefault(m,[]).append(n.decode("utf-8"))
    elif request.method == "POST":
        type = request.POST.get("task_type",None)

        begin_time = request.POST.get("begtime",None)
        end_time = request.POST.get("endtime",None)

        if type== "2":
            app_key = request.POST.get("app_key", None)
            print app_key
            app_list = datamanager.DataManager().test_get_applist()

            result_o = datamanager.DataManager().test_datacheck_process(app_key,begin_time,end_time)
            result ="\n".join(result_o)


            models.HistoryInfo8.objects.create(app_key=app_key,result=result)
        else:
            app_list = datamanager.DataManager().test_get_applist()
            app_key =[]
            for (m, n, z) in app_list:

                temp = n
                app_key.append(temp)
            for app_key in  app_key:
                result_o = datamanager.DataManager().test_datacheck_process(app_key,begin_time,end_time)
                result = "\n".join(result_o)
                print result
                models.HistoryInfo8.objects.create(app_key=app_key, result=result)


    history = models.HistoryInfo8.objects.all()



    return render(request, "datacheck.html", {"dt": dt,"history":history}, )

def channel(request):

    dt1 =[]
    env = request.POST.get("env",None)
    print env
    dt2 = []
    info ="\n"
    if request.method == "GET":
        app_info_1 = channel_check.ChannelCheck().test_get_applist_2(env='cloud-atlas-server.sdp.101.com')
        app_info_2 = channel_check.ChannelCheck().test_get_applist_2(env='cloud-atlas-server.pre1.web.nd')
        dt1=[]
        dt2=[]
        # print app_info
        for (m,n) in app_info_1:
            temp = {}
            temp["key"] = m
            temp["value"] = n
            # temp[m] = n
            dt1.append(temp)
            # dt.setdefault(m,[]).append(n.decode("utf-8"))
        for (m, n) in app_info_2:
            temp = {}
            temp["key"] = m
            temp["value"] = n
            # temp[m] = n
            dt2.append(temp)
            # dt.setdefault(m,[]).append(n.decode("utf-8"))
    elif request.method == "POST":
        type = request.POST.get("task_type",None)
        flag =request.POST.get("hidLI",None)
        env = request.POST.get("env", None)

        begin_time = request.POST.get("begtime",None)
        end_time = request.POST.get("endtime",None)

        if type== "2":
            if env =='cloud-atlas-server.sdp.101.com':
                app_key = request.POST.get("app_key", None)
            else:
                app_key = request.POST.get("app_key_2", None)
            result_o = channel_check.ChannelCheck().test_datacheck_process(app_key,begin_time,end_time,flag,env)
            if result_o==None:
                pass
            else:
                result = "<br/>".join(result_o[1])
                app_key_e = (result_o[0])
                app_list = channel_check.ChannelCheck().test_get_applist_2(env)
                for (m, n) in app_list:
                    if m==app_key_e:
                        app_name=n
                        models.HistoryInfo10.objects.create(app_key=app_name,result=result)
        else:

            app_list = channel_check.ChannelCheck().test_get_applist_2(env)
            app_keys =[]
            for (m, n) in app_list:

                temp = m
                app_keys.append(temp)
            for app_key in  app_keys:
                result_o = channel_check.ChannelCheck().test_datacheck_process(app_key,begin_time,end_time,flag,env)
                if result_o == None:
                    pass
                else:
                    result = "<br/>".join(result_o[1])
                    app_key_e=(result_o[0])
                    for (m, n) in app_list:
                        if m == app_key_e:
                            app_name = n
                            models.HistoryInfo10.objects.create(app_key=app_name, result=result)



    history_tmp = models.HistoryInfo10.objects.all()
    history =  serializers.serialize("json",history_tmp)



    return render(request, "channel.html", {"dt1": dt1,"dt2":dt2,"history":history}, )

def home(request):

    return render(request,"home.html")