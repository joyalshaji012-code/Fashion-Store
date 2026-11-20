import random
import smtplib

import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.cache import never_cache

from Myapp.models import Customers, Products, Workers, Review, Feedback, Orders, Ordereditems, Salerequests, Carts, \
    Balance, Productsbycolor, Deliverystatus, Stock


@login_required(login_url='/')
@never_cache
# print(make_password("123456"))
def addproduct(request):
    return render(request,'admin/add products.html')
def addproductbuttonsubmit(request):
    categories = request.POST['category']
    name = request.POST['product_name']
    description = request.POST['description']
    image = request.FILES['image']
    fs = FileSystemStorage()
    image = fs.save(image.name,image)
    image = fs.url(image)
    price = request.POST['price']
    # if Products.objects.filter()
    obj = Products()
    obj.name = name
    obj.categories = categories
    obj.description = description
    obj.image = image
    obj.price = price
    obj.status="Admin"
    obj.save()
    return HttpResponse("<script>alert('Product added successfully');window.location='/viewproduct';</script>")

@login_required(login_url='/')
@never_cache
def changepassword(request):
    return render(request,'admin/change password.html')
def changepasswordbuttonsubmit(request):
    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    if currentpassword == newpassword:
        return HttpResponse(
            "<script>alert('This password is already exist,Enter new password');window.location='/changepassword';</script>")
    if newpassword != confirmpassword:
        return HttpResponse("<script>alert('Passwords do not match');window.location='/changepassword';</script>")
    User.objects.filter(id=request.user.id).update(password=make_password(confirmpassword))

    return HttpResponse("<script>alert('Password changed sucessfully');window.location='/changepassword';</script>")


@login_required(login_url='/')
@never_cache
def editproduct(request,id):
    data = Products.objects.get(id=id)
    request.session['id'] = id
    # sizes_available=data.size.split(",")
    return render(request,'admin/edit product.html',{"data":data})
def editproductbuttonsubmit(request):
    name = request.POST['textfield']
    description = request.POST['textarea']

    if 'image' in request.FILES:
        images = request.FILES['image']

        fs = FileSystemStorage()
        images = fs.save(images.name, images)
        images = fs.url(images)
        Products.objects.filter(id=request.session['id']).update(image=images)

    price = request.POST['textfield4']
    # stock = request.POST['textfield5']
    # color = request.POST['textfield6']
    #
    # size_list = request.POST.getlist('CheckboxGroup1')
    # size=",".join(size_list)

    Products.objects.filter(id=request.session['id']).update(categories = request.POST['category'],name=name,description=description,price=price)
    Products.objects.filter(id=request.session['id']).update(categories = request.POST['category'],name=name,description=description,price=price)

    return HttpResponse("<script>alert('Product updated sucessfully');window.location='/viewproducts';</script>")

def forgetchangepassword(request):
    return render(request,'admin/Forget Change Password.html')
def forgetchangepasswordbuttonsubmit(request):
    newpassword = request.POST['textfield']
    data=User.objects.get(email=request.session['email'])
    data.password=make_password(newpassword)
    data.save()
    return HttpResponse("<script>alert('Password reset');window.location='/';</script>")


def forgetpasswordotp(request):
    return render(request,'admin/forget password otp.html')
def forgetpasswordotpbuttonsubmit(request):
    otp = request.POST['textfield']
    if int(otp) == int(request.session['otp']):
        return HttpResponse("<script>alert('OTP verified');window.location='/forgetchangepassword';</script>")
    else:
        return HttpResponse("<script>alert('Invalid OTP');window.location='/forgetpasswordemailcheck';</script>")



def forgetpasswordemailcheck(request):
    return render(request,'admin/forget password_emailcheack.html')
