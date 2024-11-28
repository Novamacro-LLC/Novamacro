from django.shortcuts import render

def market_dash(request):
    return render(request, 'market_dash.html')