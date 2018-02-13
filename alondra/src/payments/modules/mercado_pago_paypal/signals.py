from django.dispatch import Signal

payment_new = Signal(providing_args=['request','payment_method', 'cart_id','user_id'])
#payment_failed = Signal(providing_args=['credentials'])
#payment_closed = Signal(providing_args=['request', 'user_site'])
