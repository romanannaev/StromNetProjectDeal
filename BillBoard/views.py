from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template 

def other_page(request, page):
    try:
        template = get_template('BillBoard/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
# Create your views here.
def render_base_template(request):
    return render(request, 'layout/basic.html')


from django.contrib.auth.views import LoginView
class BBLoginView(LoginView):
    template_name = 'BillBoard/login.html' 
    def dispatch(self, request, *args, **kwargs):
        
        if request.method == 'GET':
            next1 = request.GET.get(self.REDIRECT_FIELD_NAME)
            print(str(next1))

        else :
            print('nothing')
        return super().dispatch(request, *args, **kwargs)


from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
    return render(request, 'BillBoard/profile.html')


from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'BillBoard/logout.html'


from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from BillBoard.forms import ChangeUserInfoForm
from BillBoard.models import AdvUser

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'BillBoard/change_user_info.html'    
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('BillBoard:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, args, *kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

from django.contrib.auth.views import PasswordChangeView

class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'BillBoard/password_change.html'
    success_url = reverse_lazy('BillBoard:profile')
    success_message = 'Пароль пользователя изменен'

from .forms import RegisterUserForm
from django.views.generic.edit import CreateView

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'BillBoard/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('BillBoard:register_done')

from django.views.generic.base import TemplateView

class RegisterDoneView(TemplateView):
    template_name = 'BillBoard/register_done.html'


from django.core.signing import BadSignature
from .utilities import signer

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'BillBoard/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'BillBoard/user_is_activated.html'
    else:
        template = 'BillBoard/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


from django.contrib.auth import logout
from django.views.generic.edit import DeleteView
from django.contrib import messages

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'BillBoard/delete_user.html'
    success_url = reverse_lazy('BillBoard:main')
    
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                                      'Пользователь удалён')
        return super().post(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)