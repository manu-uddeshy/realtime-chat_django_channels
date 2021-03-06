from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.http import request
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from online_users.models import OnlineUserActivity
from datetime import timedelta

@login_required
def OnlineUsers(request):
    user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=3))
    number_of_active_users = user_activity_objects.count()

    online_users = user_activity_objects
    current_user = get_user_model()

    return render(request,'chat/online.html',{"online_users":online_users , "current_user": current_user})

class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

