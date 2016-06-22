from django.shortcuts import render
from . models import Register


# Create your views here.
def index(request):
	return render(request, 'p_django_app/index.html')

def register(request):
	name = request.POST['name']
	alias = request.POST['alias']
	email = request.POST['email']
	password = request.POST['password']
	confirm_password = request.POST['confirm_password']
	errors = Register.userManager.registeration(name, alias, email, password, confirm_password)

	context = {
	"errors" : errors[1]
	}

	return render(request, 'p_django_app/index.html', context)

def login(request):
	email = request.POST['email']
	password = request.POST['password']
	errors = Register.userManager.login(email, password)
	
	context = {
	"errors_login" : errors[1]
	}
	return render(request, 'p_django_app/index.html', context)
