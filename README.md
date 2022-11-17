
# Rail-Safar

A train management system built using Django framework. It is designed for passengers/users to search,book and cancel train tickets.


## This system is built for the purpose:

* Signup, Login and Logout securely
* Search train
* View train schedules/timetable
* Check seat availability
* Login using OTP
* Confirm booking
* View booking history
* Fare enquiry
* Ticket cancellation
* Change password
* Forgot password
  
## Installation
Python and Django need to be installed

```bash
pip install django
```

## Usage

Go to the Rail-Safar folder and run

```bash
python manage.py runserver
```

Then go to the browser and enter the url **http://127.0.0.1:8000/railways/login_view**

## Navbar

* Before authentication, navbar only displays login and sign up options.

* After authentication, navbar displays all sections. 

* A user cannot jump from one url to another without logging in.

## Sign up

Enter a unique username, email address and password to create an account. The directions for a strong password are also provided.

![alt text](https://imgur.com/tINXbYH.png)

## Login 

* If you are an existing user, enter username and password to login. Else, sign up to create an account.

* Also a new admin user can be created using

```bash
python manage.py createsuperuser

or

python manage.py createsuperuser --username <username> --password <password>

```
![alt text](https://imgur.com/49Ep4De.png)


## Login with OTP

* Users who haven't signed up can still login by using this feature.

* Enter a unique username and valid email address. OTP will be sent to the email address you entered. 

* You'll be redirected back to login page where you'll have to enter the same username and OTP to login.

![alt text](https://imgur.com/dBHnWRH.png)


## Forgot Passsword

* Users who forgot their old password can use this section to login with new passoword/otp, then set a new password of their choice by navigating to "change password" section.

* Only pre existing user (users who have already signed up) can use this feature.

* Enter your email for your old username and new password/otp to be sent. Use these credentials to login.

![alt text](https://imgur.com/XutgkS4.png)


## Search 

* You'll be redirected to this page after logging in.

* Enter origin station, destination and date of journey. 

![alt text](https://imgur.com/x8KqwVW.png)

## Result

* Displays all trains which passes through your origin/destination station and runs on your selected DOJ.

* Select the train, coach and total number of passengers.

![alt text](https://imgur.com/NFqsTQv.png)

## Timetable

Displays the days on which the train runs and the ETA at each station.

![alt text](https://imgur.com/9tDtOSr.png)


## Passenger details

Enter name, age and gender of each passenger.

![alt text](https://imgur.com/KDoO4XF.png)


## Review booking

* Displays the passenger details, train name and number, coach, DOJ, source and destination stations.

* Fare is calculated on basis of distance travelled, coach, number of passengers and type of train (Premium or Express)

* Only signed up users can confirm booking. Users logged in with OTP cannot.

* Once confirmed, a confirmation email will be sent to your registered email address with all the details. This also serves the purpose of a ticket.

![alt text](https://imgur.com/Tvh7Aty.png)

## Booking history

* Once the booking is confirmed, you'll be redirected to this section.

* It displays history of all the bookings done by the user.

* You can also cancel bookings from this section.

![alt text](https://imgur.com/yZW7NjO.png)

![alt text](https://imgur.com/sfGP1S2.png)


## Change password

* A User who has logged in with OTP will not be allowed to use this section.

* Signed up users should enter their old and new passwords to change password.

* Once changed, you'll be logged out of the system and have to login using the new password.


![alt text](https://imgur.com/Sddy4yx.png)


## Admin page

Go to the browser and enter the url  **http://127.0.0.1:8000/admin**

![alt text](https://imgur.com/LWWROT8.png)

![alt text](https://imgur.com/bp94N8a.png)

If a new train is introduced, the following models should be updated in order: 

**Trains --> Stations --> Train days --> Distance**











