# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from . import models
from django.core.mail import send_mail
import datetime
from Bibliosoft_library import settings
from django.db.models import Q
from models import IMG
import urllib
from urllib import urlretrieve
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import re


from django.shortcuts import render
import barcode
from PIL import Image, ImageDraw, ImageFont, ImageWin
from StringIO import StringIO

from django.shortcuts import render

# Create your views here.
def homepage(request):
    post = models.posttext.objects.all()
    if request.POST.has_key('admin_login'):
        user = request.POST.get('adminname')
        pwd = request.POST.get('adminpwd')
        try:
            get_id = models.admin.objects.get(id=user)
            try:
                compare_user = models.admin.objects.get(id=user, pwd=pwd)
                if compare_user:
                    request.session['user'] = user
                    request.session['pwd'] = pwd
                    return HttpResponseRedirect('/admin_home/')
                else:
                    return render(request, "homepage.html", {'ans': 'password wrong.', 'post': post})
            except:
                return render(request, "homepage.html", {'ans': 'password wrong.', 'post': post})
        except:
            return render(request, "homepage.html", {'ans': 'not exist id.', 'post': post})
    user = request.POST.get("username", None)
    pwd = request.POST.get("password", None)
    identity = request.POST.get("identity", None)

    if request.POST.has_key('librarian_recover'):
        try:
            lib = models.librarian.objects.filter(id=user)
            if lib:
                lib[0].isrequest = '1'
                lib[0].save()
            return render(request, "homepage.html", {'ans':'Already sent the message to the admin.', 'post':post})
        except:
            return render(request, "homepage.html", {'ans': 'not exist id.', 'post':post})
    elif request.POST.has_key('login'):
        if identity == 'librarian':
            try:
                get_id = models.librarian.objects.get(id=user)
                try:
                    compare_user = models.librarian.objects.get(id=user, pwd=pwd)
                    if compare_user:
                        request.session['user'] = user
                        request.session['pwd'] = pwd
                        return HttpResponseRedirect('/librarian_home/')
                    else:
                        return render(request, "homepage.html", {'ans': 'password wrong.', 'post':post})
                except:
                    return render(request, "homepage.html", {'ans': 'password wrong.', 'post':post})
            except:
                return render(request, "homepage.html", {'ans': 'not exist id.', 'post':post})

        else:
            try:
                get_id = models.reader.objects.get(id=user)
                try:
                    compare_user = models.reader.objects.get(id=user, pwd=pwd)
                    if compare_user:
                        request.session['user'] = user
                        request.session['pwd'] = pwd
                        return HttpResponseRedirect('/reader_home/')
                    else:
                        return render(request, "homepage.html", {'ans': 'password wrong.', 'post':post})
                except:
                    return render(request, "homepage.html", {'ans': 'password wrong.', 'post':post})
            except:
                return render(request, "homepage.html", {'ans': 'not exist id.', 'post':post})
    elif request.POST.has_key('signup'):
        reader_id = request.POST.get('reader_id', None)
        reader_email = request.POST.get('email', None)
        s = models.reader.objects.filter(id=reader_id, email=reader_email)
        if len(s) == 0:
            return render(request, "homepage.html", {'new_ans': 'Send failed. Check your id or email.', 'post':post})
        # try:
        #
        #     models.reader.objects.get(id=reader_id, email=reader_email)
        #
        #     sender = 'bibliosoft_b5@163.com'
        #     receiver = reader_email
        #     subject = 'change password'
        #     smtpserver = 'smtp.163.com'
        #     username = 'bibliosoft_b5@163.com'
        #     password = 'abcd12345'
        #
        #     msg = MIMEText('Your new password is 12345678.', 'plain', 'utf-8')
        #     msg['Subject'] = Header(subject, 'utf-8')
        #     msg['from'] = sender
        #     msg['to'] = receiver
        #     smtp = smtplib.SMTP()
        #     smtp.connect(smtpserver)
        #     smtp.login(username, password)
        #     smtp.sendmail(sender, [receiver,sender], msg.as_string())
        #     smtp.quit()
        # except:
        #
        #     models.reader.objects.get(id=reader_id, email=reader_email)
        #
        #     sender = 'bibliosoft_b5@163.com'
        #     receiver = sender
        #     subject = 'change password'
        #     smtpserver = 'smtp.163.com'
        #     username = 'bibliosoft_b5@163.com'
        #     password = 'abcd12345'
        #
        #     msg = MIMEText('Your new password is 12345678.', 'plain', 'utf-8')
        #     msg['Subject'] = Header(subject, 'utf-8')
        #     msg['from'] = sender
        #     msg['to'] = receiver
        #     smtp = smtplib.SMTP()
        #     smtp.connect(smtpserver)
        #     smtp.login(username, password)
        #     smtp.sendmail(sender, [receiver], msg.as_string())
        #     smtp.quit()
        try:
            send_mail('change password', 'Your new password is 12345678.', settings.EMAIL_FROM,
                      [reader_email, settings.EMAIL_FROM])
        except:
            send_mail('change password', 'Your new password is 12345678.', settings.EMAIL_FROM,
                      [settings.EMAIL_FROM])
            return render(request, "homepage.html", {'new_ans': 'Send failed.', 'post': post})

        reader = models.reader.objects.filter(id=reader_id)[0]
        reader.pwd = '12345678'
        reader.save()
        return render(request, "homepage.html", {'ans': 'Send request successfully.', 'post':post})
        #except:
        #    return render(request, "homepage.html", {'new_ans': 'Send failed. Check your id or email.', 'post':post})
    else:
        return render(request, "homepage.html", {'post':post})

