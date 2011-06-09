from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from djangohelpers.middleware import path_matches

class CatchInactiveUsersMiddleware(object):
    def process_request(self, request):
        if request.path == reverse('inactive-user'):
            return None

        if path_matches(request.path, getattr(settings, 'INACTIVE_PATHS', [])):
            return None

        if not request.user.is_authenticated():
            return None

        if request.user.is_authenticated() and not request.user.is_active:

            # @@TODO: add a cfgable notification/flash/portalstatus message callback 
            #         somehow (settings.py i guess :-/)

            response = HttpResponseRedirect(reverse('inactive-user'))
            response.status_code = 307  # please don't cache?
            return response
