from django.shortcuts import render, redirect
from .models import Member, Conflict
import datetime, time
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from mpulse.forms import *
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import multiprocessing


def index(request):
    return render(request, 'index.html')

# Create a list of active member
def list(request):
    members_list = Member.objects.all()
    # define how many objects can exist in the member list
    paginator = Paginator(members_list, len(members_list)) 
    page = request.GET.get('page') 
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'members': members})

# Add Member Function
def create(request):
    if request.method == 'POST':
        member = Member(
            first=request.POST["first"],
            last=request.POST['last'],
            telephone=request.POST['telephone'],
            clientid=request.POST['clientid'],
            accountid=request.POST['accountid']
            )
        try:
            member.full_clean()
        # Throw error if member exist
        except ValidationError as e:
            messages.error(request, 'Already Exist')
            return render(request, 'add.html')
        member.save()
        messages.success(request, 'Member was created successfully!')
        return redirect('/list')
        

    else:
        return render(request, 'add.html')

# Edit Member Function
def edit(request, id):
    members = Member.objects.get(id=id)
    context = {'members': members}
    return render(request, 'edit.html', context)

# Update Member Function
def update(request, id):
    member = Member.objects.get(id=id)
    member.first = request.POST['first']
    member.last = request.POST['lastname']
    member.telephone = request.POST['telephone']
    member.clientid = request.POST['clientid']
    member.accountid= request.POST['accountid']
    member.save()
    messages.success(request, 'Member was updated successfully!')
    return redirect('/list')

# Delete Member Function
def delete(request, id):
    member = Member.objects.get(id=id)
    member.delete()
    messages.error(request, 'Member was deleted successfully!')
    return redirect('/list')

# Super User
def users(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {'users': users})

# Delete Super User
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.error(request, 'User was deleted successfully!')
    return redirect('/users')

# Upload CSV Files
def upload_csv(request):
    client = []
    if 'GET' == request.method:
        memberdata = Member.objects.all()
        context = {'member': memberdata}
        return render(request, 'upload.html', context)
    try:
        # First Condition: Make sure there is a file
        csv_file = request.FILES["csv_file"]
        if len(csv_file) == 0:
            messages.error(request, 'Empty File')
            return render(request, 'upload.html')
        # Second Condition: Make sure the file is a CSV file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return render(request, 'upload.html')
        # Rename Data for parsing
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")

        accountids = []
        count = 0
        for index, line in enumerate(lines):
            fields = line.split(",")
            if index == 0:
                # Third Condition: Check if top row CVS fields are as expected
                if (fields[0] == 'first_name') and (fields[1] == 'last_name') and (fields[2] == 'phone_number') and (
                        fields[3] == 'client_member_id') and (fields[4] == 'account_id'):
                    pass
                # Throw an Error if document headers don't match
                else:
                    messages.error(request, 'File is not Correct Headers')
                    return render(request, 'upload.html')
                    break
            else:
                print(index) #Prints number # of lines

            # Save as member if not in database, otherwise save as conflict
            if (len(fields[0]) != 0) and (len(fields[1]) != 0) and (len(fields[2]) != 0) and (len(fields[3]) != 0):
                duplicate = False
                if fields[3] in accountids:
                    duplicate = True
                if fields[2] in accountids:
                    duplicate = True
                if duplicate == False:
                    try:
                        data = Member(
                            first=fields[0],
                            last=fields[1],
                            telephone=fields[2],
                            clientid=fields[3],
                            accountid=fields[4],)
                        accountids.append(fields[3])
                        accountids.append(fields[2])
                        count += 1     
                        data.save()
                    except:
                        pass

                #elif duplicate == True:      The above code will not allow
                #    conf = Conflict(         duplicates. This block will sort
                #        first=fields[0],     duplicates into another table called
                #        last=fields[1],      "conflicts" for further handling.
                #        telephone=fields[2],
                #        clientid=fields[3],
                #        accountid=fields[4],)
                #    conf.save()
                #    count += 1     
        # Message at top of screen once members are added           
        messages.success(request, "Successfully Uploaded CSV File")
        return redirect('/upload/csv/')

    # If one of the coditions weren't met
    except Exception as e:
        messages.error(request, "Unable to upload file. " + e)
        return redirect('/upload')