def admin_login(request):
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        try:
            get_id = models.admin.objects.get(id=user)
            try:
                compare_user = models.admin.objects.get(id=user, pwd=pwd)
                if compare_user:
                    request.session['user'] = user
                    request.session['pwd'] = pwd
                    return HttpResponseRedirect('/admin_home/')
                else:
                    return render(request, "login.html")
            except:
                return render(request, "login.html", {'ans': 'password wrong.'})
        except:
            return render(request, "login.html", {'ans': 'not exist id.'})
    else:
        return render(request, "login.html")

def reader_home(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])

        return render(request, "reader_home.html",{'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_search(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        imgs = IMG.objects.all()
        #content = {
        #    'imgs': imgs,
        #}

        appointment = models.appointment.objects.all()
        now = datetime.datetime.now()
        for record in appointment:
            time = record.time
            appointment_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            if (now - appointment_time).seconds > 7200 or (now - appointment_time).days >= 1:
                record.delete()

        if request.method == 'POST':
            if request.POST.has_key('reserve'):

                book_id = request.POST.get('book id', None)
                book_name = models.book.objects.filter(id=book_id)[0].name
                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")
                models.appointment.objects.create(reader_id=request.session['user'], book_id=book_id,
                                                  book_name=book_name, time=time)
                searchword = request.POST.get('search', None)
                booklist = models.book.objects.filter(Q(name__icontains=searchword))
                searchlist = []
                for book in booklist:
                    if len(models.appointment.objects.filter(book_id=book.id)) == 0:
                        searchlist.append(book)
                return render(request, "reader_search.html", {'searchresult': searchlist,'login': request.session['user'], 'img':imgs})
            book_name = request.POST.get('search', None)
            try:
                booklist = models.book.objects.filter(Q(name__icontains=book_name) | Q(ISBN__icontains=book_name))
                searchlist = []
                for book in booklist:
                    if len(models.appointment.objects.filter(book_id=book.id)) == 0:
                        searchlist.append(book)
                if len(searchlist)==0:
                    return render(request, "reader_search.html",
                                  {'searchresult': searchlist, 'searchword':book_name, 'login': request.session['user'], 'img': imgs, 'ans':'No search result'})
                else:
                    return render(request, "reader_search.html", {'searchresult': searchlist, 'searchword':book_name,'login':request.session['user'], 'img':imgs})
            except:
                return render(request, "reader_search.html",{'login':request.session['user'], 'searchword':book_name})
        else:
            return render(request, "reader_search.html",{'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_lending(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                pwd=request.session['pwd'])
        lend = models.lend.objects.filter(reader_id=request.session['user'], isreturned='0')
        today_date = datetime.datetime.now()
        default_fine = float(models.default.objects.values('fine').first().values()[0])
        default_period = int(models.default.objects.values('return_period').first().values()[0])

        if len(lend) == 0:
            return render(request, "reader_lending.html",{'ans':'no lending books.','login':request.session['user']})
        for record in lend:
            lend_date = record.date
            Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
            record.remain_lendingtime = default_period - (today_date - Lend_date).days
            lenddays = (today_date - Lend_date).days
            if lenddays > default_period:
                record.topay_fine = (lenddays - default_period) * default_fine
            record.save()

        return render(request, "reader_lending.html", {'reader_lendingbooks':lend,'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_returnhistory(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        fine = models.lend.objects.filter(reader_id=request.session['user'])
        today_date = datetime.datetime.now()
        default_fine = float(models.default.objects.values('fine').first().values()[0])
        default_period = int(models.default.objects.values('return_period').first().values()[0])

        returnlist = models.lend.objects.filter(reader_id=request.session['user'], isreturned='1')
        if len(returnlist) == 0:
            return render(request, "reader_returnhistory.html",{'ans':'no borrow history.','login':request.session['user']})

        list = []
        for record in fine:
            if record.ispayed == '0':
                lend_date = record.date
                Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
                lenddays = (today_date - Lend_date).days
                if lenddays > default_period:
                    record.topay_fine = ( lenddays - default_period ) * default_fine
                    record.save()
            if record.isreturned == '1':
                list.append(record)
        total = 0.0
        for line in list:
            if line.ispayed == '0':
                total = total + float(line.topay_fine)
        return render(request, "reader_returnhistory.html", {'reader_returnhistory': list,'login':request.session['user'], 'total':total})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_lookupfine(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        fine = models.lend.objects.filter(reader_id=request.session['user'])
        today_date = datetime.datetime.now()
        default_fine = float(models.default.objects.values('fine').first().values()[0])
        default_period = int(models.default.objects.values('return_period').first().values()[0])

        if len(fine) == 0:
            return render(request, "reader_home.html",{'ans':'no fine history.','login':request.session['user']})

        list = []
        for record in fine:
            if record.ispayed == '0':
                lend_date = record.date
                Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
                lenddays = (today_date - Lend_date).days
                if lenddays > default_period:
                    record.topay_fine = ( lenddays - default_period ) * default_fine
                    record.save()
            if record.isreturned == '1':
                list.append(record)
        return render(request, "reader_to-pay fine.html", {'reader_finelist': list,'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def reader_reserve(request):
    try:
        models.reader.objects.get(id=request.session['user'],
                                     pwd=request.session['pwd'])
        try:
            appointment = models.appointment.objects.filter(reader_id=request.session['user'])
            now = datetime.datetime.now()
            for record in appointment:
                time = record.time
                appointment_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                if (now - appointment_time).seconds > 7200 or (now - appointment_time).days >= 1:
                    record.delete()
            appointment = models.appointment.objects.filter(reader_id=request.session['user'])
            if len(appointment) == 0:
                return render(request, "reader_reserve.html", {'ans': 'no appointment history.','login':request.session['user']})
            return render(request, "reader_reserve.html", {'reader_reserve': appointment,'login':request.session['user']})
        except:
            return HttpResponseRedirect('/reader_home/',{'login':request.session['user']})

    except:
        return HttpResponseRedirect('/homepage/')


def reader_changeinfo(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        r = models.reader.objects.filter(id=request.session['user'])[0]
        if request.method == 'POST':
            name = request.POST.get('name', None)
            pwd = request.POST.get('password', None)
            email = request.POST.get('email', None)
            reader = models.reader.objects.filter(id = request.session['user'])[0]
            reader.name = name
            reader.pwd = pwd
            reader.email = email
            reader.save()
            return render(request, "reader_changeinfo.html",{'r':reader,'ans':'Change successfully.', 'login':request.session['user']})
        else:
            return render(request, "reader_changeinfo.html",{'r':r, 'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def reader_bookdetail(request):
    try:
        models.reader.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        imgs = IMG.objects.all()
        if request.method == 'POST':
            book_id = request.POST.get('book_id', None)
            searchword = request.POST.get('search', None)
            print book_id
            book = models.book.objects.filter(id=book_id)[0]
            book_name = book.name

            return render(request, "reader_bookdetail.html", {'login':request.session['user'], 'book_name':book_name, 'i':book, 'img':imgs, 'searchword':searchword})
        return HttpResponseRedirect("/reader_home/", {'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def admin_home(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        return render(request, "admin_home.html", {'login':request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def admin_addlibrarian(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            id = request.POST.get('username', None)
            name = request.POST.get('name', None)
            models.librarian.objects.create(id=id, name=name)
            return render(request, "admin_addlibrarian.html", {'ans':'Add librarian '+id +' successfully', 'login':request.session['user']})
        else:
            return render(request, "admin_addlibrarian.html",{'login':request.session['user']})
    except:
        return render(request, "homepage.html")

def admin_manage(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            if request.POST.has_key('find'):
                word = request.POST.get('search', None)
                librarian = models.librarian.objects.filter(Q(name__icontains=word) | Q(id__icontains=word))
                return render(request, "admin_manage.html", {'librarian_list': librarian, 'login':request.session['user']})
            id = request.POST.get('librarian id', None)
            models.librarian.objects.filter(id=id).delete()
        librarian_list = models.librarian.objects.all()
        return render(request, "admin_manage.html", {'librarian_list': librarian_list, 'login':request.session['user']})
    except:
        return render(request, "homepage.html")

def admin_defaultvalue(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        fine = models.default.objects.values('fine').first().values()[0]
        period = models.default.objects.values('return_period').first().values()[0]
        deposit = models.default.objects.values('deposit').first().values()[0]
        if request.method == 'POST':
            fine = request.POST.get('fine', None)
            return_period = request.POST.get('return_period', None)
            deposit = request.POST.get('deposit', None)
            line = models.default.objects.all()[0]
            line.fine = fine
            line.return_period = return_period
            line.deposit = deposit
            line.save()
            return render(request, "admin_defaultvalue.html",{'fine':fine, 'period':return_period, 'deposit':deposit, 'login':request.session['user'],'ans':'Change successfully.'})
        return render(request, "admin_defaultvalue.html",{'fine':fine, 'period':period, 'deposit':deposit, 'login':request.session['user']})
    except:
        return render(request, "homepage.html")

def admin_request(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        #librarian = models.librarian.objects.all()
        if request.method == 'POST':
            if request.POST.has_key('agree'):
                id = request.POST.get('librarian id', None)
                lib = models.librarian.objects.filter(id=id)[0]
                lib.pwd = '00010001'
                lib.isrequest = '0'
                lib.save()
                return render(request, "admin_request.html", {'ans': 'The password of '+id+' is recovered.','login':request.session['user']})
            elif request.POST.has_key('refuse'):
                id = request.POST.get('librarian id', None)
                lib = models.librarian.objects.filter(id=id)[0]
                lib.isrequest = '0'
                lib.save()
        librarian = models.librarian.objects.filter(isrequest='1')
        if len(librarian) == 0:
            return render(request, "admin_request.html", {'ans': 'Without request!','login':request.session['user']})
        return render(request, "admin_request.html", {'request_list':librarian,'login':request.session['user']})
    except:
        return render(request, "homepage.html")

def admin_changeinfo(request):
    try:
        models.admin.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            old_pwd = request.POST.get('old password', None)
            new_pwd = request.POST.get('new password', None)
            lib = models.admin.objects.filter(id=request.session['user'], pwd=old_pwd)
            if len(lib) == 0:
                return render(request, "admin_changeinfo.html", {'ans': 'Old password wrong.','login': request.session['user']})
            else:
                lib[0].pwd = new_pwd
                lib[0].save()
                return render(request, "admin_changeinfo.html", {'ans':'Change successfully.','login': request.session['user']})
        else:
            return render(request, "admin_changeinfo.html",{'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def librarian_home(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])

        lend = models.lend.objects.all()
        today_date = datetime.datetime.now()
        default_period = models.default.objects.values('return_period').first()

        if len(lend) == 0:
            return render(request, "librarian_home.html", {'login': request.session['user']})
        for record in lend:
            lend_date = record.date
            Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
            record.remain_lendingtime = int(default_period.values()[0]) - (today_date - Lend_date).days
            record.save()

            if record.remain_lendingtime == 0:
                reader_email = models.reader.objects.filter(id=record.reader_id)[0].email
                send_mail('Outdue Alert!',
                          'Your borrowing book ' + record.book_name + ' is the last day. Please return the book or we will take fine.',
                          settings.EMAIL_FROM,
                          [reader_email,settings.EMAIL_FROM])

        return render(request, "librarian_home.html", {'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_managebook(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        deletelist = models.delete.objects.all()
        categories = models.category.objects.all()
        check = models.lend.objects.all()

        if request.method == 'POST':

            if request.POST.has_key('delete'):
                book_id = request.POST.get('book id', None)
                book_name = request.POST.get('book name', None)
                models.book.objects.filter(id=book_id)[0].delete()
                models.delete.objects.create(book_id=book_id, book_name=book_name, librarian_id=request.session['user'])
                searchlist = models.book.objects.all()
                for line in searchlist:
                    line.book_id = str(line.id)
                return render(request, "librarian_managebook.html", {'searchresult': searchlist, 'deletelist':deletelist, 'categories': categories, 'login': request.session['user'], 'check':check})
            else:
                book_name = request.POST.get('search', None)
                try:
                    searchlist = models.book.objects.filter(Q(name__icontains=book_name))
                    if len(searchlist) == 0:
                        return render(request, "librarian_managebook.html", {'ans': 'no such book.', 'deletelist':deletelist, 'categories': categories, 'login': request.session['user'], 'check':check})
                    for line in searchlist:
                        line.book_id = str(line.id)
                    return render(request, "librarian_managebook.html", {'searchresult': searchlist, 'deletelist':deletelist, 'categories': categories, 'login': request.session['user'], 'check':check})
                except:
                    return render(request, "librarian_managebook.html", {'deletelist':deletelist, 'categories': categories, 'login': request.session['user'], 'check':check})
        else:
            searchlist = models.book.objects.all()
            for line in searchlist:
                line.book_id = str(line.id)
            return render(request, "librarian_managebook.html", {'searchresult': searchlist, 'deletelist':deletelist, 'categories': categories, 'login': request.session['user'], 'check':check})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_addcategory(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            category = request.POST.get('category', None)
            models.category.objects.create(name=category)
        categories = models.category.objects.all()
        return render(request, "librarian_addcategory.html",{'categories':categories,'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_changepwd(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        l = models.librarian.objects.filter(id = request.session['user'])[0]
        if request.method == 'POST':
            name = request.POST.get('name', None)
            old_pwd = request.POST.get('old password', None)
            new_pwd = request.POST.get('new password', None)
            lib = models.librarian.objects.filter(id=request.session['user'], pwd=old_pwd)
            if len(lib) == 0:
                return render(request, "librarian_changepwd.html", {'ans': 'old password wrong.','login': request.session['user'], 'name':l.name})
            else:
                lib[0].pwd = new_pwd
                lib[0].save()
                return render(request, "librarian_changepwd.html", {'ans':'Change successfully.','login': request.session['user'], 'name':l.name})
        else:
            return render(request, "librarian_changepwd.html",{'login': request.session['user'], 'name':l.name})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_addreader(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            id = request.POST.get('username', None)
            email = request.POST.get('email', None)
            name = request.POST.get('name', None)
            sex = request.POST.get('sex', None)
            deposit = models.default.objects.values('deposit').first().values()[0]
            if models.reader.objects.filter(id=id):
                return render(request, "librarian_addreader.html", {'ans':'The id exists.','login': request.session['user']})
            models.reader.objects.create(id=id, sex=sex, email=email, name=name, deposit=deposit)

            Code = barcode.get_barcode_class('code39')
            bar = Code(str(id), barcode.writer.ImageWriter(), True)
            bar.save('static/images/bar')

            today_date = datetime.datetime.now().strftime("%Y-%m-%d")

            income_search = models.income.objects.filter(date=today_date)

            if len(income_search) == 0:
                models.income.objects.create(date=today_date, deposit=deposit, fine=0, sum=deposit)
            else:
                income = income_search[0]
                income.deposit = float(income.deposit) + float(deposit)
                income.sum = float(income.sum) + float(deposit)
                income.save()

            return render(request, "librarian_addreader.html", {'bar':id, 'login':request.session['user']})
        else:
            return render(request, "librarian_addreader.html", {'login':request.session['user']})
    except:
        return render(request, "homepage.html")


def librarian_managereader(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        try:
            no_id = request.session['no_id']
            readers = models.reader.objects.filter(id=no_id)
            request.session.pop('no_id', None)
            check = models.lend.objects.all()
            return render(request, "librarian_managereader.html", {'searchresult':readers, 'check':check,'login': request.session['user']})
        except:
            readers = models.reader.objects.all()
            if request.method == 'POST':
                if request.POST.has_key('delete'):
                    reader_id = request.POST.get('reader id', None)

                    lend = models.lend.objects.filter(reader_id=reader_id, isreturned='0')
                    if len(lend) != 0:
                        return render(request, "librarian_managereader.html",
                                      {'searchresult':readers, 'ans': 'the reader cannot be deleted because of the not-returned book.','login': request.session['user']})

                    fine = models.lend.objects.filter(reader_id=reader_id, ispayed='0')

                    if len(fine) != 0:
                        return render(request, "librarian_managereader.html",
                                      {'searchresult':readers, 'ans': 'the reader cannot be deleted because of the to-pay fine.','login': request.session['user']})
                    reader_deposit = float(models.reader.objects.filter(id=reader_id)[0].deposit)
                    models.reader.objects.filter(id=reader_id)[0].delete()

                    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    income_search = models.income.objects.filter(date=today_date)

                    if len(income_search) == 0:
                        models.income.objects.create(date=today_date, deposit=0-reader_deposit, fine=0, sum=0-reader_deposit)
                    else:
                        income = income_search[0]
                        income.deposit = float(income.deposit) - reader_deposit
                        income.sum = float(income.sum) - reader_deposit
                        income.save()
                elif request.POST.has_key('clear'):
                    reader_id = request.POST.get('reader id', None)
                    fine = float(models.reader.objects.filter(id=reader_id)[0].fine)
                    lend_record = models.lend.objects.filter(reader_id=reader_id, ispayed='0')
                    for l in lend_record:
                        l.ispayed = '1'
                        l.save()

                    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

                    income_search = models.income.objects.filter(date=today_date)

                    if len(income_search) == 0:
                        models.income.objects.create(date=today_date, deposit=0, fine=fine, sum=fine)
                    else:
                        income = income_search[0]
                        income.fine = float(income.fine) + fine
                        income.sum = float(income.sum) + fine
                        income.save()

                else:
                    reader_id = request.POST.get('search', None)
                    readers = models.reader.objects.filter(Q(id__icontains=reader_id)|Q(name__icontains=reader_id))
                    if len(readers) == 0:
                        return render(request, "librarian_managereader.html", {'searchresult':readers, 'ans': 'no reader of this id.','login': request.session['user']})
                    else:
                        r = readers[0]
                        lends = models.lend.objects.filter(reader_id=r.id, ispayed='0')
                        fine = 0
                        for l in lends:
                            fine = fine + float(l.topay_fine)
                        if float(r.fine) != float(fine):
                            r.fine = fine
                            r.save()
                        check = models.lend.objects.filter(reader_id=readers[0].id)
                        return render(request, "librarian_managereader.html", {'searchresult': readers, 'check':check,'login': request.session['user']})

            else:
                today_date = datetime.datetime.now()
                default_fine = float(models.default.objects.values('fine').first().values()[0])
                default_period = int(models.default.objects.values('return_period').first().values()[0])
                for r in readers:
                    lends = models.lend.objects.filter(reader_id=r.id, ispayed='0')
                    for record in lends:
                        lend_date = record.date
                        Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
                        lenddays = (today_date - Lend_date).days
                        if lenddays > default_period:
                            record.topay_fine = (lenddays - default_period) * default_fine
                            record.save()

            for r in readers:
                lends = models.lend.objects.filter(reader_id=r.id, ispayed='0')
                fine = 0
                for l in lends:
                    fine = fine + float(l.topay_fine)
                if float(r.fine) != float(fine):
                    r.fine = fine
                    r.save()
            check = models.lend.objects.all()
            return render(request, "librarian_managereader.html", {'searchresult': readers, 'check':check,'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def librarian_checkincome(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        income = models.income.objects.all()
        today_date = datetime.datetime.now()
        daily = 0.0
        daily_fine = 0.0
        daily_deposit = 0.0
        weekly = 0.0
        weekly_fine = 0.0
        weekly_deposit = 0.0
        monthly = 0.0
        monthly_fine = 0.0
        monthly_deposit = 0.0
        for record in income:
            date = record.date.split(' ')[0]
            income_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            days = (today_date - income_date).days
            if days == 0:
                daily = daily + float(record.sum)
                daily_fine = daily_fine + float(record.fine)
                daily_deposit = daily_deposit + float(record.deposit)
            if days >= 0 & days <7:
                weekly = weekly + float(record.sum)
                weekly_fine = weekly_fine + float(record.fine)
                weekly_deposit = weekly_deposit + float(record.deposit)
            if days >= 0 & days <30:
                monthly = monthly + float(record.sum)
                monthly_fine = monthly_fine + float(record.fine)
                monthly_deposit = monthly_deposit + float(record.deposit)

        if request.method == 'POST':
            date1 = request.POST.get('date1', None)
            date2 = request.POST.get('date2', None)
            date1 = '20' + date1
            date2 = '20' + date2
            date_sum = 0.0
            date_fine = 0.0
            date_deposit = 0.0
            for record in income:
                date = record.date
                if date >= date1 and date <= date2:
                    date_sum = date_sum + float(record.sum)
                    date_fine = date_fine + float(record.fine)
                    date_deposit = date_deposit + float(record.deposit)
            return render(request, "librarian_checkincome.html",
                          {'daily_fine':daily_fine, 'daily_deposit':daily_deposit, 'weekly_fine':weekly_fine, 'weekly_deposit':weekly_deposit,'monthly_fine':monthly_fine, 'monthly_deposit':monthly_deposit,
                              'income_daily': daily, 'income_weekly': weekly, 'income_monthly': monthly,
                           'date_sum': date_sum, 'date_fine':date_fine,'date_deposit':date_deposit,'login': request.session['user']})

        return render(request, "librarian_checkincome.html",
        {'daily_fine':daily_fine, 'daily_deposit':daily_deposit, 'weekly_fine':weekly_fine, 'weekly_deposit':weekly_deposit,'monthly_fine':monthly_fine, 'monthly_deposit':monthly_deposit,
            'income_daily':daily, 'income_weekly':weekly, 'income_monthly':monthly,'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_post(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            if request.POST.has_key('add'):
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                title = request.POST.get('title', None)
                word = request.POST.get('content', None)
                models.posttext.objects.create(title=title, content=word, date=now, auth=request.session['user'])
                posts = models.posttext.objects.all()
                return render(request, "librarian_post.html", {'posts':posts, 'login': request.session['user']})
            elif request.POST.has_key('delete'):
                id = request.POST.get('delete_id', None)
                models.posttext.objects.filter(id=id)[0].delete()
        posts = models.posttext.objects.all()
        return render(request, "librarian_post.html",{'posts':posts, 'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_lend(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])

        appointment = models.appointment.objects.all()
        now = datetime.datetime.now()
        for record in appointment:
            time = record.time
            appointment_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            print (now - appointment_time).seconds
            if (now - appointment_time).seconds > 7200 or (now - appointment_time).days >= 1:
                record.delete()

        if request.method == 'POST':
            book_id = request.POST.get('book_id', None)
            reader_id = request.POST.get('reader_id', None)

            today_date = datetime.datetime.now()
            default_fine = float(models.default.objects.values('fine').first().values()[0])
            default_period = int(models.default.objects.values('return_period').first().values()[0])
            lends = models.lend.objects.filter(reader_id=reader_id, ispayed='0')
            for record in lends:
                lend_date = record.date
                Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
                lenddays = (today_date - Lend_date).days
                if lenddays > default_period:
                    record.topay_fine = (lenddays - default_period) * default_fine
                    record.save()

            if len(models.book.objects.filter(id=book_id, islent='0')) == 0:
                return render(request, "librarian_lend.html", {'ans': 'The book id is wrong.','login': request.session['user']})
            if len(models.reader.objects.filter(id=reader_id)) == 0:
                return render(request, "librarian_lend.html", {'ans': 'The reader id is wrong.','login': request.session['user']})

            if len(models.lend.objects.filter(reader_id=reader_id, isreturned='0'))==3:
                return render(request, "librarian_lend.html", {'ans': 'The reader has kept 3 books.','login': request.session['user']})

            if len(models.appointment.objects.filter(book_id=book_id)) != 0:
                appointment = models.appointment.objects.filter(book_id=book_id)[0]
                if appointment.reader_id != reader_id:
                    return render(request, "librarian_lend.html",
                              {'ans': 'The book is reserved by '+appointment.reader_id+" .", 'login': request.session['user']})
            for f in lends:
                if float(f.topay_fine) > 0:
                    request.session['no_id'] = reader_id
                    return HttpResponseRedirect('/librarian_managereader/')
            book = models.book.objects.filter(id=book_id)[0]
            book.islent = '1'
            book.save()
            default_period = models.default.objects.values('return_period').first().values()[0]
            models.lend.objects.create(book_id=book_id, book_name=book.name, reader_id=reader_id,
                                       remain_lendingtime=default_period, date=datetime.datetime.now().strftime("%Y-%m-%d"))

            return render(request, "librarian_lend.html", {'ans': 'lend the book << ' + book.name + ' >> successfully','login': request.session['user']})
        return render(request, "librarian_lend.html",{'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')


def librarian_return(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            book_id = request.POST.get('book_id', None)
            book = models.book.objects.filter(id=book_id)
            if len(book) == 0:
                return render(request, "librarian_return.html", {'ans': 'Cannot find this book.',
                                                          'login': request.session['user']})
            nolend = models.book.objects.filter(id=book_id, islent='0')
            if len(nolend) != 0:
                return render(request, "librarian_return.html", {'ans': 'The book have not been borrowed.',
                                                          'login': request.session['user']})
            book_name = book[0].name
            lend_record = models.lend.objects.filter(book_id=book_id, isreturned='0')[0]

            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
            default_fine = float(models.default.objects.values('fine').first().values()[0])
            default_period = int(models.default.objects.values('return_period').first().values()[0])

            lend_date = lend_record.date
            Lend_date = datetime.datetime.strptime(lend_date, "%Y-%m-%d")
            lenddays = (datetime.datetime.now() - Lend_date).days
            if lenddays > default_period:
                fine = (lenddays - default_period) * default_fine
                lend_record.topay_fine = fine

                # income_search = models.income.objects.filter(date=today_date)
                # if len(income_search) == 0:
                #     models.income.objects.create(date=today_date, deposit=0, fine=fine, sum=fine)
                # else:
                #     income = income_search[0]
                #     income.fine = float(income.fine) + float(fine)
                #     income.sum = float(income.deposit) + float(fine)
                #     income.save()

            lend_record.isreturned = '1'
            lend_record.save()

            book = models.book.objects.filter(id=book_id)[0]
            book.islent = '0'
            book.save()

            if float(lend_record.topay_fine) > 0:
                reader_id = lend_record.reader_id
                request.session['no_id'] = reader_id
                return HttpResponseRedirect('/librarian_managereader/')

            return render(request, "librarian_return.html",{'ans': 'return the book << ' + book_name + ' >> successfully','login': request.session['user']})
        else:
            return render(request, "librarian_return.html",{'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_addbook(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        categories = models.category.objects.all()
        deletelist = models.delete.objects.all()
        if request.method == 'POST':
            newcategory = request.POST.get('newcategory', None)
            if len(newcategory) != 0:
                models.category.objects.create(name=newcategory)
                categories = models.category.objects.all()
                return render(request, "librarian_addbook.html",
                      {'deletelist': deletelist, 'categories': categories, 'login': request.session['user']})
            if request.POST.has_key('withoutISBN'):
                book_name = request.POST.get('bookname', None)
                isimg = models.IMG.objects.filter(img_name=book_name)
                if len(isimg)==0:
                    new_img = IMG(
                        img=request.FILES.get('img'),
                        img_name=book_name
                    )
                    new_img.save()
                floor = request.POST.get('floor', None)
                shelf = request.POST.get('shelf', None)
                area = request.POST.get('area', None)
                price = request.POST.get('price', None)
                category = request.POST.get('category', None)
                description = request.POST.get('description', None)
                num = request.POST.get('num', None)
                new_book = []
                for i in range(0, int(num)):
                    models.book.objects.create(name=book_name, floor=floor, shelf=shelf, area=area,
                                               price=price, category=category, description=description)
                    new_id = models.book.objects.last().id
                    new_book.append(new_id)
                    Code = barcode.get_barcode_class('code39')
                    bar = Code(str(new_id), barcode.writer.ImageWriter(), True)
                    bar.save('static/images/' + str(new_id))
                searchlist = models.book.objects.all()
                return render(request, "librarian_addbook.html",
                              {'ans': 'add book << ' + book_name + ' >> successfully.', 'new_book': new_book,
                               'deletelist': deletelist, 'categories': categories, 'searchresult': searchlist, 'login': request.session['user']})
            elif request.POST.has_key('withISBN'):
                ISBN = request.POST.get('ISBN', None)
                try:
                    # 将isbn作为变量传递到url中，得到对应的地址
                    url = 'https://api.douban.com/v2/book/isbn/' + ISBN
                    # 使用urllib模块打开url
                    response = urllib.urlopen(url)
                    # 读取url的网页内容，并用utf8编码
                    result = response.read().decode('utf8')
                    # 将返回的字符串转成json格式
                    result_json = json.loads(result)
                    book_name = result_json['title']
                    price = result_json['price']
                    description = result_json['summary']
                    img = str(result_json['image'])
                    img.replace('\\','')
                    img1 = img.replace('\\', '')
                    print img1
                    urlretrieve(img1, "E:/Bibliosoft_library/media/upload/"+book_name+".jpg")
                    print 'ok'
                    isimg = models.IMG.objects.filter(img_name=book_name)
                    if len(isimg) == 0:
                        new_img = IMG(
                            url='/media/upload/'+book_name+'.jpg',
                            img_name=book_name
                        )
                        new_img.save()
                    # 信息获取失败，抛出一个异常
                except :
                    print '?'
                floor = request.POST.get('floor', None)
                shelf = request.POST.get('shelf', None)
                area = request.POST.get('area', None)
                category = request.POST.get('category', None)
                num = request.POST.get('num', None)
                new_book = []
                for i in range(0, int(num)):
                    models.book.objects.create(name=book_name, floor=floor, shelf=shelf, area=area, ISBN=ISBN,
                                               price=price, category=category, description=description)
                    new_id = models.book.objects.last().id
                    new_book.append(new_id)
                    Code = barcode.get_barcode_class('code39')
                    bar = Code(str(new_id), barcode.writer.ImageWriter(), True)
                    bar.save('static/images/' + str(new_id))
                return render(request, "librarian_addbook.html",
                              {'ans': 'add book << ' + book_name + ' >> successfully.', 'new_book': new_book,
                               'deletelist': deletelist, 'categories': categories, 'login': request.session['user']})
            else:
                print 'else'
                return render(request, "librarian_addbook.html",
                              {'categories': categories, 'deletelist': deletelist, 'login': request.session['user']})
        else:
            print 'else'
            return render(request, "librarian_addbook.html", {'categories':categories, 'deletelist': deletelist, 'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')
'''
def librarian_deletelist(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        deletelist = models.delete.objects.all()
        if len(deletelist) == 0:
            return render(request, "librarian_deletelist.html", {'ans':'no delete history.'})
        else:
            return render(request, "librarian_deletelist.html", {'deletelist':deletelist})
    except:
        return HttpResponseRedirect('/homepage/')
'''
def librarian_editbook(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        categories = models.category.objects.all()
        if request.method == 'POST':
            if request.POST.has_key('submit'):
                id = request.POST.get('book id', None)
                book = models.book.objects.filter(id=id)[0]
                book.name = request.POST.get('name', None)
                book.floor = request.POST.get('floor', None)
                book.shelf = request.POST.get('shelf', None)
                book.area = request.POST.get('area', None)
                book.price = request.POST.get('price', None)
                book.category = request.POST.get('category', None)
                book.description = request.POST.get('description', None)
                book.save()

            elif request.POST.has_key('edit'):
                book_id = request.POST.get('book id', None)
                book = models.book.objects.filter(id=book_id)[0]
            return render(request, "librarian_editbook.html", {'book': book, 'categories':categories,'login': request.session['user']})
        else:
            return render(request, "librarian_editbook.html", {'categories':categories,'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_checkfine(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            reader_id = request.POST.get('reader id', None)
            finelist = models.lend.objects.filter(reader_id=reader_id)
            if len(finelist) == 0:
                return render(request, "librarian_checkfine.html", {'ans':'no fine history.'})
            return render(request, "librarian_checkfine.html", {'finelist':finelist})
        return render(request, "librarian_checkfine.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_checklend(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            reader_id = request.POST.get('reader id', None)
            lendlist = models.lend.objects.filter(reader_id=reader_id)
            if len(lendlist)==0:
                return render(request, "librarian_checklend.html",{'ans':'no lend history.'})
            return render(request, "librarian_checklend.html", {'lendlist':lendlist})
        return render(request, "librarian_checklend.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_checkreturn(request):
    try:
        models.librarian.objects.get(id = request.session['user'],
                                    pwd=request.session['pwd'])
        if request.method == 'POST':
            reader_id = request.POST.get('reader id', None)
            lendlist = models.lend.objects.filter(reader_id=reader_id)
            returnlist = []
            if len(lendlist) == 0:
                render(request, "librarian_checkreturn.html", {'ans':'no return history.'})
            for line in lendlist:
                if line.isreturned == '1':
                    returnlist.append(line)
            if len(returnlist) == 0:
                return render(request, "librarian_checkreturn.html", {'ans': 'no return history.'})
            else:
                return render(request, "librarian_checkreturn.html", {'returnlist':returnlist})
        return render(request, "librarian_checklend.html")
    except:
        return HttpResponseRedirect('/homepage/')

def librarian_detail(request):
    #return render(request, "librarian_detail.html", {'login': request.session['user']})
    try:
        models.librarian.objects.get(id=request.session['user'],
                                     pwd=request.session['pwd'])
        if request.method=='POST':
            if request.POST.has_key('edit'):
                title = request.POST.get('title', None)
                content = request.POST.get('content', None)
                post_id = request.POST.get('post_id',None)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                post = models.posttext.objects.filter(id=post_id)[0]
                post.title = title
                post.content = content
                post.date = now
                post.auth = request.session['user']
                post.save()
                return render(request, "librarian_detail.html", {'login': request.session['user'], 'post':post})
            post_id = request.POST.get('post_id', None)
            print post_id
            post = models.posttext.objects.filter(id=post_id)[0]
            return render(request, "librarian_detail.html", {'login': request.session['user'], 'post':post})

        return render(request, "librarian_detail.html", {'login': request.session['user']})
    except:
        return HttpResponseRedirect('/homepage/')