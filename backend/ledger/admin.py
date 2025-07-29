from django.contrib import admin
from .models import User, LedgerItem

# Junior: Basic admin registration without customization
admin.site.register(User)
admin.site.register(LedgerItem)