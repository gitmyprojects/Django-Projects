from django.urls import path
from account.views import (
	account_view,
	edit_account_view,
)
# new requirement for v.2.2
app_name = 'account'

urlpatterns = [
    # user_id is in carrots because we are using the pk and that will change.
	path('<user_id>/', account_view, name="view"),
	path('<user_id>/edit/', edit_account_view, name="edit"),
]