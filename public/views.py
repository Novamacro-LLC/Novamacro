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


#Create view for products page
def products(request):
    title = 'Novamacro, LLC Products'
    desc = ('At Novamacro, we provide comprehensive technology solutions designed to meet the diverse needs of small '
            'and medium-sized businesses. ')
    context = {
        'title': title,
        'desc': desc,
    }
    return render(request, 'public/product.html', context)


#Create view for consulting page
def consulting(request):
    title = 'Novamacro, LLC Consulting'
    desc = ('Transform your business operations with consulting services tailored to your unique needs. ')
    context = {
        'title': title,
        'desc': desc,
    }
    return render(request, 'public/consulting.html', context)