def forgetpasswordemailcheckbuttonsubmit(request):
    email = request.POST['textfield']
    request.session['email']=email
    otp=random.randint(100000, 999999)
    request.session['otp']=otp
    # ✨ Python Email Codeimport smtplib

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # ✅ Gmail credentials (use App Password, not real password)
    sender_email = "projecteshop7@gmail.com"
    receiver_email = email  # change to actual recipient
    app_password = "xanv kagb utjs pfkl"  # App Password from Google
    pwd = str(otp)  # Example password to send

    # Setup SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Create the email
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "🔑 Your OTP for resetting password"

    # Plain text (backup)
    # text = f"""
    # Hello,

    # Your password for Smart Donation Website is: {pwd}

    # Please keep it safe and do not share it with anyone.
    # """

    # HTML (attractive)
    html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color:#2c7be5;">🔑 eshopping Website</h2>
            <p>Hello,</p>
            <p>Your otp for resetting password is:</p>
            <p style="padding:10px; background:#f4f4f4; 
                      border:1px solid #ddd; 
                      display:inline-block;
                      font-size:18px;
                      font-weight:bold;
                      color:#2c7be5;">
              {pwd}
            </p>
            <p>Please keep it safe and do not share it with anyone.</p>
            <hr>
            <small style="color:gray;">This is an automated email from eshopping System.</small>
          </body>
        </html>
        """

    # Attach both versions
    # msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Send email
    server.send_message(msg)
    print("✅ Email sent successfully!")

    # Close connection
    server.quit()
    return HttpResponse("<script>alert('Check email for OTP');window.location='/forgetpasswordotp';</script>")

@login_required(login_url='/')
@never_cache
def home(request):
    return render(request,'admin/home.html')


def log(request):
    return render(request,'admin/login.html')

def loginbuttonsubmit(request):
    username = request.POST['textfield']
    password = request.POST['textfield2']
    data = authenticate(request,username = username,password = password)
    if data:
        if data.is_superuser:
            login(request,data)
            return redirect('/home')
        elif data.groups.filter(name="worker").exists():
            login(request, data)
            if Workers.objects.filter(LOGIN_id=request.user.id,status="Approved").exists():
                request.session['wid']=Workers.objects.get(LOGIN_id=request.user.id).id
                return redirect('/homeworker')
            return HttpResponse("<script>alert('Unauthorized worker');window.location='/';</script>")

        elif data.groups.filter(name="user").exists():
            login(request, data)
            request.session['cid']=Customers.objects.get(LOGIN_id=request.user.id).id
            return redirect('/homeuser')
    return HttpResponse("<script>alert('Unauthorized User');window.location='/';</script>")

@login_required(login_url='/')
@never_cache
def orderhistory(request):
    data = Orders.objects.all()
    for i in data:
        i.ordereditem = Ordereditems.objects.filter(ORDER=i.id)

    return render(request,'admin/Orderhistory.html',{'data':data})

@login_required(login_url='/')
@never_cache
def rejectreason(request):
    return render(request,'admin/Reject reason.html')
def rejectreasonbuttonsubmit(request):
    reason = request.POST['textarea']
    return HttpResponse("Rejected")

@login_required(login_url='/')
@never_cache
def salerequesthistory(request):
    data = Products.objects.filter(status='Approved')
    total = 0
    pending = 0
    approved  = 0
    for i in data:
        total = total + int(i.price)
        if i.status == 'Approved':
            approved = approved + int(i.price)
        if i.status == 'Pending':
            pending = pending + int(i.price)
    return render(request,'admin/Salerequesthistory.html',{'data':data,'pending':pending,'approved':approved,'total':total})

@login_required(login_url='/')
@never_cache
def verifyworker(request):
    data = Workers.objects.filter(status="pending")
    return render(request,'admin/verify_worker.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewproducts(request):
    data = Products.objects.filter(status__in=["Approved",'Admin'])
    return render(request,'admin/view products.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewreview(request):
    data = Review.objects.all()
    return render(request,'admin/view review.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewuserfeedback(request):
    data = Feedback.objects.all()
    return render(request,'admin/view user feedback.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewusers(request):
    data = Customers.objects.all()
    return render(request,'admin/view users.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewworkers(request):
    data = Workers.objects.filter(status="Approved")
    return render(request,'admin/view worker.html',{'data':data})

@login_required(login_url='/')
@never_cache
def vieworder(request):
    data = Orders.objects.all()
    return render(request,'admin/Vieworder.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewordereditem(request,id):
    data = Ordereditems.objects.filter(ORDER=id)
    return render(request,'admin/Viewordereditem.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewpayment(request):
    data = Orders.objects.all()
    return render(request,'admin/Viewpayment.html',{'data':data})

@login_required(login_url='/')
@never_cache
def viewsalerequest(request):
    data = Products.objects.filter(status="pending")
    return render(request,'admin/Viewsalerequest.html',{'data':data})

@login_required(login_url='/')
@never_cache
def worker_approve(request,id):
    Workers.objects.filter(id=id).update(status="Approved")
    # ✨ Python Email Codeimport smtplib

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # ✅ Gmail credentials (use App Password, not real password)
    sender_email = "projecteshop7@gmail.com"
    receiver_email = Workers.objects.get(id=id).email # change to actual recipient
    app_password = "xanv kagb utjs pfkl"  # App Password from Google
    pwd = "Approved"  # Example password to send

    # Setup SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Create the email
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "🔑 Your eshopping Website Password"

    # Plain text (backup)
    # text = f"""
    # Hello,

    # Your password for Smart Donation Website is: {pwd}

    # Please keep it safe and do not share it with anyone.
    # """

    # HTML (attractive)
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color:#2c7be5;">🔑 eshopping Website</h2>
        <p>Hello,</p>
        <p>Your password is:</p>
        <p style="padding:10px; background:#f4f4f4; 
                  border:1px solid #ddd; 
                  display:inline-block;
                  font-size:18px;
                  font-weight:bold;
                  color:#2c7be5;">
          {pwd}
        </p>
        <p>Please keep it safe and do not share it with anyone.</p>
        <hr>
        <small style="color:gray;">This is an automated email from eshopping System.</small>
      </body>
    </html>
    """

    # Attach both versions
    # msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Send email
    server.send_message(msg)
    print("✅ Email sent successfully!")

    # Close connection
    server.quit()
    return redirect('/verifyworker')

@login_required(login_url='/')
@never_cache
def worker_reject(request,id):
    Workers.objects.filter(id=id).update(status="Rejected")
    # ✨ Python Email Codeimport smtplib

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # ✅ Gmail credentials (use App Password, not real password)
    sender_email = "projecteshop7@gmail.com"
    receiver_email = Workers.objects.get(id=id).email  # change to actual recipient
    app_password = "xanv kagb utjs pfkl"  # App Password from Google
    pwd = "Rejected"  # Example password to send

    # Setup SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Create the email
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "🔑 Your eshopping Website Password"

    # Plain text (backup)
    # text = f"""
    # Hello,

    # Your password for Smart Donation Website is: {pwd}

    # Please keep it safe and do not share it with anyone.
    # """

    # HTML (attractive)
    html = f"""
       <html>
         <body style="font-family: Arial, sans-serif; color: #333;">
           <h2 style="color:#2c7be5;">🔑 eshopping Website</h2>
           <p>Hello,</p>
           <p>Your password is:</p>
           <p style="padding:10px; background:#f4f4f4; 
                     border:1px solid #ddd; 
                     display:inline-block;
                     font-size:18px;
                     font-weight:bold;
                     color:#2c7be5;">
             {pwd}
           </p>
           <p>Please keep it safe and do not share it with anyone.</p>
           <hr>
           <small style="color:gray;">This is an automated email from eshopping System.</small>
         </body>
       </html>
       """

    # Attach both versions
    # msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Send email
    server.send_message(msg)
    print("✅ Email sent successfully!")

    # Close connection
    server.quit()
    return redirect('/verifyworker')

