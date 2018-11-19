from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item, List


def createItemFromPOST(request,listID):
    lst = List.objects.get(id=listID)
    Item.objects.create(name=request.POST['reminder_name'],
                        daysAhead=request.POST['reminder_days_ahead'],
                        time=request.POST['reminder_time'],list = lst)


def homePage(request):
    return render(request,'home.html')

def newList(request):
    lst = List.objects.create()
    createItemFromPOST(request,lst.id)
    return redirect(f'/lists/{lst.id}/')

def viewList(request,listID):
    lst = List.objects.get(id=listID)
    reminderTextList = [f'{i+1}: {r.name} at {r.time} in {r.daysAhead} days'
                        for i,r in enumerate(Item.objects.filter(list=lst)) ]
    return render(request,'reminders.html',{'reminders':reminderTextList,
    'listID':listID})


def addToList(request,listID):
    lst = List.objects.get(id=listID)
    createItemFromPOST(request,listID)
    return redirect(f'/lists/{lst.id}/')
