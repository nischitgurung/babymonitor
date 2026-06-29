from django.shortcuts import render, redirect

from django.contrib.auth import authenticate

from django.contrib.auth import login

from django.contrib.auth import logout

from .forms import RegisterForm


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = RegisterForm()

    return render(request,
                  "register.html",
                  {
                      "form": form
                  })


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]

        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("dashboard")

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect("login")