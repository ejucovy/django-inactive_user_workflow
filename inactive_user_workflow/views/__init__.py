from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from djangohelpers.lib import rendered_with, allow_http
from inactive_user_workflow.lib import resend_mail

@allow_http("GET", "POST")
@rendered_with('registration/resend-confirmation-success.html')
def resend_confirmation_email(request):

    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == "GET":
        return renderform(request)

    username = request.POST['username']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return nosuchuser(request, username)

    if user.is_active:
        return notinactive(request, username)

    resend_mail(username)

    return {'username': username, 'user': user}

from inactive_user_workflow.forms import ReconfirmForm
@rendered_with('registration/resend-confirmation-form.html')
def renderform(request):
    form = ReconfirmForm()
    return {'form': form}

@rendered_with('registration/resend-confirmation-nouser.html')
def nosuchuser(request, username):
    form = ReconfirmForm()
    return {'form': form,
            'username': username}

@rendered_with('registration/resend-confirmation-notinactive.html')
def notinactive(request, username):
    form = ReconfirmForm()
    return {'form': form,
            'username': username}
