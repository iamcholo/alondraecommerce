from django.dispatch import Signal

user_site_logged_in = Signal(providing_args=['request', 'user_site'])
user_site_login_failed = Signal(providing_args=['credentials'])
user_site_logged_out = Signal(providing_args=['request', 'user_site'])