@login_required(login_url='/')
@never_cache
def removeproduct(request,id):
    Products.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Product deleted successfully');window.location='/viewproducts';</script>")

@login_required(login_url='/')
@never_cache
def salerequest_approve(request,id):
    return render(request, "admin/approve_product.html", {"id":id})
def salerequest_approve_post(request, id):
    name = request.POST['textfield']
    description = request.POST['textarea']
    price = request.POST['textfield4']
    # stock = request.POST['textfield5']
    # color = request.POST['textfield6']
    # size_list = request.POST.getlist('CheckboxGroup1')
    # size=",".join(size_list)
    obj = Products.objects.get(id=id)
    obj.name = name
    obj.description = description
    obj.price = price
    # obj.stock = stock
    # obj.color = color
    # obj.size = size
    obj.status = "Approved"
    obj.save()
    price = obj.requested_price
    try:


        balance = Balance.objects.filter(WORKER=obj.WORKER_id)
        balance.update(amount = int(balance[0].amount) + int(price) )
    except:
        obj = Balance()
        obj.WORKER_id = 1
        obj.amount = price
        obj.save()



    return HttpResponse("<script>alert('Product Approved');window.location='/viewproducts';</script>")

@login_required(login_url='/')
@never_cache
def salerequest_reject(request,id):
    Products.objects.filter(id=id).update(status="Rejected")
    return HttpResponse("<script>alert('Sale request rejected');window.location='/viewsalerequest';</script>")

@login_required(login_url='/')
@never_cache
def updatedeliverystatus(request,id):
    Orders.objects.filter(id=id).update(status="delivered")
    return HttpResponse("<script>alert('Delivered');window.location='/vieworder';</script>")

@login_required(login_url='/')
@never_cache
def productbycolour(request,id):
    request.session['pid'] = id
    return render(request,"admin/productsbycolour.html")
def productbycolour_buttonclick(request):
    image = request.FILES['fileField']

    fs = FileSystemStorage()
    image = fs.save(image.name, image)
    image = fs.url(image)

    color = request.POST['textfield']

    obj = Productsbycolor()
    obj.PRODUCT_id = request.session['pid']
    obj.image = image
    obj.color = color
    obj.save()
    return HttpResponse("<script>alert('Product color image added successfully');window.location='/viewbycolour/" + str(request.session['pid']) + "';</script>")

@login_required(login_url='/')
@never_cache
def viewbycolour(request,id):
    data = Productsbycolor.objects.filter(PRODUCT=id)
    return render(request,"admin/viewbycolour.html",{'data':data})

@login_required(login_url='/')
@never_cache
def deleteproductimage(request,id):
    product = Productsbycolor.objects.filter(id=id).values('PRODUCT_id').first()
    pid = product['PRODUCT_id'] if product else 0
    Productsbycolor.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Product image deleted');window.location='/viewbycolour/" + str(pid) + "';</script>")

@login_required(login_url='/')
@never_cache
def shippingstatus(request,id):
    request.session['ooid']=id
    data = Deliverystatus.objects.filter(ORDER=id)
    return render(request,"admin/shippingstatus.html",{'data':data})
