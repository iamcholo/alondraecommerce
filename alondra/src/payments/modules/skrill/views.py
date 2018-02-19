from django.db.models import Q
from django.http import HttpResponse
import urllib

def create_checkout(request, slug=None, page=1, model=None):
        url = "https://www.skrill.com/app/payment.pl";
        data = {
            'pay_to_email':'demoqco@sun-fish.com',
            'transaction_id':"ASDASDAEEDF",#cambiar esto
            'return_url':'/payment/cancel/',
            'return_url_text':'Volver a la plataforma',
            'return_url_target':2,
            'cancel_url':'/payment/cancel/',
            'status_url':'/payment/process/',
            'amount': 50,
            'language':"ES",
            'currency':"USD",
        }
        post = urllib.urlencode(data)
        b = StringIO.StringIO()
        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, url)
        ch.setopt(pycurl.FOLLOWLOCATION, True)
        ch.setopt(pycurl.HEADER, True)
        ch.setopt(pycurl.VERBOSE, False)
        ch.setopt(pycurl.POST, True)
        ch.setopt(pycurl.WRITEFUNCTION, b.write)
        ch.setopt(pycurl.POSTFIELDS, post)

        ch.perform()
        ch.close()
   
    return HttpResponse("")

def process(request, slug=None, model=None):
#    pay_to_email = $request->input('pay_to_email');// quien recive el pago en este caso yaraujo@outlook.com
#    pay_from_email  = $request->input('pay_from_email');// quien nos envia el pago
#    customer_id  = $request->input('customer_id');// id de quien nos envia el pago
#    transaction_id  = $request->input('transaction_id');
#    amount  = $request->input('amount');
#    status  = $request->input('status'); //Status of the transaction: -2 Fallido  / 2 procesado/ 0 pendiente / -1 cancelado
#    mb_amount  = $request->input('mb_amount'); // cuanto te llego a tu cuenta descontando los fee de skrill
#    currency  = $request->input('currency');
#    neteller_id  = $request->input('neteller_id'); // en el caso de haber usado neteller te devuelve el id de la cuenta
#    payment_type  = $request->input('payment_type'); // tipo de pago que usuario realizo tarjeta de debito,neteller,etc..
#    merchant_fields  = $request->input('merchant_fields'); // tipo de pago que usuario realizo tarjeta de debito,neteller,etc..
#    if(status == 2)
#    {
#        //procesar pago
#    }    
   
   
    return HttpResponse("")
