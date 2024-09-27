from django.shortcuts import render,redirect
from .models import*
from django.contrib import messages
from turff.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    return render(request,"turff/index.html")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect("/")

def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Login  in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"turff/login.html")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration sucess You can login now....!")
            return redirect('/login') 
    return render(request,"turff/register.html",{'form':form})

def cart_page(request):
    cart_items = Bookingss.objects.filter(user=request.user)
    total_cost = sum(item.total_cost for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
    }
    return render(request, 'turff/cart.html', context)




from django.shortcuts import render
from .models import Bookingss





def games(request):
    catagory=GameCatagory.objects.filter(status=0)
    return render(request,"turff/games.html",{"catagory":catagory})

def gamesview(request, name):
    if (GameCatagory.objects.filter(name=name,status=0)):
        game = TurfCatagory.objects.filter(game_category__name=name)
        return render(request, "turff/gamess/index.html", {"game":game,"category_name":name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('games')


def games_details(request, gname, tname):
    if (GameCatagory.objects.filter(name=gname, status=0)):
        if (TurfCatagory.objects.filter(name=tname, status=0)):
            game = TurfCatagory.objects.filter(name=tname, status=0).first()
            return render(request, "turff/gamess/games_details.html", {"game": game})
        else:
            messages.error(request, "No Such Product Found")
            return redirect('games')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('games')
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json



from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import TurfCatagory, GameCatagory, Bookingss
from django.contrib.auth.decorators import login_required
from django.conf import settings

@csrf_exempt
@login_required
def book_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            turf = get_object_or_404(TurfCatagory, id=data['turf_id'])
            game_category = get_object_or_404(GameCatagory, id=data['game_category_id'])
            booking_date = data['booking_date']
            time_slot = data['time_slot']
            user_email = data.get('email')

            if Bookingss.objects.filter(
                user=user,
                turf=turf,
                game_category=game_category,
                booking_date=booking_date,
                time_slot=time_slot
            ).exists():
                return JsonResponse({'status': 'error', 'message': 'You have already booked this slot. Please select another slot.'})

            if Bookingss.objects.filter(turf=turf, booking_date=booking_date, time_slot=time_slot).exists():
                return JsonResponse({'status': 'error', 'message': 'This slot is already booked someone. Please select another slot.'})

            game_name = game_category.name
            game_description = game_category.description
            turf_name = turf.name
            turf_description = turf.description
            total_cost = turf.total_cost

            booking = Bookingss.objects.create(
                user=user,
                turf=turf,
                game_category=game_category,
                booking_date=booking_date,
                time_slot=time_slot,
                game_name=game_name,
                game_description=game_description,
                turf_name=turf_name,
                turf_description=turf_description,
                total_cost=total_cost
            )

            subject = 'Booking Confirmation'
            message = f'Your booking for {game_name} at {turf_name} on {booking_date} at {time_slot} is confirmed.'
            sender_email = settings.EMAIL_HOST_USER
            recipient_email = user_email
            send_mail(subject, message, sender_email, [recipient_email])

            return JsonResponse({'status': 'success', 'message': 'Booking successful!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def cancel_booking_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            turf_id = data['turf_id']
            booking_date = data['booking_date']
            time_slot = data['time_slot']

            # Find the booking in the database
            booking = Bookingss.objects.get(
                turf_id=turf_id,
                booking_date=booking_date,
                time_slot=time_slot,
                user=request.user
            )
            booking.delete()
            return JsonResponse({'status': 'success', 'message': 'Booking cancelled successfully.'})
        except Bookingss.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Booking not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    


def about(request):
    return render(request,"turff/about.html")


def admin(request):
    return render(request, 'admin')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib import messages
import random

User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            # Generate OTP (example)
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            request.session['username'] = username
            request.session['email'] = email

            messages.success(request, f'OTP for {username} ({email}): {otp}')
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, "User with provided username and email does not exist.")
            return redirect('forgot_password')
    return render(request, 'turff/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if entered_otp == str(stored_otp):
            username = request.session.get('username')
            email = request.session.get('email')
            user = User.objects.get(username=username, email=email)
            login(request, user)
            del request.session['otp']
            del request.session['username']
            del request.session['email']
            messages.success(request, f'Logged in successfully as {username}')
            return redirect('home')  # Redirect to home or any other page after successful login
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')
    return render(request, 'turff/verify_otp.html')





