from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import *
from .forms import YourModelForm
from django.http import HttpResponse

def custom_authenticate(password):
    try:
        stored_password = Login.objects.get(password=password)
    except Login.DoesNotExist:
        return None
    
    # Check if the provided password matches the stored password
    if check_password(password, stored_password.password):
        # Password matches, return the stored password instance
        # print("Yes, you valid")
        return stored_password
    else:
        # Password doesn't match
        return None

# Create your views here.

def index(request, parameter=None):
    if request.method == 'POST':
        provided_token = request.POST.get('password')

        password_matched = authenticate(username='visitor', password=provided_token)

        if(password_matched):
            login(request, password_matched)
            root_person = Person.objects.first()
            family_tree_data = get_family_tree_data(root_person, 10)

            return render(request, 'index.html', {'tree': family_tree_data})
        else:
            data = {
                'error': 'Invalid Token, try again.'
            }

            return render(request, 'login.html', data)
    else:
        second_search = True
        # Define the possible IDs based on the parameter
        if parameter == '1':
            root_person_id = 2
        elif parameter == '2':
            root_person_id = 14
        elif parameter == '3':
            root_person_id = 15
        else:
            second_search = False
            # Default option or invalid parameter, use a default root person ID
            root_person_id = 1  # You can change this to another default ID or handle it differently

        if root_person_id == 1:
            tree_width = get_object_or_404(Person, pk=1).tree_width
        else:
            tree_width = get_object_or_404(Person, pk=root_person_id).tree_width

        root_person = get_object_or_404(Person, pk=1)

        max_gen = 50

        if root_person_id == 1: 
            max_gen = 1


        # Generate family tree data
        family_tree_data = get_family_tree_data(root_person, max_gen, focused_child=root_person_id)

        all_data = get_family_tree_data(root_person, 50)

        # Render the template with the data
        return render(request, 'lab.html', {'tree': family_tree_data, 'all_data': all_data, 'startingID': root_person_id, 'tree_width': tree_width, 'second_search': second_search})


def lab(request):
    if request.method == 'POST':
        provided_token = request.POST.get('password')

        password_matched = authenticate(username='visitor', password=provided_token)

        if(password_matched):
            login(request, password_matched)
            root_person = Person.objects.first()
            family_tree_data = get_family_tree_data(root_person, 50)

            return render(request, 'lab.html', {'tree': family_tree_data})
        else:
            data = {
                'error': 'Invalid Token, try again.'
            }

            return render(request, 'login.html', data)
    else:
        # if request.user.is_authenticated:
        root_person = Person.objects.first()
        family_tree_data = get_family_tree_data(root_person, 50)

        return render(request, 'lab.html', {'tree': family_tree_data})
        # else:
        #     return render(request, 'login.html')

def adminlogin(request):
    if request.method == 'POST':
        provided_token = request.POST.get('password')

        password_matched = authenticate(username='dev', password=provided_token)

        if(password_matched):
            login(request, password_matched)

            return redirect("/modify")
        else:
            data = {
                'error': 'Invalid Token, try again.'
            }

            return render(request, 'login.html', data)   
    else:
        return render(request, 'login.html')   

def modify(request):
    required_username = "dev"  # Replace with the required username

    # Check if the current user is authenticated and has the required username
    if request.user.is_authenticated and request.user.username == required_username:
        # User is authenticated with the required username, return the main template

        root_person = Person.objects.first()  # Assuming Person model is imported
        family_tree_data = get_family_tree_data(root_person, 50)

        if request.method == 'POST':
            form = YourModelForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'modify.html', {'tree': family_tree_data, 'form': YourModelForm(), 'alert': 'success'})
            else:
                return render(request, 'modify.html', {'tree': family_tree_data, 'form': form})
        else:
            form = YourModelForm()
            return render(request, 'modify.html', {'tree': family_tree_data, 'form': form})
    else:
        # User is not authenticated with the required username, return another template
        return render(request, 'login.html')



def request(request):
    if request.method == 'POST':
        request_text = request.POST.get('content')
        if request_text:
            Request.objects.create(request=request_text)
            return render(request, 'success.html')
        
        data = {
            'error': 'Sorry, you must fill the above text field.'
        }
        return render(request, 'request.html', data)
    else:
        if request.user.is_authenticated:
            return render(request, 'request.html')
        else:
            return render(request, 'login.html')

    
def print_children(request):
    # Get the person with id=2
    parent = Person.objects.get(id=15)
    
    # Define an empty string to store the names
    names = ''
    
    # Recursive function to append children names to the string
    def print_child_names(person):
        nonlocal names
        children = Person.objects.filter(father=person)
        for child in children:
            names += f"{child.first_name}\n"
            # Recursively call the function for each child
            print_child_names(child)

            child.papa = 15
            child.save()
    
    # Start printing children names
    print_child_names(parent)
    
    # Return a plain text response to the browser
    return HttpResponse(names, content_type='text/plain')


def get_family_tree_data(person, max_generations=10, current_generation=0, focused_child=None):
    data = {
        'id': person.id,
        'first_name': person.first_name,
        'farsi_name': person.farsi_name,
        'father': person.father.id if person.father else 'None',
        'children': [],
        'papa': 0 if person.papa is None else person.papa,
        'gen': person.generation
    }

    # Initialize children as an empty queryset
    children = Person.objects.none()

    # Recursively get data for children up to the specified number of generations
    if current_generation < max_generations:
        if current_generation == 1:
            if person.id == focused_child or focused_child == 1 or focused_child == None:
                children = Person.objects.filter(father=person)
                for child in children:
                    data['children'].append(get_family_tree_data(child, max_generations, current_generation + 1,focused_child))
        else:
            children = Person.objects.filter(father=person)
            for child in children:
                data['children'].append(get_family_tree_data(child, max_generations, current_generation + 1,focused_child))

    # Add the count of children and specify "sons" if there are children
    num_children = children.count()
    if num_children > 0:
        child_str = '<div id="langaugeSwap"><p id="nodep" class="english" style="font-size: 14px; color: #E6D2AA80; text-align: center;">' + f"{num_children} {'son' if num_children == 1 else 'sons'}"
        data['num_children'] = child_str + "</p> " + '<p id="nodep" class="farsi" style="font-size: 14px; color: #E6D2AA80; text-align: center;"> ' + f"{num_children}" + " پسر</p></div><div id='circle'></div>"
    else:
        data['num_children'] = ""

    return data


def signout(request):
    logout(request)
    return redirect('/')