from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item

def homePage(request):
    if request.method == 'POST':
        Item.objects.create(name=request.POST['reminder_name'],
                            daysAhead=request.POST['reminder_days_ahead'],
                            time=request.POST['reminder_time'])
    reminderTextList = [f'{r.id}: {r.name} at {r.time} in {r.daysAhead} days' for r in Item.objects.all()]
    return render(request,'home.html',{'reminders':reminderTextList})
