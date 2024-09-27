from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart/', views.cart_page, name='cart_page'),
    path('games',views.games,name="games"),    
    path('games/<str:name>',views.gamesview,name="games"), 
    path('games/<str:gname>/<str:tname>',views.games_details,name="games_details"), 
    path('book_game/',views.book_game, name='book_game'),
    path('cancel-booking/',views.cancel_booking_view, name='cancel_booking'),
    path('about/', views.about, name='about'),
    path('admin/',views.admin, name='admin'),
    path('forgot-password/', views.forgot_password, name="forgot_password"),
    path('verify-otp/', views.verify_otp, name="verify_otp"),
   
    

   

    
    
    
     
    

   

  
]