def shippingstatus_buttonclick(request):
    status = request.POST['radio']
    description = request.POST['textfield']
    Orders.objects.filter(id=request.session['ooid']).update(status=status)

    obj = Deliverystatus()
    obj.ORDER_id = request.session['ooid']
    obj.status = status
    obj.description = description
    obj.date = datetime.datetime.now().date()
    obj.save()
    return HttpResponse("<script>alert('Shipping status updated successfully');window.location='/vieworder';</script>")

@login_required(login_url='/')
@never_cache
def viewdeliverystatus(request):
    return render(request,"admin/uviewdeliverystatus.html")

def addstock(request,id):
    request.session['pid'] = id
    return render(request, "admin/addstock.html")
def addstock_buttonclick(request):
    size = request.POST['radio']
    stock = request.POST['textfield']
    color = request.POST['textfield2']
    image = request.FILES['fileField']
    fs = FileSystemStorage()
    image = fs.save(image.name, image)
    image = fs.url(image)
    if Stock.objects.filter(size = size,color = color,PRODUCT_id = request.session['pid']).exists():
        cqty = int(Stock.objects.get(size = size,color = color,PRODUCT_id = request.session['pid']).stock)
        Stock.objects.filter(size=size, color=color,PRODUCT_id = request.session['pid']).update(stock = int(cqty) + int(stock))

        return HttpResponse("<script>alert('Stock updated successfully');window.location='/viewstock/" + str(
            request.session['pid']) + "';</script>")

    obj = Stock()
    obj.size = size
    obj.stock = stock
    obj.color = color
    obj.PRODUCT_id = request.session['pid']
    obj.image = image
    obj.save()
    return HttpResponse("<script>alert('Stock added successfully');window.location='/viewstock/" + str(request.session['pid']) + "';</script>")

def viewstock(request,id):
    data = Stock.objects.filter(PRODUCT=id)
    return render(request,"admin/view stock.html",{'data':data})

def editstock(request,id):
    request.session['pid'] = id
    stock = Stock.objects.get(id=id)
    return render(request,"admin/editstock.html", {'stock': stock})
def editstock_buttonclick(request):
    size = request.POST['radio']
    stock = request.POST['textfield']
    color = request.POST['textfield2']
    obj = Stock.objects.get(id=request.session['pid'])
    product_id = obj.PRODUCT_id
    obj.size = size
    obj.stock = stock
    obj.color = color
    
    # Only update image if a new file is uploaded
    if 'fileField' in request.FILES and request.FILES['fileField']:
        image = request.FILES['fileField']
        fs = FileSystemStorage()
        image = fs.save(image.name, image)
        image = fs.url(image)
        obj.image = image
    
    obj.save()
    return HttpResponse("<script>alert('Stock updated successfully');window.location='/viewstock/" + str(product_id) + "';</script>")

def deletestock(request,id):
    stock_item = Stock.objects.get(id=id)
    product_id = stock_item.PRODUCT_id
    Stock.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Stock deleted successfully');window.location='/viewstock/" + str(product_id) + "';</script>")
# ===============================================================================================
@login_required(login_url='/')
@never_cache
def addproductworker(request):
    return render(request,"worker/Add product worker.html")
def addproductworker_buttonclick(request):
    # name = request.POST['textfield']
    description = request.POST['textfield2']
    price = request.POST['textfield3']
    # color = request.POST['textfield4']
    image = request.FILES['fileField']

    fs = FileSystemStorage()
    image = fs.save(image.name, image)
    image = fs.url(image)

    # size = request.POST.getlist('CheckboxGroup1')
    obj = Products()
    obj.categories = request.POST['category']
    obj.description = description
    obj.requested_price = price
    # obj.color = color
    obj.image = image
    # obj.size = size
    obj.status="pending"
    obj.WORKER_id=request.session['wid']
    obj.save()
    return HttpResponse("<script>alert('Product added successfully. Waiting for admin approval');window.location='/viewproductworker';</script>")

@login_required(login_url='/')
@never_cache
def changepasswordworker(request):
    return render(request,"worker/Change password worker.html")
def changepasswordworker_buttonclick(request):
    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    if currentpassword == newpassword:
        return HttpResponse("<script>alert('This password is already exist,Enter new password');window.location='/homeworker';</script>")
    if newpassword != confirmpassword:
        return HttpResponse("<script>alert('Passwords do not match');window.location='/homeuser';</script>")
    User.objects.filter(id=request.user.id).update(password=make_password(confirmpassword))

    return HttpResponse("<script>alert('Password changed successfully');window.location='/homeworker';</script>")

@login_required(login_url='/')
@never_cache
def editproductworker(request, id):
    data=Products.objects.get(id=id)
    return render(request,"worker/Edit product worker.html", {"data":data})

def editproductworker_buttonclick(request, id):
    description = request.POST['textfield']
    price = request.POST['textfield2']
    if 'fileField' in request.FILES:
        image = request.FILES['fileField']
        fs = FileSystemStorage()
        image = fs.save(image.name, image)
        image = fs.url(image)
        Products.objects.filter(id = id).update(description = description,requested_price = price,image = image)
    Products.objects.filter(id = id).update(description = description,requested_price = price)

    return HttpResponse("<script>alert('Product updated successfully');window.location='/viewproductworker';</script>")

