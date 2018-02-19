from django.conf.urls import include, url
from payments.modules.skrill import views 
register_url = False
urlpatterns = [
 	url(r'^payment/skrill/checkout/{0,1}$', views.create_checkout),
    url(r'^payment/skrill/process/{0,1}$', views.process, name="payment_mercadopago_process"),
   
]






