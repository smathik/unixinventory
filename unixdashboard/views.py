# -*- coding: utf-8 -*-
from django.shortcuts import render
import json, ldap, MySQLdb
from django.http import HttpResponse
# from valuation.models import *
from django.views.decorators.csrf import csrf_exempt
# from valuation.models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import date


def loginpage(request):
  return render(request,'login.html')

# def login_check(request):
#   username = request.POST['username']
#   password = request.POST['password']
#   print username, password
#   # user = authenticate(username="admin", password="admin")
#   if username=="admin" and password=="admin":
#       # login(request, user)
#       dump = "success"      
#       return HttpResponse(content=json.dumps(dump),content_type='Application/json')
#   else:
#       return render(request,'login.html')

def login_check(request):
  username = request.POST['username']
  password = request.POST['password']
  ldap_server="tus1gdsdirpin04"
  user_dn = "cn="+username+",ou=Accounts,ou=People,o=GDS"
  base_dn = "ou=People,o=GDS"
  connect = ldap.open(ldap_server)
  search_filter = "cn="+username
  try:
    connect.bind_s(user_dn,password)
    result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
    connect.unbind_s()
    dump = "success"
    return HttpResponse(content=json.dumps(dump),content_type='Application/json')
  except ldap.LDAPError:
    connect.unbind_s()
    print "authentication error"
    return render(request,'login.html')

def logout_view(request):
  logout(request)
  return render(request,'login.html')

# @login_required

def home(request):
  return render(request,'home.html')

def addrow(request):
  if request.method == 'POST':
        ip = request.POST['ip']
        fqdn = request.POST['fqdn']
        fqdn = request.POST['fqdn']
        server_name = request.POST['server_name']
        application_name = request.POST['application_name']
        app_support_conatct = request.POST['app_support_conatct']
        console = request.POST['console']
        machine_type = request.POST['machine_type']
        os_type = request.POST['os_type']
        oslevel = request.POST['oslevel']
        decomission = request.POST['decomission']
        date = request.POST['date']
        decommission_request = request.POST['decommission_request']
        category = request.POST['category']
        user = request.POST['user']
        environment = request.POST['environment']
        in_scope_for_patch = request.POST['in_scope_for_patch']
        connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
        cursor = connection.cursor ()
        query = """INSERT INTO mastertable (ip,fqdn,server_name,application_name,app_support_conatct,console,machine_type,os_type,oslevel,decomission,date,decommission_request,category,user,environment,in_scope_for_patch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"""
        values = (ip,fqdn,server_name,application_name,app_support_conatct,console,machine_type,os_type,oslevel,decomission,date,decommission_request,category,user,environment,in_scope_for_patch)
        cursor.execute(query, values)
  return render(request,'home.html')


def state(request):
    data = []
    connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
    cursor = connection.cursor ()
    cursor.execute ("select * from mastertable")
    datas = cursor.fetchall ()
    dataa = [list(i) for i in datas]
    for i in dataa[1:20]:
        data.append({'IP':i[0],'FQDN':i[1],'ServerName':i[2],'ServerOwner':i[3],'ApplicationName':i[4]})
    # data.encode('utf-8').strip()
    # print data[1:20]
    return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')



# import xlrd
# import MySQLdb
# book = xlrd.open_workbook("/media/smathik/Files/Cognizant/pytest.xlsx")
# sheet = book.sheet_by_name("Sheet1")
# database = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
# cursor = database.cursor()
# query = """INSERT INTO mastertable (IP, FQDN, ServerName, ServerOwner, ApplicationName, SupportGroupDL, Console, MachineType, SiteType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
# for r in range(1, sheet.nrows):
#       IP      = sheet.cell(r,0).value
#       FQDN = sheet.cell(r,1).value
#       ServerName          = sheet.cell(r,2).value
#       ServerOwner     = sheet.cell(r,3).value
#       AppliactionName       = sheet.cell(r,4).value
#       SupportGroupDL = sheet.cell(r,5).value
#       Console        = sheet.cell(r,6).value
#       MachineType       = sheet.cell(r,7).value
#       SiteType     = sheet.cell(r,8).value
#       values = (IP, FQDN, ServerName, ServerOwner, AppliactionName, SupportGroupDL, Console, MachineType, SiteType)
#       print values
#       cursor.execute(query, values)

# cursor.close()
# database.commit()
# database.close()