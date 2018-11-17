from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

def homePage(request):
    return render(request,'home.html')

def newList(request):
    Item.objects.create(name=request.POST['reminder_name'],
                        daysAhead=request.POST['reminder_days_ahead'],
                        time=request.POST['reminder_time'])
    return redirect('/lists/THElist')

def viewList(request):
    reminderTextList = [f'{i+1}: {r.name} at {r.time} in {r.daysAhead} days'
                        for i,r in enumerate(Item.objects.all())]
    return render(request,'reminders.html',{'reminders':reminderTextList})
