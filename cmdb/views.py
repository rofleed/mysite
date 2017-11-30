from django.shortcuts import render
from django.shortcuts import HttpResponse
import http.client
import urllib3
from cmdb.cloud_atlas import test_run
from cmdb import  models


# Create your views here.

# conn = http.client.HTTPConnection("www.baidu.com")
# conn.request("GET","/")
# r1=conn.getresponse()
# print(r1.status,r1.reason
def index(request):
    #request.POST
    #request.GET
    # return  HttpResponse("hello world")
    Testlist=[{},]
    result=[]
    if request.method=="POST":
        app_key = request.POST.get("app_key",None)
        proctime = request.POST.get("proctime",None)
        datanum = request.POST.get("datanum",None)
        env = request.POST.get("env", None)

        #添加数据到数据库
        models.HistoryInfo6.objects.create(app_key=app_key,proctime= proctime,datanum = datanum,env =env)
        #temp = {"app_key":app_key,"proctime":proctime}

        #TestList.append(temp)
        #TestList = [
       #     {"app_key": "app_key", "proctime": "proctime"},

       # ]
        case = test_run.SimulateCloudTest()
        result = case.test_autorun(app_key, proctime,datanum,env)
    TestList = models.HistoryInfo6.objects.all()


    return  render(request, "index.html", {"App_key":TestList,"result":result})
    #)
    # app_key = (request.GET.get("app_key", None))
    # case = test_run.SimulateCloudTest()
    # result = case.test_autorun(app_key)
    # return HttpResponse(result)
def test(request):
    app_key = (request.GET.get("app_key", None))
    case = test_run.SimulateCloudTest()
    result = case.test_autorun(app_key,)
    return HttpResponse(result)