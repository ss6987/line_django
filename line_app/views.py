from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from line_app.models import User,Relationship
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
class SampleTemplateView(TemplateView):
    template_name = "HTML/index.html"


@method_decorator(login_required, name='dispatch')
class MainView(TemplateView):
    template_name = "HTML/user_main.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        users = User.objects.all()
        login_user = users.get(username=self.request.user.username)
        context['user'] = login_user
        users = users.filter(~Q(username=login_user.username))
        for friend in login_user.get_followers():
            users = users.filter(~Q(username=friend.username))
        context['others'] = users
        rooms = login_user.get_rooms()
        room_names = login_user.get_room_names()
        user_rooms = []
        for i in range(len(room_names)):
            user_rooms.append([rooms[i],room_names[i]])
        context['rooms'] = user_rooms
        return context

    def post(self,request,*args,**kwargs):
        action = request.POST["action"]
        if action == "add_friend" or action == "delete_friend":
            login_user = User.objects.get(username=self.request.user.username)
            target_name = request.POST["target_name"]
            target_user = User.objects.get(username=target_name)
            if action == "add_friend":
                relationship = Relationship(follow=login_user, follower=target_user)
                relationship.save()
            elif action == "delete_friend":
                relationship = Relationship.objects.all().filter(follow=login_user).filter(follower=target_user)
                relationship.delete()
        context = self.get_context_data()
        return render(request,self.template_name,context)