from django.shortcuts import render, redirect
from graphql import GraphQLError
from .schema import schema
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def users_list(request):
    query = '''
        query {
            users {
                edges {
                    node {
                        id
                        username
                        email
                    }
                }
            }
        }
    '''
    try:
        result = schema.execute(query)
    except GraphQLError as e:
        return render(request, 'error.html', {'error': e})

    if result.errors:
        return render(request, 'error.html', {'error': result.errors})

    users = result.data['users']['edges']
    user_data = []
    for user in users:
        node = user['node']
        user_data.append({
            'id': node['id'],
            'username': node['username'],
            'email': node['email'],
        })
    for user in user_data:  
        print(user['username'])    
    return render(request, 'users_list.html', {'users': user_data})

def me(request):
    query = '''
        query {
            me {
                 id
                 username
                        email
                }
        }
    '''
    try:
        result = schema.execute(query, context_value=request)
    except GraphQLError as e:
        return render(request, 'error.html', {'error': e})

    if result.errors:
        return render(request, 'error.html', {'error': result.errors})

    user_data = [
        {
            'id': result.data['me']['id'],
            'username': result.data['me']['username'],
            'email': result.data['me']['email'],
        }
    ]
    print (user_data[0])
    return render(request, 'me.html', {'user': user_data[0]})

@login_required
def home(request):
    query = '''
        query {
            me {
                 id
                 username
                        email
                        profilePic
                               firstName

                }
        }
    '''
    try:
        result = schema.execute(query, context_value=request)
    except GraphQLError as e:
        return render(request, 'error.html', {'error': e})

    if result.errors:
        return render(request, 'error.html', {'error': result.errors})

    user_data = [
        {
            'id': result.data['me']['id'],
            'username': result.data['me']['username'],
            'email': result.data['me']['email'],
            'profile_pic': result.data['me']['profilePic'],
            'first_name': result.data['me']['firstName'],
            
        }
    ]
    print (user_data[0])
    return render(request, 'home.html', {'users': user_data[0]})

def register(request):
    if request.method == 'POST':
        query = '''
            mutation {
                register(
                    email: "%s",
                    username: "%s",
                    password1: "%s",
                    password2: "%s"
                ) {
                    success,
                    errors,
                    token,
                    refreshToken
                }
            }
        ''' % (
            request.POST['email'],
            request.POST['username'],
            request.POST['password1'],
            request.POST['password2'],
        )

        try:
            result = schema.execute(query, context_value=request )
        except GraphQLError as e:
            return render(request, 'error.html', {'error': e})

        if result.errors:
            return render(request, 'error.html', {'error': result.errors})

        success = result.data['register']['success']
        if success:
            
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            # Log in the user
            login(request, user)
            return redirect('users')
        else:
            errors = result.data['register']['errors']
            return render(request, 'error.html', {'error': errors})

    return render(request, 'register.html')
