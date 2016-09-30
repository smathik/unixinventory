# -*- coding: utf-8 -*-
from django.shortcuts import render
import json, MySQLdb, xlrd, sys
from django.http import HttpResponse, HttpResponseBadRequest
# from valuation.models import *
from django.views.decorators.csrf import csrf_exempt
# from valuation.models import *
from django.contrib.auth import authenticate,login
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from unixdashboard.models import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.shortcuts import render
# from _compact import JsonResponse
from django import forms
import django_excel as excel
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from unixdashboard.serializers import UserSerializer, BackupSerializer
from rest_framework import filters
from rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

#@api_view(['GET'])
class BackupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = backup.objects.all()
    serializer_class = BackupSerializer
#    filter_backends = (filters.DjangoFilterBackend,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('server_name',)

class UploadFileForm(forms.Form):
    file = forms.FileField()

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
#   username,password = request.POST['username'], request.POST['password']
#   ldap_server="tus1gdsdirpin04"
#   user_dn = "cn="+username+",ou=Accounts,ou=People,o=GDS"
#   base_dn = "ou=People,o=GDS"
#   connect = ldap.open(ldap_server)
#   search_filter = "cn="+username
#   try:
#       connect.bind_s(user_dn,password)
#       result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
#       user = authenticate(username=username, password=password)
#       if user:
#         login(request, user)
#         dump = "success"
#         return HttpResponse(content=json.dumps(dump),content_type='Application/json')
#       else:
#         users = User.objects.create_user(username=username, password=password)
#         users.save()
#         user = authenticate(username=username, password=password)
#         if user:
#           login(request, user)
#           dump = "success"
#           return HttpResponse(content=json.dumps(dump),content_type='Application/json')
#       connect.unbind_s()
#   except ldap.LDAPError:
#       connect.unbind_s()
#       print "authentication error"
#       return render(request,'login.html')


def logout_view(request):
   logout(request)
   return render(request,'login.html')

# @login_required
def home(request):
  return render(request,'home.html')

# @login_required
def edit(request):
  return render(request,'edit.html')

