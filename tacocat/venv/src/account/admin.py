from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


# this is setting up a custom admin panel
class AccountAdmin(UserAdmin):
    #
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
    # this is preventing admin from making any changes to these fields
	readonly_fields=('id', 'date_joined', 'last_login')

# these are required
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Account, AccountAdmin)