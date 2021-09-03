from django import forms
# google the django class to see the source code. Ex. 'UserCreationForm' class.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

# ----------------------REGISTRATION FORM-------------------------------------
class RegistrationForm(UserCreationForm):
	# there is no email field in the built in UserCreationForm so we're adding it here.
	# 'help text' is what will be displayed if they enter something invalid or missing
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		# what model we are abstracting from
		model = Account
		# here are the fields that the form will require. username and passwords are built-in to UserCreationForm class
		fields = ('email', 'username', 'password1', 'password2', )

	# ------------form validation functions-------------
	# by prepending 'clean' to username, django knows to run this function when the form is submitted.
	def clean_email(self):
		# this is a function that is executing. its saying, get this value from the form
		# itself and look for the field 'email' and cast it to lowercase
		# [email] is the NAME indicated in the register.html page as 'name=email' attribute (line 43)
		email = self.cleaned_data['email'].lower()
		# this is saying look inside the Account table in the db, and 'get' (followed by the search criteria) email.
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			# if the email does not exist in the Account db, return email
			return email
		# if the email already exists in the table, raise this Validation Error
		raise forms.ValidationError('Email "%s" is already in use.' % email)


	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)

	# ------------End of form validation functions-------------
# -------------------END OF REGISTRATION FORM-------------------------------------



class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


    def save(self, commit=True):
		#save(commit=False) is a db transaction that wont be commited to the db.
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account
# ----------------------CUSTOM FORM FOR AUTHENTICATING-------------------------------------
class AccountAuthenticationForm(forms.ModelForm):
	# we're using a custom password field because we want to add the correct widget
	# this widget will hide the password while typing.
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")





# -----------------END OF CUSTOM FORM FOR AUTHENTICATING-------------------------------------



#-----------------------------Notes-----------------------------------------------
# the 'get' keyword will return a single row
	# filter will return multiple rows aka a query set
#