# @login_required
@csrf_exempt
def addrow(request):
  if request.method == 'POST':
        ip,fqdn,server_name,serverowner,application_name,app_support_contact,console,machine_type,site_type,os_type,oslevel,bu,source,decomission,decomission_request,category,environment,in_scope_for_patch = request.POST.get('ip'),request.POST.get('fqdn'),request.POST.get('server_name'),request.POST.get('serverowner'),request.POST.get('application_name'),request.POST.get('app_support_contact'),request.POST.get('console'),request.POST.get('machine_type'),request.POST.get('site_type'),request.POST.get('os_type'),request.POST.get('oslevel'),request.POST.get('bu'),request.POST.get('source'),request.POST.get('decomission'),request.POST.get("decomission_request"),request.POST.get('category'),request.POST.get('environment'),request.POST.get('in_scope_for_patch')
        connection = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
        cursor = connection.cursor ()
        query = """INSERT INTO master (ip,fqdn,server_name,serverowner,application_name,app_support_contact,console,machine_type,site_type,os_type,oslevel,bu,source,decomission,decomission_request,category,environment,in_scope_for_patch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
        values = (str(ip),str(fqdn),str(server_name),str(serverowner),str(application_name),str(app_support_contact),str(console),str(machine_type),str(site_type),str(os_type),str(oslevel),str(bu),str(source),str(decomission),str(decomission_request),str(category),str(environment),str(in_scope_for_patch))
        print values
        a = cursor.execute(query, values)
        cursor.close()
        connection.commit()
        connection.close()
  return HttpResponse(content=json.dumps({'data': "success"}),content_type='Application/json')

# @login_required
@csrf_exempt
def modifyrow(request):
  if request.method == 'POST':
        ip,fqdn,server_name,serverowner,application_name,app_support_contact,console,machine_type,site_type,os_type,oslevel,bu,source,decomission,decomission_request,category,environment,in_scope_for_patch,updated_by = request.POST.get('ip'),request.POST.get('fqdn'),request.POST.get('server_name'),request.POST.get('serverowner'),request.POST.get('application_name'),request.POST.get('app_support_contact'),request.POST.get('console'),request.POST.get('machine_type'),request.POST.get('site_type'),request.POST.get('os_type'),request.POST.get('oslevel'),request.POST.get('bu'),request.POST.get('source'),request.POST.get('decomission'),request.POST.get("decomission_request"),request.POST.get('category'),request.POST.get('environment'),request.POST.get('in_scope_for_patch'),request.user.username
        connection = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
        cursor = connection.cursor ()
        cursor.execute("""
          UPDATE master
          SET fqdn=%s,server_name=%s,serverowner=%s,application_name=%s,app_support_contact=%s,console=%s,machine_type=%s,site_type=%s,os_type=%s,oslevel=%s,bu=%s,source=%s,decomission=%s,decomission_request=%s,category=%s,environment=%s,in_scope_for_patch=%s,updated_by=%s
          WHERE ip=%s
        """,(str(fqdn),str(server_name),str(serverowner),str(application_name),str(app_support_contact),str(console),str(machine_type),str(site_type),str(os_type),str(oslevel),str(bu),str(source),str(decomission),str(decomission_request),str(category),str(environment),str(in_scope_for_patch),str(updated_by),str(ip)))
        cursor.close()
        connection.commit()
        connection.close()
  return HttpResponse(content=json.dumps({'data': 'success'}),content_type='Application/json')

# @login_required
@csrf_exempt
def state(request):
    data = []
    connection = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
    cursor = connection.cursor ()
    cursor.execute ("select * from master")
    datas = cursor.fetchall ()
    dataa = [list(i) for i in datas]
    for i in dataa:
     data.append({'ip':str(i[0]),'fqdn':str(i[1]),'server_name':str(i[2]),'serverowner':str(i[3]),'application_name':str(i[4]),'app_support_contact':str(i[5]),'console':str(i[6]),'machine_type':str(i[7]),'site_type':str(i[8]),'os_type':str(i[9]),'oslevel':str(i[10]),'bu':str(i[11]),'source':str(i[12]),'decomission':str(i[13]),'date':str(i[14]),'decomission_request':str(i[15]),'category':str(i[16]),'environment':str(i[17]),'in_scope_for_patch':str(i[18]),'updated_by':str(i[19]),'last_patched':str(i[20])})
    cursor.close()
    connection.commit()
    connection.close()
    return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')


# @login_required
@csrf_exempt
def ip_datas(request):
  if request.method == 'POST':
        data = []
        ip = request.POST.get('ip')
        rowid = request.POST.get('rowid')
        connection = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
        cursor = connection.cursor ()
        cursor.execute ('select * from master_history where ip LIKE "%'+ip+'%"')
        datas = cursor.fetchall ()
        dataa = [list(i) for i in datas]
        if rowid:
          get_delete_data = dataa[int(rowid)]
          print get_delete_data
        for i in dataa:
          data.append({'ip':str(i[0]),'fqdn':str(i[1]),'server_name':str(i[2]),'serverowner':str(i[3]),'application_name':str(i[4]),'app_support_contact':str(i[5]),'console':str(i[6]),'machine_type':str(i[7]),'site_type':str(i[8]),'os_type':str(i[9]),'oslevel':str(i[10]),'bu':str(i[11]),'source':str(i[12]),'decomission':str(i[13]),'date':str(i[14]),'decomission_request':str(i[15]),'category':str(i[16]),'environment':str(i[17]),'in_scope_for_patch':str(i[18])})
        return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')

# @login_required
@csrf_exempt
def delete_row(request):
  if request.method == 'POST':
        ip,fqdn,server_name,serverowner,application_name,app_support_contact,console,machine_type,site_type,os_type,oslevel,bu,source,decomission,decomission_request,category,environment,in_scope_for_patch = request.POST.get('ip'),request.POST.get('fqdn'),request.POST.get('server_name'),request.POST.get('serverowner'),request.POST.get('application_name'),request.POST.get('app_support_contact'),request.POST.get('console'),request.POST.get('machine_type'),request.POST.get('site_type'),request.POST.get('os_type'),request.POST.get('oslevel'),request.POST.get('bu'),request.POST.get('source'),request.POST.get('decomission'),request.POST.get("decomission_request"),request.POST.get('category'),request.POST.get('environment'),request.POST.get('in_scope_for_patch')
        connection = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
        cursor = connection.cursor ()
        cursor.execute("""
          DELETE FROM master_history
          WHERE ip=%s and fqdn=%s and server_name=%s and serverowner=%s and application_name=%s and app_support_contact=%s and console=%s and machine_type=%s and site_type=%s and os_type=%s and oslevel=%s and bu=%s and source=%s and decomission=%s and decomission_request=%s and category=%s and environment=%s and in_scope_for_patch=%s""",(str(ip),str(fqdn),str(server_name),str(serverowner),str(application_name),str(app_support_contact),str(console),str(machine_type),str(site_type),str(os_type),str(oslevel),str(bu),str(source),str(decomission),str(decomission_request),str(category),str(environment),str(in_scope_for_patch)))
        cursor.close()
        connection.commit()
        connection.close()
  return HttpResponse(content=json.dumps({'data': 'success'}),content_type='Application/json')

def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['file']
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_name("sample")
            nrows = sheet.nrows
            database = MySQLdb.connect(host="localhost", user="root", passwd="passw0rd", db="unixinventory")
            cursor = database.cursor()
            query = """INSERT INTO master (ip, fqdn, server_name, serverowner, application_name, app_support_contact, console, machine_type, site_type, last_patched, in_scope_for_patch, environment, updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            for r in range(1, sheet.nrows):
              try:
                  ip      = str(sheet.cell(r,0).value)
                  fqdn = str(sheet.cell(r,1).value)
                  server_name          = str(sheet.cell(r,2).value)
                  serverowner     = str(sheet.cell(r,3).value)
                  application_name       = str(sheet.cell(r,4).value)
                  app_support_contact = str(sheet.cell(r,5).value)
                  console        = str(sheet.cell(r,6).value)
                  machine_type       = str(sheet.cell(r,7).value)
                  site_type     = str(sheet.cell(r,8).value)
                  try:
                      last     = sheet.cell(r,9).value
                      last_pat =  xlrd.xldate_as_tuple(last, 1)
                      a1_datetime = datetime(*last_pat)
                      print a1_datetime.strftime("%m/%d/%Y") 
                      last_patched = a1_datetime.strftime("%m/%d/%Y")
                  except:
                      last_patched     = str(sheet.cell(r,9).value)
                  in_scope_for_patch = str(sheet.cell(r,10).value)
                  environment = str(sheet.cell(r,11).value)
                  updated_by = "MASTER_INVENTORY"
                  values = (ip, fqdn, server_name, serverowner, application_name, app_support_contact, console, machine_type, site_type, last_patched, in_scope_for_patch, environment, updated_by)
                  print values
                  cursor.execute(query, values)
              except:
                  ip      = str(sheet.cell(r,0).value)
                  print "failed>>",ip
                  continue      
              cursor.close()
              database.commit()
              database.close()
            return HttpResponse("Updated Successfully :)", status=200)
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


