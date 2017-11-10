from django.core.urlresolvers import reverse_lazy
from line_app.models import User
from django import forms
# Create your views here.
from django.views.generic import CreateView


class CreateUserView(CreateView):
    template_name = "accounts/create.html"
    model = User
    fields = ("username","password")
    success_url = reverse_lazy("main")

    def get_form(self):
        form = super(CreateUserView,self).get_form()
        form.fields["password"].widget = forms.PasswordInput()
        return form