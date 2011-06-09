from django.core.management.base import BaseCommand

from inactive_user_workflow.lib import resend_mail

class Command(BaseCommand):
    def handle(self, username, debug=None, *args, **options):
        if debug is not None:
            message, email = resend_mail(username, send=False)
        else:
            message, email = resend_mail(username)

        print "To: %s" % email
        print message
        if debug is not None:
            print "(No email sent because the command was run with debug mode ON)"
        else:
            print "(Email sent)"

        return