@login_required(login_url='/')
@never_cache
def homeworker(request):
    return render(request,"worker/Home worker.html")


def register(request):
    return render(request,"worker/Register.html")
def register_buttonclick(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    place = request.POST['textfield4']
    post = request.POST['textfield5']
    pin = request.POST['textfield6']
    proof = request.FILES['fileField']

    fs = FileSystemStorage()
    proof = fs.save(proof.name, proof)
    proof = fs.url(proof)

    password = request.POST['textfield7']
    confirmpassword = request.POST['textfield8']
    if password == confirmpassword:

        obj1 = User()
        obj1.username = email
        obj1.password = make_password(password)
        obj1.save()

        obj1.groups.add(Group.objects.get(name="worker"))

        obj = Workers()
        obj.name = name
        obj.email = email
        obj.phone = phone
        obj.place = place
        obj.post = post
        obj.pin = pin
        obj.proof = proof
        obj.LOGIN = obj1
        obj.status = "pending"
        obj.reason = "pending"
        # obj.password = password
        # obj.confirmpassword = confirmpassword
        obj.save()

        obj2 = Balance()
        obj2.amount = 0
        obj2.WORKER_id = obj.id
        obj2.save()

        return HttpResponse("<script>alert('Registration successful! Please wait for admin approval');window.location='/';</script>")
    return HttpResponse("<script>alert('Password mismatch');window.location='/register';</script>")

@login_required(login_url='/')
@never_cache
def sendsalerequest(request, id):
    return render(request,"worker/Send sale request.html", {"id":id})
def sendsalerequest_buttonclick(request, id):
    qty = request.POST['textfield']
    obj = Salerequests()
    obj.qty = qty
    obj.PRODUCT_id=id
    obj.date=datetime.datetime.now().date()
    obj.status = "pending"
    obj.paymentstatus = "pending"
    obj.paymentdate = "pending"
    obj.save()

    return HttpResponse("<script>alert('Sale request submitted successfully');window.location='/viewproductworker';</script>")

@login_required(login_url='/')
@never_cache
def viewpaymenthistoryworker(request):
    data = Products.objects.filter(WORKER=request.session['wid'],status="Approved")
    return render(request,"worker/View payment history worker.html",{'data':data})

@login_required(login_url='/')
@never_cache
def viewproductworker(request):
    data = Products.objects.filter(WORKER=request.session['wid'])
    return render(request,"worker/View product worker.html",{'data':data})

@login_required(login_url='/')
@never_cache
def viewprofileandupdate(request):
    data = Workers.objects.get(id=request.session['wid'])
    return render(request,"worker/View profile and update.html",{'data':data})
def viewprofileandupdate_buttonclick(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    place = request.POST['textfield4']
    post = request.POST['textfield5']
    pin = request.POST['textfield6']
    if 'fileField' in request.FILES:
        proof = request.FILES['fileField']

        fs = FileSystemStorage()
        proof = fs.save(proof.name, proof)
        proof = fs.url(proof)
        Workers.objects.filter(id=request.session['wid']).update(name=name, email=email, phone=phone, place=place,
                                                                 post=post, pin=pin, proof=proof)

    Workers.objects.filter(id=request.session['wid']).update(name=name,email=email,phone=phone,place=place,post=post,pin=pin)
    return HttpResponse("<script>alert('Profile updated successfully');window.location='/viewprofileandupdate';</script>")

@login_required(login_url='/')
@never_cache
def viewrequesthistoryworker(request):
    data = Salerequests.objects.filter()
    return render(request,"worker/View request history worker.html",{'data':data})

@login_required(login_url='/')
@never_cache
def viewreviewworker(request):
    data = Review.objects.filter(PRODUCT__WORKER=request.session['wid'])
    return render(request,"worker/View review worker.html",{'data':data})

@login_required(login_url='/')
@never_cache
def viewsalerequestworker(request):
    data = Salerequests.objects.filter(PRODUCT__WORKER=request.session['wid'])
    return render(request,"worker/View sale request  worker.html",{'data':data})

@login_required(login_url='/')
@never_cache
def removeproductworker(request,id):
    Products.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Product deleted successfully');window.location='/viewproductworker';</script>")

@login_required(login_url='/')
@never_cache
def mybalance(request):
    data = Balance.objects.filter(WORKER=request.session['wid'])
    if data.exists():
        if int(data[0].amount) > 0:
            return render(request,"worker/mybalance.html",{'data':data})
        return render(request, "worker/mybalance.html")
    else:
        return render(request, "worker/mybalance.html")

@login_required(login_url='/')
@never_cache
def mybalance_buttonclick(request):
    return redirect('/withdraw')

@login_required(login_url='/')
@never_cache
def withdraw(request):
    data = Balance.objects.filter()[0].amount
    return render(request,"worker/withdraw.html",{'data':data})
def withdraw_buttonclick(request):
    request.session['a'] = request.POST['textfield']
    return redirect('/default')

@login_required(login_url='/')
@never_cache
def default(request):
    import razorpay

    razorpay_api_key = "your-razorpay-key-here"
    razorpay_secret_key = "your-razorpay-secret-here"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    amount = int(request.session['a']) * 100
    # amount = float(amount)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    return render(request, 'worker/pay.html',{'razorpay_api_key': razorpay_api_key,
                                            'amount': order_data['amount'],
                                            'currency': order_data['currency'],
                                            'order_id': order['id']})
