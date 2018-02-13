import paypalrestsdk
from django.core.urlresolvers import resolve
from django.conf import settings
from payments.signals import payment_new
from payments.models import PaymentMethod, PaymentMethodFields
from orders.models import Orders, OrderShippingItem
from user_addresses.models import Addresess
from user.models import CustomUser as User
from cart.cart2 import Cart,Cart2, CART_ID, ItemAlreadyExists
from urlparse  import urlsplit, parse_qs
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# middleware to process payment
class PaymentPaypalMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
       
        
        current_url = resolve(request.path_info)
        url_name = current_url.url_name
        
        if url_name == 'payment_sucesss': 
            payer_id = request.GET.get('PayerID',None)
            payment_id = request.GET.get('paymentId',None)
            if payer_id is not None and payment_id is not None:
                paypalrestsdk.configure({
                    "mode": settings.PAYPAL_MODE,
                    "client_id": settings.PAYPAL_CLIENT_ID,
                    "client_secret": settings.PAYPAL_CLIENT_SECRET 
                })
                payment = paypalrestsdk.Payment.find(
                    payment_id
                )
               
                if payment.execute({"payer_id": payer_id}):
                    print("Payment execute successfully")
                    if len(payment.transactions) > 0:
                        params = parse_qs(payment.transactions[0].custom)
                        D = PaymentMethod()   
                        D.payment_method = "paypal"
                        D.status = "Aprobbed"
                        D.amount = payment.transactions[0].amount.total
                        D.currency = payment.transactions[0].amount.currency
                        D.save()

                        pf = PaymentMethodFields()
                        pf.payment = D
                        pf.key = "first_name"
                        pf.value = payment.payer.payer_info.first_name
                        pf.save()
                        
                        pf = PaymentMethodFields()
                        pf.payment = D
                        pf.key = "last_name"
                        pf.value = payment.payer.payer_info.last_name
                        pf.save()
                        pf = PaymentMethodFields()
                        pf.payment = D
                        pf.key = "email"
                        pf.value = payment.payer.payer_info.email


                        pf.save()
                            
                           
                        o = Orders()
                        o.status = "pending"
                        o.payment_method = pf


                        try:
                            o.shipping_addresss = Addresess.objects.get(id=int(params['shipping_addresss_id']))
                        except Addresess.DoesNotExist:
                            pass
                        try:
                            o.billing_addresss = Addresess.objects.get(id=int(params['billing_addresss_id']))
                        except Addresess.DoesNotExist:
                            pass
                        try:
                            o.autor = User.objects.get(id=int(params['user_id']))
                        except User.DoesNotExist:
                            pass
                        
                        o.save()

                        cart = Cart(params['cart_id'])

                        for c in cart.items():
                            os = OrderShippingItem()
                            os.order = o
                            os.product = c.product
                            os.price = c.unit_price
                            os.qty = c.quantity
                            os.save()
