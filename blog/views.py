from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import *


def index(request):
	posted_blogs = Blogtbl.objects.filter(status='Accepted').order_by("-created_date")
	all_blogs = Paginator(posted_blogs,6)
	page = request.GET.get('page')
	try:
		blogs = all_blogs.page(page)
	except PageNotAnInteger:
		blogs = all_blogs.page(1)
	except EmptyPage:
		blogs = all_blogs.page(1)
	
	context = {
		"blogs":blogs
	}
	return render(request,'index.html',context)


def about_us(request):
	return render(request,'about_us.html')


def contact_us(request):
	error = ""
	if request.method == 'POST':
		email = request.POST['email']
		uname = request.POST['uname']
		message = request.POST['msg']

		try:
			Contacttbl.objects.create(sender_name=uname,sender_email=email,sender_message=message)
			error = "no"
		except:
			error = "yes"
	
	context = {
		"error":error
	}
	return render(request,'contact_us.html',context)


def user_login(request):
	if request.user.is_authenticated:
		return redirect('user_home')
	error = ""
	if request.method == 'POST':
		uname = request.POST['email']
		pass1 = request.POST['pwd']

		user = authenticate(request,username=uname,password=pass1)

		if user:
			try:
				login(request,user)
				error = "no"
			except:
				error = "yes"	
	context = {
		"error":error
	}
	return render(request,'user_login.html',context)


def user_signup(request):
	error = ""
	if request.method == 'POST':
		fname = request.POST['firstname']
		lname = request.POST['lastname']
		pass1 = request.POST['pwd']
		uname = request.POST['email']
		mbl = request.POST['contact']
		gend = request.POST['gender']
		pic = request.FILES['image']

		if User.objects.filter(username=uname):
			error = "exists"
		else:
			try:
				user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=pass1)
				Usertbl.objects.create(user=user,contact=mbl,gender=gend,image=pic)
				error = "no"
			except:
				error = "yes"
	context = {
		"error":error
	}
	return render(request,'user_signup.html',context)


def user_home(request):
	if not request.user.is_authenticated:
		return redirect('user_login')
	user = request.user
	blog_post = Usertbl.objects.get(user=user)
	error = ""
	if request.method == 'POST':
		fname = request.POST['firstname']
		lname = request.POST['lastname']
		contact = request.POST['contact']
		gender = request.POST['gender']

		blog_post.user.first_name = fname
		blog_post.user.last_name = lname
		blog_post.contact = contact
		blog_post.gender = gender

		try:
			blog_post.save()
			blog_post.user.save()
			error="no"
		except:
			error="yes"

		try:
			img = request.FILES['image']
			blog_post.image = img
			blog_post.save()
			error="no"
		except:
			pass
	context = {
		"blog_post":blog_post,
		"error":error
	}

	return render(request,'user_home.html',context)


def logout_users(request):
	logout(request)
	return redirect('/')


def user_createblog(request):
	if not request.user.is_authenticated:
		return redirect('user_login')
	error = ""
	if request.method == 'POST':
		blogtitle = request.POST['btitle']
		bintrd = request.POST['bintro']
		bdescrpn = request.POST['bdesc']
		bimg = request.FILES['bimage']

		user = request.user
		user1 = Usertbl.objects.get(user=user)

		try:
			Blogtbl.objects.create(user=user1,title=blogtitle,introduction=bintrd,description=bdescrpn,created_date=date.today(),image=bimg,status="Pending")
			error = "no"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'user_createblog.html',context)


def user_viewblogs(request):
	if not request.user.is_authenticated:
		return redirect('user_login')
	user = request.user
	user1 = Usertbl.objects.get(user=user)
	posted_blogs = Blogtbl.objects.filter(user=user1).order_by('-created_date')
	all_blogs = Paginator(posted_blogs,3)
	page = request.GET.get('page')
	try:
		blogs = all_blogs.page(page)
	except PageNotAnInteger:
		blogs = all_blogs.page(1)
	except EmptyPage:
		blogs = all_blogs.page(1)
	
	context = {
		"blogs":blogs
	}
	return render(request,'user_viewblogs.html',context)


def user_blogdetail(request,id):
	if not request.user.is_authenticated:
		return redirect('user_login')
	posted_blogs = Blogtbl.objects.get(id=id)
	context = {
		"posted_blog":posted_blogs
	}
	return render(request,'user_blogdetail.html',context)


def user_editblog(request,id):
	if not request.user.is_authenticated:
		return redirect('user_login')
	error = ""
	posted_blogs = Blogtbl.objects.get(id=id)
	if request.method == 'POST':
		blogtitle = request.POST['btitle']
		bintrd = request.POST['bintro']
		bdescrpn = request.POST['bdesc']

		user = request.user
		user1 = Usertbl.objects.get(user=user)

		posted_blogs.user = user1
		posted_blogs.title = blogtitle
		posted_blogs.introduction = bintrd
		posted_blogs.description = bdescrpn
		posted_blogs.created_date = date.today()

		try:
			posted_blogs.save()
			error = "no"
		except:
			error = "yes"

		try:
			img = request.FILES['bimage']
			posted_blogs.image = img
			posted_blogs.save()
			error = "no"
		except:
			pass
	context = {
		"posted_blog":posted_blogs,
		"error":error
	}
	return render(request,'user_editblog.html',context)


