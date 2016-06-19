# -*- coding: utf-8 -*-
from django.shortcuts import render
import json, MySQLdb
from django.http import HttpResponse
# from valuation.models import *
from django.views.decorators.csrf import csrf_exempt
# from valuation.models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


def loginpage(request):
  return render(request,'login.html')

def login_check(request):
  username = request.POST['username']
  password = request.POST['password']
  print username, password
  # user = authenticate(username="admin", password="admin")
  if username=="admin" and password=="admin":
      # login(request, user)
      dump = "success"
      return HttpResponse(content=json.dumps(dump),content_type='Application/json')
  else:
      return render(request,'login.html')

# def login_check(request):
#   username = request.POST['username']
#   password = request.POST['password']
#   ldap_server="tus1gdsdirpin04"
#   user_dn = "cn="+username+",ou=Accounts,ou=People,o=GDS"
#   base_dn = "ou=People,o=GDS"
#   connect = ldap.open(ldap_server)
#   search_filter = "cn="+username
#   try:
#     connect.bind_s(user_dn,password)
#     result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
#     connect.unbind_s()
#     dump = "success"
#     return HttpResponse(content=json.dumps(dump),content_type='Application/json')
#   except ldap.LDAPError:
#     connect.unbind_s()
#     print "authentication error"
#     return render(request,'login.html')

def logout_view(request):
  logout(request)
  return render(request,'login.html')

# @login_required

def home(request):
  return render(request,'home.html')


def edit(request):
  return render(request,'edit.html')

@csrf_exempt
def addrow(request):
  if request.method == 'POST':
        print ">>>>>>"
        ip = request.POST.get('ip')
        fqdn = request.POST.get('fqdn')
        server_name = request.POST.get('server_name')
        application_name = request.POST.get('application_name')
        app_support_conatct = request.POST.get('app_support_conatct')
        console = request.POST.get('console')
        machine_type = request.POST.get('machine_type')
        os_type = request.POST.get('os_type')
        oslevel = request.POST.get('oslevel')
        values = (ip,fqdn,server_name,application_name,app_support_conatct,console,machine_type,os_type,oslevel)
        print values
        # decomission = request.POST['decomission']
        # date = request.POST['date']
        # decommission_request = request.POST['decommission_request']
        # category = request.POST['category']
        # user = request.POST['user']
        # environment = request.POST['environment']
        # in_scope_for_patch = request.POST['in_scope_for_patch']
        # connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
        # cursor = connection.cursor ()
        # query = """INSERT INTO master (ip,fqdn,server_name,application_name,app_support_conatct,console,machine_type,os_type,oslevel,decomission,date,decommission_request,category,user,environment,in_scope_for_patch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"""
        # values = (ip,fqdn,server_name,application_name,app_support_conatct,console,machine_type,os_type,oslevel,decomission,date,decommission_request,category,user,environment,in_scope_for_patch)
        # print values
        # cursor.execute(query, values)
  return HttpResponse(content=json.dumps({'data': "success"}),content_type='Application/json')


# def modifyrow(request):
#     print "yes its working"
#         # ip = request.POST['ip']
#         # fqdn = request.POST['fqdn']
#         # fqdn = request.POST['fqdn']
#         # server_name = request.POST['server_name']
#         # application_name = request.POST['application_name']
#         # app_support_conatct = request.POST['app_support_conatct']
#         # console = request.POST['console']
#         # machine_type = request.POST['machine_type']
#         # os_type = request.POST['os_type']
#         # oslevel = request.POST['oslevel']
#         # decomission = request.POST['decomission']
#         # date = request.POST['date']
#         # decommission_request = request.POST['decommission_request']
#         # category = request.POST['category']
#         # user = request.POST['user']
#         # environment = request.POST['environment']
#         # in_scope_for_patch = request.POST['in_scope_for_patch']
#         # connection = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
#         # cursor = connection.cursor ()
#         # query = """INSERT INTO master (ip,fqdn,server_name,application_name,app_support_conatct,console,machine_type,os_type,oslevel,decomission,date,decommission_request,category,user,environment,in_scope_for_patch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"""
#         # values = (ip,fqdn,server_name,application_name,app_support_conatct,console,machine_type,os_type,oslevel,decomission,date,decommission_request,category,user,environment,in_scope_for_patch)
#         # cursor.execute(query, values)
#   return render(request,'home.html')


def state(request):
    data = []
    connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
    cursor = connection.cursor ()
    cursor.execute ("select * from master")
    datas = cursor.fetchall ()
    dataa = [list(i) for i in datas]
    print dataa
    # new = [x.encode('UTF8') for x in dataa]
    # d = [[s.encode('ascii', 'ignore') for s in lis] for lis in dataa]
    # print d[1:20]
    for i in dataa:
        data.append({'ip':str(i[0]),'fqdn':str(i[1]),'server_name':str(i[2]),'serverowner':str(i[3]),'application_name':str(i[4]),'app_support_conatct':str(i[5]),'console':str(i[6]),'machine_type':str(i[7]),'site_type':str(i[8])})
    return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')