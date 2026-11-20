"""Eshopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('addproduct',views.addproduct),
    path('addproductbuttonsubmit',views.addproductbuttonsubmit),
    path('changepassword',views.changepassword),
    path('changepasswordbuttonsubmit', views.changepasswordbuttonsubmit),
    path('editproduct/<id>',views.editproduct),
    path('editproductbuttonsubmit',views.editproductbuttonsubmit),
    path('forgetchangepassword',views.forgetchangepassword),
    path('forgetchangepasswordbuttonsubmit',views.forgetchangepasswordbuttonsubmit),
    path('forgetpasswordotp',views.forgetpasswordotp),
    path('forgetpasswordotpbuttonsubmit',views.forgetpasswordotpbuttonsubmit),
    path('forgetpasswordemailcheck',views.forgetpasswordemailcheck),
    path('forgetpasswordemailcheckbuttonsubmit', views.forgetpasswordemailcheckbuttonsubmit),
    path('home',views.home),
    path('',views.log),
    path('loginbuttonsubmit', views.loginbuttonsubmit),
    path('orderhistory',views.orderhistory),
    path('rejectreason',views.rejectreason),
    path('rejectreasonbuttonsubmit',views.rejectreasonbuttonsubmit),
    path('salerequesthistory',views.salerequesthistory),
    path('verifyworker',views.verifyworker),
    path('viewproducts',views.viewproducts),
    path('viewreview',views.viewreview),
    path('viewuserfeedback',views.viewuserfeedback),
    path('viewusers',views.viewusers),
    path('viewworkers',views.viewworkers),
    path('vieworder',views.vieworder),
    path('viewordereditem/<id>',views.viewordereditem),
    path('viewpayment',views.viewpayment),
    path('viewsalerequest',views.viewsalerequest),
    path('worker_approve/<id>',views.worker_approve),
    path('worker_reject/<id>',views.worker_reject),
    path('removeproduct/<id>',views.removeproduct),
    path('salerequest_approve/<id>', views.salerequest_approve),
    path('salerequest_approve_post/<id>', views.salerequest_approve_post),
    path('salerequest_reject/<id>', views.salerequest_reject),
    path('updatedeliverystatus/<id>',views.updatedeliverystatus),
    path('productbycolour/<id>',views.productbycolour),
    path('productbycolour_buttonclick',views.productbycolour_buttonclick),
    path('viewbycolour/<id>',views.viewbycolour),
    path('deleteproductimage/<id>',views.deleteproductimage),
    path('shippingstatus/<id>',views.shippingstatus),
    path('shippingstatus_buttonclick',views.shippingstatus_buttonclick),
    path('viewdeliverystatus',views.viewdeliverystatus),
    path('logout',views.logouts),
    path('addstock/<id>',views.addstock),
    path('addstock_buttonclick',views.addstock_buttonclick),
    path('editstock/<id>',views.editstock),
    path('editstock_buttonclick',views.editstock_buttonclick),
    path('viewstock/<id>',views.viewstock),
    path('deletestock/<id>',views.deletestock),



#     =======================================================================

    path('addproductworker',views.addproductworker),
    path('addproductworker_buttonclick',views.addproductworker_buttonclick),
    path('changepasswordworker',views.changepasswordworker),
    path('changepasswordworker_buttonclick',views.changepasswordworker_buttonclick),
    path('editproductworker/<id>',views.editproductworker),
    path('homeworker',views.homeworker),
    path('register',views.register),
    path('register_buttonclick',views.register_buttonclick),
    path('sendsalerequest/<id>',views.sendsalerequest),
    path('sendsalerequest_buttonclick/<id>',views.sendsalerequest_buttonclick),
    path('viewpaymenthistoryworker',views.viewpaymenthistoryworker),
    path('viewproductworker',views.viewproductworker),
    path('viewprofileandupdate',views.viewprofileandupdate),
    path('viewprofileandupdate_buttonclick',views.viewprofileandupdate_buttonclick),
    path('viewrequesthistoryworker',views.viewrequesthistoryworker),
    path('viewreviewworker',views.viewreviewworker),
    path('viewsalerequestworker',views.viewsalerequestworker),
    path('editproductworker_buttonclick/<id>',views.editproductworker_buttonclick),
    path('removeproductworker/<id>',views.removeproductworker),
    path('mybalance',views.mybalance),
    path('mybalance_buttonclick',views.mybalance_buttonclick),
    path('withdraw',views.withdraw),
    path('withdraw_buttonclick',views.withdraw_buttonclick),
    path('default',views.default),
    path('paymentsuccess',views.paymentsuccess),

#    ============================================================================

    path('addtocart/<id>',views.addtocart),
    path('addtocart_buttonclick',views.addtocart_buttonclick),
    path('changepassworduser',views.changepassworduser),
    path('changepassworduser_buttonclick',views.changepassworduser_buttonclick),
    path('homeuser',views.homeuser),
    path('registeruser',views.registeruser),
    path('registeruser_buttonclick',views.registeruser_buttonclick),
    path('sendfeedbackuser',views.sendfeedbackuser),
    path('sendfeedbackuser_buttonclick',views.sendfeedbackuser_buttonclick),
    path('sendreviewuser/<id>',views.sendreviewuser),
    path('sendreviewuser_buttonclick',views.sendreviewuser_buttonclick),
    path('viewandeditprofileuser',views.viewandeditprofileuser),
    path('viewandeditprofileuser_buttonclick',views.viewandeditprofileuser_buttonclick),
    path('viewcart',views.viewcart),
    path('viewordersanditemsuser',views.viewordersanditemsuser),
    path('viewproductuser/<id>',views.viewproductuser),
    path('viewreviewuser/<id>',views.viewreviewuser),
    path('removecart/<id>',views.removecart),
    path('makepayment/<id>',views.makepayment),
    path('makepayment_buttonclick',views.makepayment_buttonclick),
    path('payment',views.payment),
    path('orderpaymentsuccess',views.orderpaymentsuccess),
    path('placeorder',views.placeorder),
    path('allpayment',views.allpayment),
    path('allpayment_buttonclick',views.allpayment_buttonclick),
    path('payall',views.payall),
    path('uviewdeliverystatus/<id>',views.uviewdeliverystatus),
    path('categoriesuser',views.categoriesuser),


]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)