@login_required(login_url='/')
@never_cache
def paymentsuccess(request):
    total = int(Balance.objects.filter()[0].amount) - int(request.session['a'])
    Balance.objects.filter().update(amount = total)
    return HttpResponse("<script>alert('Withdraw sucessfull');window.location='/mybalance';</script>")


#    =============================================================================

@login_required(login_url='/')
@never_cache
def addtocart(request,id):
    product = Products.objects.get(id=id)
    request.session['pid'] = id
    
    # Get all stock items directly from Stock model for this product
    stock_items = Stock.objects.filter(PRODUCT=product)
    print(stock_items)
    sizes = product.get_sizes()
    colors = product.get_colors()
    
    # Organize stock data by color with size and stock details
    stock_by_color = {}
    for item in stock_items:
        if item.color not in stock_by_color:
            stock_by_color[item.color] = {
                'color': item.color,
                'image': item.image,
                'sizes': []
            }
        stock_by_color[item.color]['sizes'].append({
            'size': item.size,
            'stock': item.get_stock_quantity(),
            'in_stock': item.in_stock(),
            'id': item.id
        })
    
    return render(request,"user/Add to cart.html",{
        'data': product, 
        'stock_items': stock_items,
        'stock_by_color': list(stock_by_color.values()),
        'sizes': sizes,
        'colors': colors
    })
def addtocart_buttonclick(request):
    size = request.POST['textfield4']
    color = request.POST['textfield5']
    qty = request.POST['textfield7']
    customization = request.POST['customization']
    obj = Carts()
    obj.CUSTOMER_id = request.session['cid']
    obj.PRODUCT_id = request.session['pid']
    obj.size = size
    obj.customization = customization
    obj.selectedcolor = color
    obj.qty = qty
    obj.save()
    return HttpResponse("<script>alert('Item added to cart successfully');window.location='/viewcart';</script>")

@login_required(login_url='/')
@never_cache
def changepassworduser(request):
    return render(request,"user/Change password user.html")
def changepassworduser_buttonclick(request):
    currentpassword = request.POST['textfield']
    newpassword = request.POST['textfield2']
    confirmpassword = request.POST['textfield3']
    if currentpassword == newpassword:
        return HttpResponse("<script>alert('This password is already exist,Enter a new password');window.location='/homeuser';</script>")
    if newpassword != confirmpassword:
        return HttpResponse("<script>alert('Passwords do not match');window.location='/homeuser';</script>")

    User.objects.filter(id=request.user.id).update(password=make_password(confirmpassword))
    return HttpResponse("<script>alert('Password changed successfully');window.location='/homeuser';</script>")

@login_required(login_url='/')
@never_cache
def homeuser(request):
    data = Products.objects.filter(status__in=["Approved","Admin"])[0:8]
    return render(request,"user/Home user.html",{'data':data})


def registeruser(request):
    return render(request,"user/Register user.html")
