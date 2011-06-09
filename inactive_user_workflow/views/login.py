###################################################
###################################################
###################################################
######                                       ######
######            inactive users             ######
######      should be allowed to log in      ######
######         contrib-dot-auth fork         ######
######                                       ######
###################################################
###################################################
###################################################


from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36

from django.contrib.auth.forms import AuthenticationForm

from datetime import timedelta

#### XXXX see http://code.djangoproject.com/ticket/12103, hopefully this can 
#         go away
class Form(AuthenticationForm):
    """
    override core contrib login form to allow inactive accounts to log in.
    """
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data


#### XXXX this half can go away in 1.2 and greater b/c there will be an authentication_form arg
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.http import urlquote, base36_to_int
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
def login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "Displays the login form and handles the login action."
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = Form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            
            if request.POST.get('remember') == 'on':
                request.session.set_expiry(timedelta(3000))
            
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = Form(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
login = never_cache(login)

