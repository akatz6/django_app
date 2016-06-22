from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
import bcrypt
from django.db import models
import re
from django.contrib import messages
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
	def registeration(self, name, alias, email, password, confirm_password):
		errors = []
		errors.append(self.validate_length(name, 'name', 2, 'Name is too short'))
		errors.append(self.validate_length(alias, 'alias', 2, 'Alias is too short'))
		errors.append(self.validate_email(email))
		errors.append(self.validate_passwords(password, confirm_password))
		error = []

		for elements in range(0, len(errors)):
			try:
				error.append(errors[elements][1])
			except:
				pass
		error2 = {}
		for d in error:
			error2.update(d)

		if not bool(error2):
			pw_bytes = password.encode('utf-8')
			hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
			Register.objects.create(name = name, alias = alias,
			password = hashed, email = email)
			success = {}
			success['success'] = "Registeration comeplete, please log in"
			return (True, success)
		else:
			return (False, error2)

	def login(self, email, password):
		errors = {}
		valid = True
		try:
			registered = Register.objects.get(email = email)
		except:
			errors['email'] = "Email Not found"
			valid = False

		if(valid):
			pw_bytes = password.encode('utf-8')
			salt = registered.password.encode('utf-8')
			
			if bcrypt.hashpw(pw_bytes, salt) != salt:
				errors['password'] = "Email and password do not match"
				return (False, errors)
			else: 
				errors['password'] = "Succes"
				return (True, errors)
		else:
			return (False, errors)


	def validate_length(self, test, name, alength, error_string):
		errors = {}
		if len(test) < alength:
			errors[name] = error_string
			return(False, errors)

	def validate_email(self, email_address):
		errors = {}
		if not EMAIL_REGEX.match(email_address):
			errors['email'] = "Please enter a valid email"
			return(False, errors)

	def validate_passwords(self, password, confirm_password):
		errors = {}
		if password != confirm_password:
			errors['password'] = "Passwords do not match"
			return(False, errors)
		elif len(password) < 8:
			errors['password'] = "Passwords need to be longer than 8 characters"
			return(False, errors)
	# def login(self, test, name, alength, error_string):
# Create your models here.
class Register(models.Model):
	name = models.CharField(max_length=45)
	alias = models.CharField(max_length=45)
	password = models.TextField(max_length=1000)
	email = models.EmailField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	userManager = UserManager()
	objects = models.Manager()
