import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib import messages
from .otp import email_otp, booking_confirmation
from django.core.mail import send_mail
from datetime import datetime, date, time
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.hashers import check_password


def layout(request):
    return render(request, 'railways/layout.html')


def login_view(request):
    if request.method == 'POST':
        if request.POST.get('submit_login') == 'submitted':
            username = request.POST.get('username')
            password = request.POST.get('password')
            pwd_otp = request.session.get('otp')
            otp_username = request.session.get('otp_username')
            u = User.objects.filter(username=username).first()
            user = authenticate(username=username, password=password)
            if u:
                if user:
                    login(request, user)
                    request.session['username'] = username
                    messages.success(request, f" Logged in successfully ")
                    return redirect('search')
                else:
                    messages.error(request, "Incorrect password")
            else:
                messages.error(request, "Username is incorrect or does not exist")
    return render(request, 'railways/login_view.html')


class UserRegForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def signup(request):
    form = UserRegForm()
    if request.method == "POST":
        form = UserRegForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password1')
        cnf_password = request.POST.get('password2')
        user_email = request.POST.get('email')
        e = User.objects.filter(email=user_email).first()
        if password != cnf_password:
            messages.error(request, "Passwords do not match. Please try again")
            form = UserRegForm()
        elif e:
            messages.error(request, "Email address already exists. Try again.")
            form = UserRegForm()
        elif form.is_valid():
            n = User.objects.create_user(username=username, password=password, email=user_email)
            n.save()
            messages.success(request, f"Account created for {username}. Please login.")
            return redirect('login_view')

    return render(request, 'railways/signup.html', {'form': form})


@login_required
def search(request):
    s = Stations.objects.all()
    stations_list = []
    for item in s:
        stations_list.append(item)
    if request.method == "POST":
        if request.POST.get('search'):
            input_origin = request.POST.get('origin')
            input_destination = request.POST.get('destination')
            my_date = request.POST.get('datetime')
            my_date_str = my_date.split('T')[0]
            date_now = datetime.strptime(my_date, '%Y-%m-%dT%H:%M')
            today = datetime.today()

            if date_now >= today:
                isoweekday = datetime.strptime(my_date_str, '%Y-%m-%d').isoweekday()
                print(isoweekday)
                d1 = Days.objects.get(id=isoweekday)
                td1 = TrainDays.objects.filter(train_days=d1).all()
                train_day = []
                for item in td1:
                    train_day.append(item.trains.train_no)
                request.session['train_day'] = train_day
                if input_origin == input_destination:
                    messages.error(request, "origin and destination cannot be same")
                    return redirect('search')
                else:
                    request.session['input_origin'] = input_origin
                    request.session['input_destination'] = input_destination
                    request.session['my_date_str'] = my_date_str
                    return redirect('result')
            else:
                messages.error(request, "Invalid date")

    return render(request, 'railways/search.html', {'stations_list': stations_list})


@login_required
def result(request):
    my_date_str = request.session.get('my_date_str')
    train_day = request.session.get('train_day')
    st_org = Stations.objects.get(code=request.session.get('input_origin'))
    st_dt = Stations.objects.get(code=request.session.get('input_destination'))
    train_list = []
    s1 = []
    train_for_date = True
    direct_train = True

    for train1 in st_org.train.all():
        for train2 in st_dt.train.all():
            if train1.train_no == train2.train_no:
                direct_train = False
                if train1.train_no in train_day:
                    train_for_date = False
                    train_list.append(train1)
                    t1 = Trains.objects.get(train_no=train1.train_no)
                    s = Seats.objects.filter(train_no=t1, date=my_date_str, from_st=st_org, to_st=st_dt).all()
                    if s:
                        s1.append(s)
                    else:
                        Seats(train_no=t1, date=my_date_str, from_st=st_org, to_st=st_dt).save()
                        s = Seats.objects.filter(train_no=t1, date=my_date_str, from_st=st_org, to_st=st_dt).all()
                        s1.append(s)

    if direct_train:
        messages.error(request, "No direct train available between the selected route")
        return redirect('search')

    if train_for_date:
        messages.error(request, "No train for selected date. Choose alternate date.")
        return redirect('search')

    if request.method == "POST":
        if request.POST.get('tt'):
            request.session['train_no'] = request.POST.get('tt')
            return redirect('timetable')
        elif request.POST.get('submit_train'):
            if request.POST.get('train'):
                if request.POST.get('seat'):
                    psg1 = int(request.POST.get('psg'))
                    train_no = request.POST.get('train')
                    t2 = Trains.objects.get(train_no=train_no)
                    s_psg = Seats.objects.get(train_no=t2, date=my_date_str, from_st=st_org, to_st=st_dt)
                    seat = request.POST.get('seat')
                    if (seat == '3-AC' and psg1 <= s_psg.ac) or (seat == 'SL' and psg1 <= s_psg.sl):
                        request.session['seat'] = seat
                        request.session['psg'] = psg1
                        request.session['train'] = train_no
                        return redirect('details')
                    else:
                        messages.error(request, "not enough seats")

                else:
                    messages.error(request, "Please choose a seat")
            else:
                messages.error(request, "Please choose a train")

    return render(request, 'railways/result.html', {'train_list': train_list,
                                                    's1': s1
                                                    })


