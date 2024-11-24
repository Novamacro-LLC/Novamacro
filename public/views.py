from lib2to3.fixes.fix_input import context

from django.shortcuts import render


#Create view for the home page
def home(request):
    title = 'Novamacro, LLC Home'
    desc = ('At Novamacro, we help small and medium businesses harness the power of emerging technologies to drive '
            'growth, increase efficiency, and unlock new opportunities.')
    context = {
        'title': title,
        'desc': desc,
    }
    return render(request, 'public/index.html', context)


#Create view for about page
def about(request):
    title = 'Novamacro, LLC About Us'
    desc = ('Founded in 2017 in the heart of the Memphis area, Novamacro LLC bridges the gap between cutting-edge '
            'technology and the practical needs of growing businesses.')
    context = {
        'title': title,
        'desc': desc,
    }
    return render(request, 'public/about-us.html', context)