def registeruser_buttonclick(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    password = request.POST['textfield4']
    confirmpassword = request.POST['textfield5']
    obj1 = User()
    obj1.username = email
    obj1.password = make_password(password)
    obj1.save()

    obj1.groups.add(Group.objects.get(name="user"))

    obj = Customers()
    obj.name = name
    obj.email = email
    obj.phone = phone
    obj.LOGIN = obj1
    obj.save()
    return HttpResponse("<script>alert('Registration successful! Please login');window.location='/';</script>")

@login_required(login_url='/')
@never_cache
def sendfeedbackuser(request):
    return render(request,"user/Send feedback user.html")
def sendfeedbackuser_buttonclick(request):
    feedback = request.POST['textarea']
    obj = Feedback()
    obj.CUSTOMER_id = request.session['cid']
    obj.feedback = feedback
    obj.date = datetime.datetime.now().date()
    obj.save()
    return HttpResponse("<script>alert('Thank you for your feedback!');window.location='/homeuser';</script>")

@login_required(login_url='/')
@never_cache
def sendreviewuser(request,id):
    request.session['id'] = id
    return render(request,"user/Send review user.html")
def sendreviewuser_buttonclick(request):
    review = request.POST['textfield2']
    rating = request.POST['textfield']
    obj = Review()
    obj.CUSTOMER_id = request.session['cid']
    obj.PRODUCT_id = request.session['id']
    obj.comment = review
    obj.rating = rating
    obj.date = datetime.datetime.now().date()
    obj.save()
    return HttpResponse("<script>alert('Thank you for your review!');window.location='/homeuser';</script>")

@login_required(login_url='/')
@never_cache
def viewandeditprofileuser(request):
    data = Customers.objects.get(id=request.session['cid'])
    return render(request,"user/View and edit profile user.html",{'data':data})
def viewandeditprofileuser_buttonclick(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    phone = request.POST['textfield3']
    obj = Customers.objects.filter(id=request.session['cid']).update(name = name,email = email,phone = phone)

    return HttpResponse("<script>alert('Profile updated successfully');window.location='/viewandeditprofileuser';</script>")

@login_required(login_url='/')
@never_cache
def viewcart(request):
    data = Carts.objects.filter(CUSTOMER_id=request.session['cid'])
    total = 0
    cart_items = []
    
    for cart_item in data:
        # Check stock for this specific size and color combination
        stock_items = Stock.objects.filter(
            PRODUCT=cart_item.PRODUCT,
            size=cart_item.size,
            color=cart_item.selectedcolor
        )
        total_price = int(cart_item.PRODUCT.price) * int(cart_item.qty)

        item_data = {
            'cart': cart_item,
            'total_price': total_price,
            'in_stock': False,
            'available_qty': 0,
            'stock_status': 'Out of Stock'
        }
        
        if stock_items.exists():
            stock_item = stock_items.first()
            available_qty = stock_item.get_stock_quantity()
            
            if available_qty > 0:
                item_data['in_stock'] = True
                item_data['available_qty'] = available_qty
                
                if available_qty > 5:
                    item_data['stock_status'] = f'In Stock ({available_qty})'
                else:
                    item_data['stock_status'] = f'Limited Stock ({available_qty})'
                
                # Only add to total if item is in stock
                total += int(cart_item.qty) * int(cart_item.PRODUCT.price)
            else:
                item_data['stock_status'] = 'Out of Stock'

        cart_items.append(item_data)
    
    request.session['total'] = total
    return render(request,"user/View cart.html",{'cart_items': cart_items, 'total': total})

@login_required(login_url='/')
@never_cache
def viewordersanditemsuser(request):
    data = Ordereditems.objects.all()
    return render(request,"user/View orders and items user.html",{'data':data})

@login_required(login_url='/')
@never_cache
def viewproductuser(request,id):
    data = Products.objects.filter(categories=id,status__in=["Approved",'Admin'])
    return render(request,"user/View Product user.html",{'data':data})

@login_required(login_url='/')
@never_cache
def viewreviewuser(request,id):
    data = Review.objects.filter(PRODUCT=id)
    return render(request,"user/View review user.html",{'data':data})

@login_required(login_url='/')
@never_cache
def removecart(request,id):
    Carts.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Item removed from cart');window.location='/viewcart';</script>")

@login_required(login_url='/')
@never_cache
def makepayment(request,id):
    request.session['cartid'] = id
    return render(request,"user/make payment.html")
def makepayment_buttonclick(request):
    method = request.POST['RadioGroup1']
    address = request.POST['textfield4']
    latitude = request.POST['textfield']
    longitude = request.POST['textfield2']
    request.session['latitude'] = latitude
    request.session['longitude'] = longitude
    if method == "online":
        request.session['a'] = int(Carts.objects.get(id=request.session['cartid']).qty) * int(Carts.objects.get(id=request.session['cartid']).PRODUCT.price)
        return  redirect('/payment')

    obj = Orders()
    obj.CUSTOMER_id=request.session['cid']
    obj.date = datetime.datetime.now().date()
    obj.status = "pending"
    obj.amount = int(Carts.objects.get(id=request.session['cartid']).qty) * int(Carts.objects.get(id=request.session['cartid']).PRODUCT.price)
    obj.paymentstatus = method
    obj.paymentdate = datetime.datetime.now().date()
    obj.latitude = latitude
    obj.longitude = longitude
    obj.save()

    cartdata = Carts.objects.get(id=request.session['cartid'])

    obj1 = Ordereditems()
    obj1.ORDER_id = obj.id
    obj1.PRODUCT_id=cartdata.PRODUCT_id
    obj1.qty = cartdata.qty
    obj1.selectcolor = cartdata.selectedcolor
    obj1.size = cartdata.size
    print(cartdata.customization,'####################')
    obj1.customization = cartdata.customization
    obj1.save()
    
    # Decrease stock for the ordered size and color
    try:
        stock_item = Stock.objects.get(
            PRODUCT_id=cartdata.PRODUCT_id,
            size=cartdata.size,
            color=cartdata.selectedcolor
        )
        current_stock = stock_item.get_stock_quantity()
        new_stock = max(0, current_stock - int(cartdata.qty))
        stock_item.stock = str(new_stock)
        stock_item.save()
    except Stock.DoesNotExist:
        pass

    cartdata.delete()

    return HttpResponse("<script>alert('Order placed successfully!');window.location='/homeuser';</script>")

@login_required(login_url='/')
@never_cache
def payment(request):
    import razorpay

    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    amount = int(request.session['a']) * 100
    # amount = float(amount)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    return render(request, 'user/pay.html', {'razorpay_api_key': razorpay_api_key,
                                               'amount': order_data['amount'],
                                               'currency': order_data['currency'],
                                               'order_id': order['id']})