@login_required
def timetable(request):
    train_no = request.session.get('train_no')
    t1 = Trains.objects.filter(train_no=train_no).first()
    tt1 = Timetable.objects.filter(train_no=t1).all()
    train = Trains.objects.get(train_no=train_no)
    td1 = TrainDays.objects.get(trains=train)
    return render(request, 'railways/timetable.html', {'tt1': tt1,
                                                       'days': td1.train_days.all()
                                                       })


@login_required
def details(request):
    seat = request.session.get('seat')
    psg = request.session.get('psg')
    psg_loop = []
    for item in range(1, psg + 1):
        psg_loop.append(item)
    request.session['psg_loop'] = psg_loop
    if request.method == "POST":
        if request.POST.get('submit_details'):
            psg_list = []
            for i in range(1, psg + 1):
                psg_name = request.POST.get(f'name-{i}')
                psg_age = request.POST.get(f'age-{i}')
                psg_gender = request.POST.get(f'gender-{i}')

                if psg_name != "":
                    if psg_age != "":
                        if psg_gender:
                            if int(psg_age) in range(1, 150):
                                request.session[f'psg_name{i}'] = psg_name
                                request.session[f'psg_age{i}'] = int(psg_age)
                                request.session[f'psg_gender{i}'] = psg_gender
                                psg_list1 = [psg_name, psg_age, psg_gender]
                                print(psg_list1)
                                psg_list.append(psg_list1)
                                request.session['psg_list'] = psg_list

                            else:
                                messages.error(request, "Please enter valid age")
                        else:
                            messages.error(request, "Please select gender")
                    else:
                        messages.error(request, "Please enter age")
                else:
                    messages.error(request, "Please enter name")
            return redirect('review')
    return render(request, 'railways/details.html', {'psg': psg_loop})


def otp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        u = User.objects.filter(username=username).first()
        if u:
            messages.error(request, f" Username: '{username}' already exists. Try another.")
            return redirect('otp')
        else:
            request.session['otp_username'] = username
            otp = str(email_otp(email, username))
            request.session['otp'] = otp
            n = User.objects.create_user(username=username, password=otp, first_name='OTP', email=email)
            n.save()
            messages.success(request, f" OTP sent to email address: {email}")
            return redirect('login_view')

    return render(request, 'railways/otp.html')


