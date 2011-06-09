"""
URLConf for Django user registration and authentication.

If the default behavior of the registration & authentication views is 
acceptable to you, simply use a line like this in your root URLConf to 
set up the default URLs for registration::

    (r'^accounts/', include('inactive_users_workflow.urls')),

This will also automatically set up the views in django-registration and
``django.contrib.auth`` at sensible default locations.

But if you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead. If you do, it's a
good idea to use the names ``registration_activate``,
``registration_complete`` and ``registration_register`` for the
various steps of the user-signup process.
"""

from django.conf.urls.defaults import *

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

                       url(r'^resend-confirmation/$',
                           'inactive_user_workflow.views.resend_confirmation_email',
                           name='resend-user-confirmation'),

                       url(r'^inactive/$',
                           direct_to_template,
                           {'template': 'registration/inactive_user.html'},
                           name='inactive-user'),

                       url(r'^login/$',
                           'inactive_user_workflow.views.login.login',
                           {'template_name': 'registration/login.html'},
                           name='auth_login'),
                       
                       url(r'^register/$',
                           'inactive_user_workflow.views.register.register',

                           ######################################
                           # You can customize this for your site
                           # with some arguments to the view, like
                           #{'profile_callback': create_profile,
                           # 'form_class': UserProfileForm
                           # },
                           #### see django-registration docs for details
                           #######################################
                           name='registration_register'),


                       url(r'^activate/(?P<activation_key>\w+)/$',
                           'inactive_user_workflow.views.register.activate',
                           name='registration_activate'),

                       # now we'll delegate to django-registration
                       # for the rest of the urlconf
                       (r'', include('registration.urls')),

                       )

