from django.conf.urls import include, url
from payments.modules.mercado_pago_paypal import rest_api as views 
register_url = True
urlpatterns = [
 	url(r'^payment/mercadopago/checkout/{0,1}$', views.create_mercadopago_checkout),
    url(r'^payment/mercadopago/process/{0,1}$', views.process_mercadopago, name="payment_mercadopago_process"),
    url(r'^payment/paypal/checkout/{0,1}$', views.create_paypal_checkout),
]






