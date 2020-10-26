from django.shortcuts import render, redirect             
from .models import Member, Conflict                      # Api tables
import time                                               # For timing system rest period                 
from django.contrib import messages                       # Error, success messages
from mpulse.forms import *                                # Admin/superuser if needed
from django.core.exceptions import ValidationError        # Unit testing/ exceptions
from django.core.paginator import (                       # paginator for searching members
    Paginator,                                            
    EmptyPage,                                        
    PageNotAnInteger) 
from tqdm import tqdm as progress                         # Terminal progress bar

# Home/Index
def index(request):
    return render(request, 'index.html')
 

# Member List 
def list(request):
    members_list = Member.objects.all()
    # define how many objects can exist in the member list
    paginator = Paginator(members_list, len(members_list)+10) 
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
            accountid=request.POST['accountid'])
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


# Update "Member" Function
def update(request, id):
    try:
        member = Member.objects.get(id=id)
        member.first = request.POST['first']
        member.last = request.POST['lastname']
        member.telephone = request.POST['telephone']
        member.clientid = request.POST['clientid']
        member.accountid= request.POST['accountid']
        member.save()
        messages.success(request, 'Member was updated successfully!')
    except:
        messages.error(request, 'Nothing to update')
    return redirect('/list')


# Delete Member Function
def delete(request, id):
    try:
        member = Member.objects.get(id=id)
        member.delete()
        messages.error(request, 'Member was deleted successfully!')
    except:
        messages.error(request, 'Member not in system')
    return redirect('/list')


# Delete Conflict
def conflict_delete(request, id):
    try:
        conflict = Conflict.objects.get(id=id)
        conflict.delete()
        messages.error(request, 'Conflict deleted successfully!')
    except:
        messages.error(request, 'Member not in system')
    return redirect('/upload')
    # Next, add conflict_edit and conflict_update 
    # This will give the option to edit conflict 
    # user's acct or phone and save as a Member


# Upload Sort, and Save CSV Files
def upload(request):
    wait = 0 # Sleeper for CRUD during upload
    accountids = [] # Holds current document "unique=True" fiels
    added = 0

    if 'GET' == request.method:
        memberdata = Conflict.objects.all()
        context = {'memberdata': memberdata}
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
        # Prepare Data for parsing
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
            
        # Begin loop through CSV file lines
        for index, line in progress(enumerate(lines)):
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
         
            # Save as member if not in database, otherwise save as conflict
            if (len(fields[0]) != 0) and (len(fields[1]) != 0) and (len(fields[2]) != 0) and (len(fields[3]) != 0):
                # Check if current data appeared in current document
                duplicate = False
                if fields[3] in accountids:
                    duplicate = True
                if fields[2] in accountids:
                    duplicate = True
                if fields[2] == 'phone_number':
                    duplicate = True
                # Save to database if doesn't already exist
                if duplicate == False:
                    try:
                        data = Member(
                            first=fields[0],
                            last=fields[1],
                            telephone=fields[2],
                            clientid=fields[3],
                            accountid=fields[4],)
                        # Tracking system for current document items
                        accountids.append(fields[3])
                        accountids.append(fields[2]) 
                        added += 1
                        data.save()
                        # Sleeper allows for CRUD operations during upload
                        # A more robust version would be using multiprocessors
                        if wait == 5:               
                            time.sleep(.2)  
                            wait = 0
                        else:
                            wait += 1
                    except:
                        if wait == 5:
                            time.sleep(.2)
                            wait = 0
                        else:
                            wait += 1
                        pass

                # 10.A If the person is in system
                elif duplicate == True:           # When commented this block will not allow
                    conf = Conflict(              # duplicates. This block will sort
                        first=fields[0],          # duplicates into another table called
                        last=fields[1],           # "conflicts" for further handling.
                        telephone=fields[2],
                        clientid=fields[3],
                        accountid=fields[4],)
                    conf.save()  
        # Message at top of screen once members are added 
        messages.success(request, "Successfully Uploaded CSV File")
        return redirect('/upload')
    # If one of the coditions weren't met
    except Exception as e:
        messages.error(request, "Unable to upload file. " + e)
        return redirect('/upload')


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
    try:
        user = User.objects.get(id=id)
        user.delete()
    except:
        messages.error(request, 'User was deleted successfully!')
    return redirect('/users')