@login_required(login_url='/')
@never_cache
def placeorder(request):
    return render(request,"user/placeorder.html")

@login_required(login_url='/')
@never_cache
def orderpaymentsuccess(request):
    obj = Orders()
    obj.CUSTOMER_id = request.session['cid']
    obj.date = datetime.datetime.now().date()
    obj.status = "pending"
    obj.amount = int(Carts.objects.get(id=request.session['cartid']).qty) * int(
        Carts.objects.get(id=request.session['cartid']).PRODUCT.price)
    obj.paymentstatus = "online"
    obj.paymentdate = datetime.datetime.now().date()
    obj.latitude = request.session['latitude']
    obj.longitude = request.session['longitude']
    obj.save()

    cartdata = Carts.objects.get(id=request.session['cartid'])

    obj1 = Ordereditems()
    obj1.ORDER_id = obj.id
    obj1.PRODUCT_id = cartdata.PRODUCT_id
    obj1.qty = cartdata.qty
    obj1.selectcolor = cartdata.selectedcolor
    obj1.size = cartdata.size
    obj1.customization = cartdata.customization
    obj1.save()
    
    # Decrease stock for the ordered size and color
    try:
        stock_item = Stock.objects.get(
            PRODUCT_id=cartdata.PRODUCT_id,
            size=cartdata.size,
            color=cartdata.selectedcolor
        )
        current_stock = stock_item.get_stock_quantity()
        new_stock = max(0, current_stock - int(cartdata.qty))
        stock_item.stock = str(new_stock)
        stock_item.save()
    except Stock.DoesNotExist:
        pass

    cartdata.delete()

    return HttpResponse("<script>alert('Payment successful! Order placed');window.location='/homeuser';</script>")

@login_required(login_url='/')
@never_cache
def allpayment(request):
    return render(request,"user/allpayment.html")
def allpayment_buttonclick(request):
    method = request.POST['RadioGroup1']
    latitude = request.POST['textfield']
    longitude = request.POST['textfield2']
    request.session['latitude'] = latitude
    request.session['longitude'] = longitude
    if method == "online":
        request.session['a'] = request.session['total']
        return  redirect('/payment')
    obj = Orders()
    obj.CUSTOMER_id = request.session['cid']
    obj.date = datetime.datetime.now().date()
    obj.status = "pending"
    obj.amount = request.session['total']
    obj.paymentstatus = method
    obj.paymentdate = datetime.datetime.now().date()
    obj.latitude = latitude
    obj.longitude = longitude
    obj.save()
    cartdata = Carts.objects.filter(CUSTOMER=request.session['cid'])
    for i in cartdata:
        obj1 = Ordereditems()
        obj1.ORDER_id = obj.id
        obj1.PRODUCT_id=i.PRODUCT_id
        obj1.qty = i.qty
        obj1.selectcolor = i.selectedcolor
        obj1.size = i.size
        obj1.customization = i.customization
        obj1.save()
        
        # Decrease stock for each ordered item
        try:
            stock_item = Stock.objects.get(
                PRODUCT_id=i.PRODUCT_id,
                size=i.size,
                color=i.selectedcolor
            )
            current_stock = stock_item.get_stock_quantity()
            new_stock = max(0, current_stock - int(i.qty))
            stock_item.stock = str(new_stock)
            stock_item.save()
        except Stock.DoesNotExist:
            pass

    cartdata.delete()

    return HttpResponse("<script>alert('Order placed successfully!');window.location='/homeuser';</script>")

@login_required(login_url='/')
@never_cache
def payall(request):
    import razorpay

    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

    amount = int(request.session['a']) * 100
    # amount = float(amount)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
    }

    return render(request, 'user/payall.html', {'razorpay_api_key': razorpay_api_key,
                                               'amount': order_data['amount'],
                                               'currency': order_data['currency'],
                                               'order_id': order['id']})


def logouts(request):
    logout(request)
    return HttpResponse("<script>alert('Logouted');window.location='/';</script>")

@login_required(login_url='/')
@never_cache
def uviewdeliverystatus(request,id):
    data = Deliverystatus.objects.filter(ORDER=id)
    return render(request,"user/uviewdeliverystatus.html",{'data':data})


@login_required(login_url='/')
@never_cache
# show all product categories to the user, pulling names from the database
# and include a few sample products per category for the preview cards
# (template will iterate over this data)
def categoriesuser(request):
    # grab the distinct category names for approved products
    cats = Products.objects.filter(status__in=['Approved','Admin']).values_list('categories', flat=True).distinct()
    # build a structure that contains a small set of products per category
    categories_data = []
    for cat in cats:
        prods = Products.objects.filter(categories=cat, status__in=['Approved','Admin'])[:4]
        categories_data.append({
            'name': cat,
            'products': prods,
        })
    # also pass the flat list of names for simple lists
    return render(request, "user/categoriesuser.html", {
        'categories_data': categories_data,
        'categories': list(cats),
    })


