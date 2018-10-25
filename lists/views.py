from django.shortcuts import render
from django.http import HttpResponse

def homePage(request):
    if request.method == 'POST':
        newReminderText = '1: %s at %s in %s days' % (request.POST['reminder_name'],
                                                       request.POST['reminder_time'],
                                                       request.POST['reminder_days_ahead'])
        return render(request,'home.html',{'newReminderText':newReminderText})
    return render(request,'home.html')