def user_deleteblog(request,id):
	if not request.user.is_authenticated:
		return redirect('user_login')
	posted_blog = Blogtbl.objects.get(id=id)
	posted_blog.delete()
	return redirect('user_viewblogs')


def user_changepassword(request):
	if not request.user.is_authenticated:
		return redirect('user_login')
	error = ""
	if request.method == "POST":
		crntpwd = request.POST['crpwd']
		newpwd = request.POST['newpwd']
		try:
			user = User.objects.get(id=request.user.id)
			if user.check_password(crntpwd):
				user.set_password(newpwd)
				user.save()
				error = "no"
			else:
				error = "not"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'user_changepassword.html',context)


def admin_login(request):
	if request.user.is_staff:
		return redirect('admin_home')
	error = ""
	if request.method == 'POST':
		uname = request.POST['username']
		pwd = request.POST['pwd']
			
		user = authenticate(request,username=uname,password=pwd)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'admin_login.html',context)


def admin_home(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	users = Usertbl.objects.all().count()
	blogs = Blogtbl.objects.all().count()
	pendblogs = Blogtbl.objects.filter(status='Pending').count()
	accpblogs = Blogtbl.objects.filter(status='Accepted').count()
	rejblogs = Blogtbl.objects.filter(status='Rejected').count()
	messages = Contacttbl.objects.all().count()
	context = {
		"users":users,
		"blogs":blogs,
		"pendblogs":pendblogs,
		"accpblogs":accpblogs,
		"rejblogs":rejblogs,
		"messages":messages
	}
	return render(request,'admin_home.html',context)


def admin_changestatus(request,id):
	# if not request.user.is_staff:
	# 	return redirect('admin_login')
	error = ""
	blogs_data = Blogtbl.objects.get(id=id)
	if request.method == 'POST':
		chsts = request.POST['blogstatus']
		blogs_data.status = chsts

		try:
			blogs_data.save()
			error = "no"
		except:
			error = "yes"
	context = {
		"blogs_data":blogs_data,
		"error":error
	}
	return render(request,'admin_changestatus.html',context)


def admin_pendingblogs(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	blog_data = Blogtbl.objects.filter(status="Pending").order_by('-created_date')
	context = {
		"blog_data":blog_data
	}
	return render(request,'admin_pendingblogs.html',context)

def admin_acceptedblogs(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	blog_data = Blogtbl.objects.filter(status="Accepted").order_by('-created_date')
	context = {
		"blog_data":blog_data
	}
	return render(request,'admin_acceptedblogs.html',context)


def admin_rejectedblogs(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	blog_data = Blogtbl.objects.filter(status="Rejected").order_by('-created_date')
	context = {
		"blog_data":blog_data
	}
	return render(request,'admin_rejectedblogs.html',context)


def admin_allblogs(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	blog_data = Blogtbl.objects.all().order_by('-created_date')
	context = {
		"blog_data":blog_data
	}
	return render(request,'admin_allblogs.html',context)


def admin_deleteblog(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	posted_blog = Blogtbl.objects.get(id=id)
	posted_blog.delete()
	return redirect('admin_allblogs')


def admin_allusers(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	users_data = Usertbl.objects.all().order_by('-user')
	context = {
		"users_data":users_data
	}
	return render(request,'admin_allusers.html',context)


def admin_changepassword(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	error = ""
	if request.method == "POST":
		crntpwd = request.POST['crpwd']
		newpwd = request.POST['newpwd']
		try:
			user = User.objects.get(id=request.user.id)
			if user.check_password(crntpwd):
				user.set_password(newpwd)
				user.save()
				error = "no"
			else:
				error = "not"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'admin_changepassword.html',context)


def admin_deleteusers(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	users_data = Usertbl.objects.get(id=id)
	users_data.delete()
	return redirect('admin_allusers')


def blog_details(request,id):
	posted_blogs = Blogtbl.objects.get(id=id)
	context = {
		"posted_blog":posted_blogs
	}
	return render(request,'blog_details.html',context)


# def serach_blogs(request):
# 	sb = request.POST['searchblog']
# 	blog = Blogtbl.objects.filter(title__icontains=sb)
# 	context = {
# 		"blog":blog
# 	}
# 	return render(request,'index.html',context)

def admin_allmessages(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	all_msgs = Contacttbl.objects.all().order_by('-sender_name')
	context = {
		"msgs":all_msgs
	}
	return render(request,'admin_allmessages.html',context)


def admin_deletemsgs(request,id):
	if not request.user.is_staff:
		return redirect('admin_login')
	msgs = Contacttbl.objects.get(id=id)
	msgs.delete()
	return redirect('admin_allmessages')