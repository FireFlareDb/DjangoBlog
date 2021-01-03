from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# HTML Page


def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse('This is a home page')


def about(request):
    return render(request, 'home/about.html')
    # return HttpResponse('This is a about page')


def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<5 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Message has been sent successfully")
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query) > 300:
        allPosts = []
        messages.error(request, "This is search page not a testing page. We Know What You Are Trying To Do!!!")
        return render(request, 'home/search.html')
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

        params = {'allPosts': allPosts, 'query': query}
        return render(request, 'home/search.html', params)

# Authentication APIS

def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        if len(username) > 20 and len(username) < 5:
            messages.error(request, "Username must be under 5 to 20 charecter ")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain Alphanumerics")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Password don't match")
            return redirect('home')

        # Create the user 
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Your iThACK account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Page Not Found')

    
def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invaild Username And Password, Please try again")
            return redirect("home")

    return HttpResponse('404 - Page Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("home")