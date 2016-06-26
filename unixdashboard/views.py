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
        print ">>>>>>addrow"
        ip = request.POST.get('ip')
        fqdn = request.POST.get('fqdn')
        server_name = request.POST.get('server_name')
        serverowner = request.POST.get('serverowner')
        application_name = request.POST.get('application_name')
        app_support_contact = request.POST.get('app_support_contact')
        console = request.POST.get('console')
        machine_type = request.POST.get('machine_type')
        site_type = request.POST.get('site_type')
        os_type = request.POST.get('os_type')
        oslevel = request.POST.get('oslevel')
        bu = request.POST.get('bu')
        source = request.POST.get('source')
        decomission = request.POST.get('decomission')
        decomission_request = request.POST.get('decomission_request')
        category = request.POST.get('category')
        environment = request.POST.get('environment')
        in_scope_for_patch = request.POST.get('in_scope_for_patch')
        connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
        cursor = connection.cursor ()
        query = """INSERT INTO master (ip,fqdn,server_name,serverowner,application_name,app_support_contact,console,machine_type,site_type,os_type,oslevel,bu,source,decomission,decomission_request,category,environment,in_scope_for_patch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
        values = (str(ip),str(fqdn),str(server_name),str(serverowner),str(application_name),str(app_support_contact),str(console),str(machine_type),str(site_type),str(os_type),str(oslevel),str(bu),str(source),str(decomission),str(decomission_request),str(category),str(environment),str(in_scope_for_patch))
        print values
        a = cursor.execute(query, values)
        cursor.close()
        connection.commit()
        connection.close()
  return HttpResponse(content=json.dumps({'data': "success"}),content_type='Application/json')

@csrf_exempt
def modifyrow(request):
  if request.method == 'POST':
        print ">>>>>>modifyrow"
        ip = request.POST.get('ip')
        fqdn = request.POST.get('fqdn')
        server_name = request.POST.get('server_name')
        serverowner = request.POST.get('serverowner')
        application_name = request.POST.get('application_name')
        app_support_contact = request.POST.get('app_support_contact')
        console = request.POST.get('console')
        machine_type = request.POST.get('machine_type')
        site_type = request.POST.get('site_type')
        os_type = request.POST.get('os_type')
        oslevel = request.POST.get('oslevel')
        bu = request.POST.get('bu')
        source = request.POST.get('source')
        decomission = request.POST.get('decomission')
        decomission_request = request.POST.get('decomission_request')
        category = request.POST.get('category')
        environment = request.POST.get('environment')
        in_scope_for_patch = request.POST.get('in_scope_for_patch')
        connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
        cursor = connection.cursor ()
        cursor.execute("""
          UPDATE master 
          SET fqdn=%s,server_name=%s,serverowner=%s,,application_name=%s,app_support_contact=%s,console=%s,machine_type=%s,site_type=%s,os_type=%s,oslevel=%s,bu=%s,source=%s,decomission=%s,decomission_request=%s,category=%s,environment=%s,in_scope_for_patch=%s
          WHERE ip=%s
        """,(fqdn,server_name,serverowner,application_name,app_support_contact,console,machine_type,site_type,os_type,oslevel,bu,source,decomission,decomission_request,category,environment,in_scope_for_patch,ip))
        cursor.close()
        connection.commit()
        connection.close()
        # cursor.execute ("UPDATE master SET serverowner=%s WHERE ip='%s' " % (serverowner,  ip))
        # values = (str(ip),str(fqdn),str(server_name),str(serverowner),str(application_name),str(app_support_contact),str(console),str(machine_type),str(site_type),str(os_type),str(oslevel),str(bu),str(source),str(decomission),str(decomission_request),str(category),str(environment),str(in_scope_for_patch))
        # print values
        # a = cursor.execute(query)
        # print ">>>>>q",a
  return HttpResponse(content=json.dumps({'data': 'success'}),content_type='Application/json')

@csrf_exempt
def state(request):
    data = []
    connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
    cursor = connection.cursor ()
    cursor.execute ("select * from master")
    datas = cursor.fetchall ()
    dataa = [list(i) for i in datas]
    # print dataa
    # new = [x.encode('UTF8') for x in dataa]
    # ew = [[x.encode('utf-8') for x in lis[0:9]] for lis in dataa]
    # d = [[s.encode('ascii', 'ignore') for s in lis] for lis in dataa]
    # print dataa[1:20]
    print dataa[1]
    for i in dataa[1:10]:
        data.append({'ip':i[0],'fqdn':i[1],'server_name':i[2],'serverowner':i[3],'application_name':i[4],'app_support_contact':i[5],'console':i[6],'machine_type':i[7],'site_type':i[8]})
    # for i in dataa[1]:
      # data.append({'ip':i[0],'fqdn':i[1],'server_name':i[2],'serverowner':i[3],'application_name':i[4],'app_support_contact':i[5],'console':i[6],'machine_type':i[7],'site_type':i[8],'os_type':i[9],'oslevel':i[10],'bu':i[11],'source':i[12],'decomission':i[13],'date':i[14],'decomission_request':i[15],'category':i[16],'environment':i[17],'in_scope_for_patch':i[18]})
        # data.append({'ip':i[0],'fqdn':i[1],'server_name':i[2],'serverowner':i[3],'application_name':i[4],'app_support_contact':i[5],'console':i[6],'machine_type':i[7],'site_type':i[8],'oslevel':i[9],'bu':i[10],'source':i[11],'decomission':i[12],'decomission_request':i[13],'category':i[14],'environment':i[15],'in_scope_for_patch':i[16]})
    # print data
    return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')