from django.contrib import admin
from Main.models import User, UserInformation

admin.site.register(User)  # Show accounts on admin console
admin.site.register(UserInformation)