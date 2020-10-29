from django.contrib import admin
from .models import Thread , ChatMessage
# Register your models here.
class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user','status')

# admin.site.register(Thread, ThreadAdmin)
