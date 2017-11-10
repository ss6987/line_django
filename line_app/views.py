from django.shortcuts import render,redirect
# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from line_app.models import User, Relationship, Talk, Room
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
            user_rooms.append([rooms[i], room_names[i]])
        context['rooms'] = user_rooms
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        login_user = User.objects.get(username=self.request.user.username)
        target_name = request.POST["target_name"]
        target_user = User.objects.get(username=target_name)
        if action == "add_friend":
            relationship = Relationship(follow=login_user, follower=target_user)
            relationship.save()
        elif action == "delete_friend":
            relationship = Relationship.objects.all().filter(follow=login_user).filter(follower=target_user)
            relationship.delete()
        elif action == "create_room":
            room = Room.objects.filter(Q(user__in=[login_user]) and Q(user__in=[target_user]))
            if not room.exists():
                room = Room()
                room.save()
                room.user.add(login_user)
                room.user.add(target_user)
                room.save()
                return redirect("talk",room_id=room.id)
            else:
                return redirect("talk",room_id=room.first().id)
        context = self.get_context_data()
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class TalkView(TemplateView):
    template_name = "HTML/talk.html"

    def get_context_data(self, **kwargs):
        context = super(TalkView, self).get_context_data(**kwargs)
        room = Room.objects.get(id=context['room_id'])
        members = room.user.all()
        flag = False
        for member in members:
            if member == self.request.user:
                flag = True
        if flag:
            talks = Talk.objects.all().filter(room=room).order_by("timestamp")
            context['talks'] = talks
        else:
            self.template_name = "HTML/take_error.html"
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        text = request.POST['text']
        talk = Talk(
            room=Room.objects.get(id=context['room_id']),
            user=self.request.user,
            text=text
        )
        talk.save()
        return render(request, self.template_name, context)
