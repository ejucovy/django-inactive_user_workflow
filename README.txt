This package provides some extensions and overrides to django.contrib.auth and 
django-registration to streamline the experience for new users registering for
your site.

Independent components are provided for the following tweaks:

 1. Let inactive users log in to your django site
 2. Log in the new user automatically after initial site registration
 3. Redirect inactive users to a page of your choice when they try to
    access "restricted" content

They can be wired up semi-independently.

You must have 'django.contrib.auth' in your INSTALLED_APPS.

You must have 'registration' in your INSTALLED_APPS.

To install, add 'inactive_user_workflow' to your INSTALLED_APPS. No models are defined,
so you don't need to re-run syncdb.

========
Using it
========

The simplest way to use it is to include a URLconf pattern like

 (r'^accounts/', include('inactive_user_workflow.urls'))

in your root URLconf. This will register its own views and also the
non-overridden views from django-registration and django.contrib.auth
but will not register the inactive-user-catching middleware (see below).
But if you're using Django permission checks properly, the middleware
will be optional, because django.contrib.auth always returns False
for permission checks on inactive users.

The details
===========

Two views are provided:

 inactive_user_workflow.views.registration.register

This overrides django-registration's registration_register view with
one behavioral change: it logs in the user automatically after initial
account creation.

 inactive_user_workflow.views.login.login

This overrides django.contrib.auth's auth_login view with one behavioral
change: it allows inactive users to log in to your site.

One middleware is provided:

 inactive_user_workflow.middleware.CatchInactiveUsersMiddleware

If activated, this middleware intercepts requests by logged-in inactive 
users and redirects them to a view named 'inactive-user'.

A simple direct-to-template 'inactive-user' view is also provided; it
is published at the URL /accounts/inactive/ (assuming you mount the
package's URLs at /account/). (So I lied earlier; three views are provided.)
You will likely want to override the provided template registration/inactive_user.html,
or even override the view with your own custom view.

You can define a list of URL paths that inactive users *should* be allowed
to access without being kicked over to the 'inactive-user' view. To do this,
add a list of URL prefixes to your settings.py named ANONYMOUS_PATHS, like so:

ANONYMOUS_PATHS = ('/accounts/', '/site_media/', '/publicview/')
