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
#   ldap_server="x.x.x.x"
#   username = "someuser"
#   password= "somepassword"
#   # the following is the user_dn format provided by the ldap server
#   user_dn = "uid="+username+",ou=someou,dc=somedc,dc=local"
#   # adjust this to your base dn for searching
#   base_dn = "dc=somedc,dc=local"
#   connect = ldap.open(ldap_server)
#   search_filter = "uid="+username
#   try:
#     #if authentication successful, get the full user data
#     connect.bind_s(user_dn,password)
#     result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
#     # return all user data results
#     connect.unbind_s()
#     print result
#   except ldap.LDAPError:
#     connect.unbind_s()
#     print "authentication error"

def logout_view(request):
  logout(request)
  return render(request,'login.html')

# @login_required

def home(request):
  return render(request,'home.html')


def state(request):
    data = []
    connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="unixinventory")
    cursor = connection.cursor ()
    cursor.execute ("select * from mastertable")
    datas = cursor.fetchall ()
    dataa = [list(i) for i in datas[1:20]]
    print dataa[1:10]
    for i in dataa[1:10]:
        data.append({'IP':i[0],'FQDN':i[1],'ServerName':i[2],'ServerOwner':i[3],'AppliactionName':i[4]})
    # data.encode('utf-8').strip()
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