import json
import mercadopago
import paypalrestsdk
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from payments.models import PaymentMethod, PaymentMethodFields
from orders.models import Orders, OrderShippingItem
from user_addresses.models import Addresess
from user.models import CustomUser as User
from cart.cart2 import Cart,Cart2, CART_ID, ItemAlreadyExists
#from payments.signals import payment_new


@api_view(['GET'])
@permission_classes((AllowAny,))
def create_mercadopago_checkout(request):
    
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    
    host = protocol +"://" + request.get_host()
    
    mp = mercadopago.MP(
            settings.MERCADOPAGO_CLIENT_ID, 
            settings.MERCADOPAGO_CLIENT_SECRET
        )
    
    items = []
    
    cart = Cart(request)
    
    for c in cart.items():
        
        items.append({
                "title": c.product.title,
                "quantity": 1,
                "currency_id": "VEF",
                "unit_price": c.product.pricing
            })

    preference = {
        "items": items,
        "external_reference": {
            "user_id":request.user.id,
            "shipping_addresss_id":request.session['shipping_address'],
            "billing_addresss_id":request.session['billing_address'],
            "cart_id":cart.cart_id,
        },
        "back_urls": {
            "failure": host + reverse("payment_cancel"),
            "pending": host + reverse("payment_fail"),
            "success": host + reverse("payment_sucesss")
        },
        "notification_url": host + reverse("payment_mercadopago_process")
    }
    
    preferenceResult = mp.create_preference(preference)
    
    return Response(
      {'result':preferenceResult['response']['init_point']} 
    )

@api_view(['POST','GET'])
@permission_classes((AllowAny,))
def process_mercadopago(request):
        
    if request.method == 'POST':
        pk = request.query_params.get("id")
         
        mp = mercadopago.MP(
            settings.MERCADOPAGO_CLIENT_ID, 
            settings.MERCADOPAGO_CLIENT_SECRET
        )
        paymentInfo = mp.get_payment (pk)
        
        if paymentInfo["status"] == 200:
            data = json.dumps(paymentInfo, indent=4)
          

            D.payment_method = "mercadopago"
            D.status = "Aprobbed"
            D.amount = 0.00
            D.currency = "VEF"

            for d in data['response']['items']:
                D.amount += d.unit_price

            D.save()

            pf = PaymentMethodFields()
            pf.payment = D
            pf.key = "first_name"
            pf.value = data['response']['payer']['first_name']
            pf.save()
            
            pf = PaymentMethodFields()
            pf.payment = D
            pf.key = "last_name"
            pf.value = data['response']['payer']['last_name']
            pf.save()
            pf = PaymentMethodFields()
            pf.payment = D
            pf.key = "email"
            pf.value = data['response']['payer']['email']
            pf.save()

            o = Orders()
            o.status = "pending"
            o.payment_method = pf
            
            try:
                o.shipping_addresss = Addresess.objects.get(id=int(paymentInfo['response']['external_reference']['shipping_addresss_id']))
            except Addresess.DoesNotExist:
                pass
            try:
                o.billing_addresss = Addresess.objects.get(id=int(paymentInfo['response']['external_reference']['billing_addresss_id']))
            except Addresess.DoesNotExist:
                pass
            try:
                o.autor = User.objects.get(id=int(paymentInfo['response']['external_reference']['user_id']))
            except User.DoesNotExist:
                pass
            
            o.save()

            cart = Cart(paymentInfo['response']['external_reference']['cart_id'])

            for c in cart.items():
                os = OrderShippingItem()
                os.order =o
                os.product = c.product
                os.price = c.unit_price
                os.qty = c.quantity
                os.save()

#            payment_new.send(
#                sender=D.__class__, 
#                payment_method="MercadoPago",
#                cart_id=paymentInfo['response']['external_reference']['cart_id'],
#                user_id=paymentInfo['response']['external_reference']['user_id']
#            )

            

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes((AllowAny,))
def create_paypal_checkout(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    
    host = protocol +"://" + request.get_host()

    paypalrestsdk.configure({
      "mode": settings.PAYPAL_MODE,
      "client_id": settings.PAYPAL_CLIENT_ID,
      "client_secret": settings.PAYPAL_CLIENT_SECRET 
    })

    items = []
    cart = Cart(request)
    total = 0.00
    for c in cart.items():
        total += c.product.pricing
        items.append({
            "name": c.product.title,
            "sku": c.product.id,
            "quantity": 1,
            "currency": "USD",
            "price": c.product.pricing
        })

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": host + reverse("payment_sucesss"),
            "cancel_url": host + reverse("payment_cancel")
            },
        "transactions": [{
            "item_list": {
                "items": items 
            },
        "amount": {
            "total": total,
            "currency": "USD"
            },
        "description": "Buy Web Templates.",
        "custom":"user_id=%s&cart_id=%s&shipping_addresss_id=%s&billing_addresss_id=%s" % (
                request.user_site.id,
                cart.cart_id,
                request.session['shipping_address'],
                request.session['billing_address'],
            )
       
        }]
    })
    p = ""
    if payment.create():
        print payment.id
        for link in payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid google appengine unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                approval_url = str(link.href)
                p = approval_url
               
    else:
      print(payment.error)
    return Response(
      {'result':p} 
    )

@api_view(['POST'])
@permission_classes((AllowAny,))
def process_paypal(request):

    paypalrestsdk.configure({
      "mode": settings.PAYPAL_MODE,
      "client_id": settings.PAYPAL_CLIENT_ID,
      "client_secret": settings.PAYPAL_CLIENT_SECRET 
    })

    #payment = paypalrestsdk.Payment.find("PAY-69149887RN727922PLHEC5MY")

    #print payment
    return Response(status=status.HTTP_201_CREATED)
