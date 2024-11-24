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
