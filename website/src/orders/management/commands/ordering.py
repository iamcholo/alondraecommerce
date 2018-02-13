from django.core.management import BaseCommand
from posts.models import PostItem
from payments.models import PaymentMethod
from orders.models import Orders,OrderShippingItem
from user_addresses.models import Addresess
from user.models import CustomUser as User

class Command(BaseCommand):
    help = 'check youtube videos'

    def handle(self, *args, **options):
        s = Addresess()
        s.autor = User.objects.get(id=1)
        s.city = "Montreal"
        s.country = "CA"
        s.zip_code = "2003"
        s.first_name = "mike"
        s.last_name = "thonson"
        s.address_line_1 = "montreal canada"
        s.address_line_2 = "Canada"
        s.address_type = "shipping"
        s.save()
        
        b = Addresess()
        b.autor = User.objects.get(id=1)
        b.city = "Montreal"
        b.country = "CA"
        b.zip_code = "2003"
        b.first_name = "mike"
        b.last_name = "thonson"
        b.address_line_1 = "montreal canada"
        b.address_line_2 = "Canada"
        b.address_type = "billing"
        b.save()

        p = PaymentMethod()
        p.first_name = "mike"
        p.last_name = "thonson"
        p.city = "FL"
        p.country = "US"
        p.amount = 100.00
        p.currency = "USD"
        p.email = "cocoaremix@gmail.com"
        p.payment_method = "paypal"
        p.save()
        
        for o in range(1,100):
            orders = Orders()
            orders.status = "approved"
            orders.autor = User.objects.get(id=1)
            orders.billing_addresss = b
            orders.shipping_addresss = b
            orders.payment_method = p
            orders.save()
            item = OrderShippingItem()
            item.order = orders
            item.product =PostItem.objects.get(id=1)
            item.price = 1.00
            item.qty = 15
            item.save()

        pass