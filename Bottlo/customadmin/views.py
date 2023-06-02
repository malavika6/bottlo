from django.shortcuts import render


def supuser(request):
    return render(request,"supuser/adminhome.html")
