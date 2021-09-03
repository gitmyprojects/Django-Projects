from django.shortcuts import render

def home_screen_view(request):
	context = {}
	# because 'personal' is added to the settings.py file in the root file
	# in the 'TEMPLATES' variable, django will look through all the directories for 'templates'
	# Django will see the 'personal' folder inside 'personal' directory which is why we put
	# 'personal' THEN a forward slash.
	return render(request, "personal/home.html", context)
