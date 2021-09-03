from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


# create custom user account manager
class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),# normalize will make it lowercase
			username=username, #they are not using username to login so we dont need to mormalize it
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

# -------------------basic structure if you want to create a custom user model--------------#
def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "tacocat/logo_1080_1080.png"



# extend the AbstractBaseUser class
class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email				= models.BooleanField(default=True)

# this is overwritting the django default login field to be an email rather than an username
    # both of these are required to create an Account
	USERNAME_FIELD = 'email' # 'email' comes from the variable set in the Account class
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

# when you access the object, what is going ot be returned if you dont access any of the individual fields
    # like a default return value if you dont access an individual field within the class
	def __str__(self):
		return self.username # here we are telling it to return the 'username'


# this is going to take whatever the image filename is and replace it with what we want (profile_image.png)
	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

# ----------------end of basic structure if you want to create a custom user model--------------#

#----------------------------------notes------------------------
# unique = True attribute is important so no two objects are the same
# auto_now_add = sets a flag when that object is created so as soon as an Account object is created
    # the flag will get set
# auto_now = every time they log in or alter the account, the date will get set/overwritten
# have to get a package that supports an image field
    #  pip install pillow
    # pillow allows us to use an image field
    # !!! pip freeze > requirements.txt !!!!!
        #dont forget this so we can note what versions are installed/required