@login_required
def review(request):
    train_no = request.session.get('train')
    train_name = Trains.objects.get(train_no=train_no)
    coach = request.session.get('seat')
    psg_info = request.session.get('psg_list')
    print(psg_info)
    psg = request.session.get('psg')
    my_date_str = request.session.get('my_date_str')

    input_origin = request.session.get('input_origin')
    input_destination = request.session.get('input_destination')
    s_org = Stations.objects.get(code=input_origin)
    s_des = Stations.objects.get(code=input_destination)
    t1 = Trains.objects.get(train_no=train_no)
    tt_org = Timetable.objects.filter(train_no=t1.id) & Timetable.objects.filter(station_code=s_org.id)
    tt_des = Timetable.objects.filter(train_no=t1.id) & Timetable.objects.filter(station_code=s_des.id)
    t = Trains.objects.get(train_no=train_no)
    seat = Seats.objects.get(train_no=t, date=my_date_str, from_st=s_org, to_st=s_des)
    user = User.objects.get(username=request.session.get('username'))
    d = Distance.objects.get(Q(st_from=s_org, st_to=s_des) | Q(st_from=s_des, st_to=s_org))

    if t.type.type == 'P':
        if coach == '3-AC':
            fare = (t.type.base_fare + (d.distance * t.type.ac_km)) * psg
        else:
            fare = (t.type.base_fare + (d.distance * t.type.sl_km)) * psg
    elif t.type.type == 'E':
        if coach == '3-AC':
            fare = (t.type.base_fare + (d.distance * t.type.ac_km)) * psg
        else:
            fare = (t.type.base_fare + (d.distance * t.type.sl_km)) * psg

    for item in tt_org:
        time_org = item.timing
    for item in tt_des:
        time_des = item.timing
    if request.method == "POST":
        if request.POST.get('confirm') and user.first_name != 'OTP':
            if coach == 'SL':
                seat.sl = seat.sl - psg
            elif coach == '3-AC':
                seat.ac = seat.ac - psg
            seat.save()

            for i in range(1, psg + 1):
                psg_name = request.session.get(f'psg_name{i}')
                psg_age = request.session.get(f'psg_age{i}')
                psg_gender = request.session.get(f'psg_gender{i}')
                train_no = request.session.get('train')
                my_date_str = request.session.get('my_date_str')
                username = request.session.get('username')
                p = Psg(username=username, name=psg_name, age=psg_age, gender=psg_gender, train=train_no, coach=coach,
                        origin=s_org, destination=s_des, doj=my_date_str)
                p.save()

            u = User.objects.get(username=request.session.get('username'))
            email_to = u.email
            booking_confirmation(username, email_to, my_date_str, s_org, s_des)
            messages.success(request, "Booking confirmed. Confirmation email is sent to your registered "
                                      "email address.")
            return redirect('history')
        else:
            messages.error(request, "You have logged in using OTP. Please create an account for booking.")
            return redirect('logout')
    return render(request, 'railways/review.html', {'train_name': train_name,
                                                    'train_no': train_no,
                                                    'coach': coach,
                                                    'input_origin': input_origin,
                                                    'input_destination': input_destination,
                                                    'time_org': time_org,
                                                    'time_des': time_des,
                                                    'psg_info': psg_info,
                                                    'my_date_str': my_date_str,
                                                    'fare': fare
                                                    })


@login_required
def history(request):
    p1 = Psg.objects.filter(username=request.session.get('username'))
    p = p1.order_by('doj').all()

    if request.method == "POST":
        if request.POST.get('submit_cancel'):
            p_id = request.POST.get("cancel")
            if p_id is not None:
                p1 = Psg.objects.get(id=p_id)
                t = Trains.objects.get(train_no=p1.train)
                s = Seats.objects.get(date=p1.doj, train_no=t, from_st=p1.origin, to_st=p1.destination)
                if p1.coach == '3-AC':
                    s.ac += 1
                elif p1.coach == 'SL':
                    s.sl += 1
                s.save()
                p1.delete()
                messages.success(request, "Booking cancelled successfully")
            else:
                messages.error(request, "Please select a booking to cancel.")

    return render(request, 'railways/history.html', {'p': p})


@login_required
def logout_view(request):
    username = request.session.get('username')
    u = User.objects.filter(first_name='OTP', username=username).first()
    if u:
        u.delete()
    logout(request)
    return redirect('login_view')
    return render(request, 'railways/logout_view.html')


@login_required
def change_pwd(request):
    username = request.session.get('username')
    user = User.objects.get(username=username)
    if user.first_name == "OTP":
        messages.error(request, "Users logged in with OTP cannot change password. Please sign up.")
        return redirect('search')
    else:
        old_pwd = request.POST.get('old_pwd')
        new_pwd1 = request.POST.get('new_pwd1')
        new_pwd2 = request.POST.get('new_pwd2')
        if request.method == "POST":
            if request.POST.get('change_pwd'):
                if check_password(old_pwd, user.password):
                    if new_pwd1 == new_pwd2:
                        if old_pwd != new_pwd1:
                            user.set_password(new_pwd1)
                            user.save()
                            messages.success(request, "Password changed successfully. Login again")
                            return redirect('login_view')
                        else:
                            messages.error(request, "Old and new passwords are same. Try again")
                            return redirect('change_pwd')

                    else:
                        messages.error(request, "New passwords does not match. Try again")
                        return redirect('change_pwd')
                else:
                    messages.error(request, "Incorrect old password. Try again")
                    return redirect('change_pwd')

    return render(request, 'railways/change_pwd.html')
