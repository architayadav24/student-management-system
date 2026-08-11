from django.shortcuts import render, redirect
# from django.contrib.auth import auth
from django.contrib.auth import authenticate, login, logout , update_session_auth_hash
from django.contrib.auth.models import User,auth
from .models import student
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import datetime

# Create your views here.

def index(request):
    return render(request,"index.html")

def about(request):
    return render (request,"about.html")  

def contact(request):
    return render(request,"contact.html")

def login_view(request):
    error=""
    if request.method=="POST":
        u=request.POST.get('username')
        p=request.POST.get('password')
        #student login:
        try:
            stu=student.objects.get(username=u,password=p)
            request.session['student_id']=stu.id
            return redirect('student_home')

        except student.DoesNotExist:
            pass

        #admin login-

        admin=auth.authenticate(username=u,password=p)
        if admin is not None and admin.is_staff:
            auth.login(request,admin)
            return redirect('AdminHome')
    return render(request,"login.html")

       

@login_required(login_url='login')
def AdminHome(request):
    return render(request,"AdminHome.html")

@login_required(login_url='login')
def add_students(request):
    error=""
    if request.method == "POST":
        n=request.POST['name']
        e=request.POST['email']
        u=request.POST['username']
        p=request.POST['password']
        c=request.POST['college']
        add=request.POST['address']
        jd=request.POST['join_date']
        tf=request.POST['total_fee']
        pf=request.POST['paid_fee']
        df=request.POST['due_fee']
        ph=request.POST['phone']
        tech=request.POST['technology']
        img=request.FILES['image']  
        try:
            student.objects.create(name=n,
            email=e,
            username=u,
            password=p,
            college=c,
            address=add,
            join_date=jd,
            total_fee=tf,
            paid_fee=pf,
            due_fee=df,
            phone=ph,
            technology=tech,
            image=img)
            error="no"
        except:
            error="yes"    
    return render(request,"add_students.html")

@login_required(login_url='login')
def view_students(request):
    data=student.objects.all()
    d={'data':data}
    return render(request,"view_students.html",d)

@login_required(login_url='login')   
def edit_student(request,id):
    data=student.objects.get(id=id)
    error=""
    if request.method == "POST":
        n=request.POST['fname']
        e=request.POST['email']
        c=request.POST['college']
        add=request.POST['address']
        jd=request.POST['jdate']
        tf=request.POST['tfee']
        pf=request.POST['pfee']
        df=request.POST['dfee']
        ph=request.POST['phone']
        tech=request.POST['technology']
        #update data
        data.name=n
        data.email=e
        data.college=c
        data.address=add
        data.join_date=jd
        data.total_fee=tf
        data.paid_fee=pf
        data.due_fee=df
        data.phone=ph
        data.technology=tech
        try:
            data.save()
            error="no"
        except exception as e:
            print(e)
            error="yes"
    d={"data":data,'error':error}    
    return render(request,"edit_student.html",d)

@login_required(login_url='login')
def del_student(request,id):
    data=student.objects.get(id=id)
    data.delete()
    return redirect('view_students')
    
@login_required(login_url='login')
def feedback(request):
    if request.method == "POST":
        n=request.POST['name']
        e=request.POST['email']
        f=request.POST['feedback']

        Feedback.objects.create(name=n,email=e,feedback=f)
    return render(request,'feedback.html')

@login_required(login_url='login')
def view_feedback(request): 
    data=Feedback.objects.all()
    d={'data':data}
    return render(request,'view_feedback.html',d)   


@login_required(login_url='login')
def search_stu(request):
    return render(request,'search_student.html') 


@login_required(login_url='login')
def search_student(request):
    if request.method == "POST":
        n = request.POST['sname']
        data = student.objects.filter(name__icontains=n)
        d={'data':data}
        return render(request,'view_students.html',d)
    return render(request,'search_student.html')    

@login_required(login_url='login')    
def admin_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def change_password(request):
    return render(request,'change_password.html')

@login_required(login_url='login')
def update_password(request):

    if request.method == "POST":

        old_password = request.POST.get('old_pass')
        new_password = request.POST.get('new_pass')
        confirm_password = request.POST.get('conf_pass')

        user = request.user

        # Check old password
        if not user.check_password(old_password):
            return render(
                request,
                'change_password.html',
                {'error': 'Current password is incorrect.'}
            )

        # Check new password and confirm password
        if new_password != confirm_password:
            return render(
                request,
                'change_password.html',
                {'error': 'New passwords do not match.'}
            )

        # Password length
        if len(new_password) < 6:
            return render(
                request,
                'change_password.html',
                {'error': 'Password must contain at least 6 characters.'}
            )

        # Update password
        user.set_password(new_password)
        user.save()

        # Keep current session active
        update_session_auth_hash(request, user)

        return render(
            request,
            'change_password.html',
            {'success': 'Password updated successfully!'}
        )

    return redirect('change_password')  

def student_home(request):
    if 'student_id' not in request.session:
        return redirect('login')
    sid=request.session['student_id']
    stu=student.objects.get(id=sid)    
    return render(request,'student_home.html',{'student':stu})  

def edit_profile(request):
    if 'student_id' not in request.session:
        return redirect('login')
    sid=request.session['student_id']
    stu=student.objects.get(id=sid)
    if request.method=="POST":
        stu.name=request.POST['fname']
        stu.email=request.POST['email']
        stu.address=request.POST['address']
        stu.phone=request.POST['phone']

        if request.FILES.get('image'):
            stu.image=request.FILES['image']
        stu.save()
    d={"student":stu}    
    return render(request,'edit_profile.html',d) 

def fee_detail(request):
    sid=request.session.get('student_id')
    if sid is None:
        return redirect('login')
    stu=student.objects.get(id=sid)    
    return render(request,"fee.html",{"student":stu})   

def payment_receipt(request):
    sid=request.session.get('student_id')
    if sid is None:
        return redirect('login')
    stu=student.objects.get(id=sid)
    # Generate PDF receipt
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payment_receipt_{stu.id}.pdf"'   
    pdf=canvas.Canvas(response)


    pdf.setTitle("Payment Receipt")
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(140, 800, "student record system")
    pdf.setFont("Helvetica", 22) 
    pdf.drawString(180,780,"STUDENT FEE RECIEPT")
    pdf.line(40,765,550,765)

    receipt_no = f"SRM: {stu.id}".zfill(4)#SRM0007
    pdf.setFont("Helvetica", 13)
    pdf.drawString(50, 740, f"Receipt No: {receipt_no}")
    pdf.drawString(400, 740, f"Date: {datetime.date.today().strftime('%d-%m-%Y')}")
    pdf.line(40,725,550,725)

    #student details
    pdf.setFont("Helvetica", 16)
    pdf.drawString(50, 700, "student details:")
    pdf.setFont("Helvetica", 14)

#fee details
    pdf.drawString(50, 670, f"Name: {stu.name}")
    pdf.drawString(50, 640, f"Email: {stu.email}")
    pdf.drawString(50, 610, f"Technology: {stu.technology}")
    pdf.drawString(50, 580, f"Phone: {stu.phone}")
    pdf.drawString(50, 550, f"College: {stu.college}")
    
    pdf.line(50,545,550,545)
    #
    pdf.setFont("Helvetica", 16)
    pdf.drawString(50, 430, "Fee Details")
    pdf.setFont("Helvetica", 14)
    pdf.drawString(50, 400, f"Total Fee: {stu.total_fee}")
    pdf.drawString(50, 370, f"Paid Fee: {stu.paid_fee}")
    pdf.drawString(50, 340, f"Due Fee: {stu.due_fee}")

    pdf.line(40, 330, 550, 330)

    #footer
   
    pdf.drawString(50, 100, "This is a computer-generated receipt and does not require a signature.")
    # pdf.drawString(50, 80, "For any queries, please contact us at support@university.edu")
    pdf.line(40, 70, 550, 70)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 50, "authorized signature")
    pdf.save()    
    return response

def user_change_pass(request):
    return render(request,'user_change_password.html')

def user_update_pass(request):
        sid=request.session.get('student_id')
        if sid is None:
            return redirect('login')
        stu=student.objects.get(id=sid)
        error=""  

        if request.method=="POST":
            op=request.POST['old_pass']
            np=request.POST['new_pass']   
            if stu.password!=op:
                error="Current password is incorrect"
            else:
                stu.password=np
                stu.save()
                error="done"
        return render(request,'user_change_password.html',{'error':error})       
def forgot_password(request):
    return render(request, "reset_password.html")

def reset_password(request):
    error = ""
    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password != confirm_password:
            error = "Passwords do not match"
        else:
            # Here you would typically update the user's password
            # For example: user.password = new_password; user.save()
            error = "Password reset successfully"
    return render(request, "reset_password.html", {"error": error})