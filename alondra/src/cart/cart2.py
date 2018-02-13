import datetime
import models
from django.db.models import Count   

CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    def __init__(self, request, cart_id=None):
        self.cart_id = request.session.get(cart_id or CART_ID)
        if self.cart_id:
            try:
                cart = models.Cart.objects.get(id=self.cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item
    def items(self):
        return self.cart.item_set.all()
    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, unit_price, quantity=1, meta_list=[], batch=False):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
            if batch == False:
                self.save_item_attr( item, meta_list)
        else:
            raise ItemAlreadyExists

    def add_2(self, products=[], quantity=1):
        for product in products:            
            item = self.check_if_item_exits(product)
            if item is None:
                item = self.create_product(product,quantity)
            if product.has_key("variant"):
            #create a normal product
                self.add_variant( item, product['variant'])

    def create_product(self, product,quantity):
        item = models.Item()
        item.cart = self.cart
        item.product = product['product']
        item.unit_price = product['product'].getFinalPrice()
        item.quantity = quantity
        item.save()
        return item

    def check_if_item_exits(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product['product'],
                unit_price=product['product'].getFinalPrice(),
            )
            return item
        except models.Item.DoesNotExist:
            pass
        return None

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def count_attributes(self, item, variant):
        name= variant.attribute.name
        value= variant.value
        return len(models.ItemAttributes.objects.filter(
                item__id = item.id,
                attribute_key = name,
                attribute_value = value,    
            ).annotate(count=Count("attribute_value")))

    def add_variant(self,item, variant):
        name = variant.attribute.name
        value = variant.value
        models.ItemAttributes.objects.filter(
                item__id = item.id,
                attribute_key = name,
                attribute_value = value,    
            ).delete()
        item_attribute = models.ItemAttributes()
        item_attribute.item = item
        item_attribute.attribute_key = name
        item_attribute.attribute_value = value
        item_attribute.save()

    def save_item_attr(self, item, meta_list):
        #models.ItemAttributes.objects.filter(item__id=item.id).delete()
        if len(meta_list) > 0:
            for meta in meta_list:              
                item_attribute = models.ItemAttributes()
                item_attribute.item = item
                item_attribute.attribute_key = meta['parent_name']
                item_attribute.attribute_value = meta['item_value']
                item_attribute.save()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            item.quantity = quantity
            item.unit_price = unit_price
            item.save()

        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def update_qty(self, products=[]):
        for product in products:
            #item = self.check_if_item_exits(product)
            if product['item'] is not None:
                product['item'].quantity = product['quantity']
                product['item'].save()

    def currentProductQty(self,product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )            
            return item.quantity
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def check_address_if_item_exits(self, address):
        try:
            item = models.CartAddresses.objects.get(
                cart=self.cart,
                address=address
            )
            return item
        except models.CartAddresses.DoesNotExist:
            pass
        return None

    def create_address(self, address):

        item = models.CartAddresses()
        item.cart = self.cart
        item.address = address
        item.save()
        return item

    def create_payment_type(self, payment_method):
        models.CartPaymentType.objects.filter(cart=self.cart).delete()
        payment_type = models.CartPaymentType()
        payment_type.cart = self.cart
        payment_type.payment_type = payment_method
        payment_type.save()
        return payment_type
    
    def get_payment_type(self):
        payment_type = models.CartPaymentType.objects.filter(cart=self.cart)
        if len(payment_type) > 0:
            return payment_type[0].payment_type
        return None

    def add_addresses(self, addresses=[]):
        for address in addresses:            
            item = self.check_address_if_item_exits(address)
            if item is None:
                item = self.create_address(address)

    def get_addresses(self):
        return models.CartAddresses.objects.filter(cart=self.cart)

    def address_remove(self, address):
        try:
            address = models.CartAddresses.objects.get(
                cart=self.cart,
                address=address,
            )
        except models.CartAddresses.DoesNotExist:
            raise ItemDoesNotExist
        else:
            address.delete()
    
    def clear(self):
        for item in self.cart.item_set.all():
            models.ItemAttributes.objects.filter(item__id=item.id).delete()
        
        self.cart.item_set.all().delete()
        self.cart.cartaddresses_set.all().delete()
       

    def count(self):
        return int(sum(1 for _ in self))

    def checked_out(self,checked_out=True):
        models.Cart.objects.filter(pk=self.cart_id).update(checked_out=checked_out)


class Cart2:
    def __init__(self, cart_id=None): 
        self.cart_id = cart_id      
        if self.cart_id:
            try:
                cart = models.Cart.objects.get(id=self.cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item
    def items(self):
        return self.cart.item_set.all()

    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, unit_price, quantity=1, meta_list=[], batch=False):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
            if batch == False:
                self.save_item_attr( item, meta_list)
        else:
            raise ItemAlreadyExists

    def add_2(self, products=[], quantity=1):
        for product in products:            
            item = self.check_if_item_exits(product)
            if item is None:
                item = self.create_product(product,quantity)
            if product.has_key("variant"):
            #create a normal product
                self.add_variant( item, product['variant'])

    def create_product(self, product,quantity):
        item = models.Item()
        item.cart = self.cart
        item.product = product['product']
        item.unit_price = product['product'].getFinalPrice()
        item.quantity = quantity
        item.save()
        return item

    def check_if_item_exits(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product['product'],
                unit_price=product['product'].getFinalPrice(),
            )
            return item
        except models.Item.DoesNotExist:
            pass
        return None

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def count_attributes(self, item, variant):
        name= variant.attribute.name
        value= variant.value
        return len(models.ItemAttributes.objects.filter(
                item__id = item.id,
                attribute_key = name,
                attribute_value = value,    
            ).annotate(count=Count("attribute_value")))

    def add_variant(self,item, variant):
        name = variant.attribute.name
        value = variant.value
        models.ItemAttributes.objects.filter(
                item__id = item.id,
                attribute_key = name,
                attribute_value = value,    
            ).delete()
        item_attribute = models.ItemAttributes()
        item_attribute.item = item
        item_attribute.attribute_key = name
        item_attribute.attribute_value = value
        item_attribute.save()

    def save_item_attr(self, item, meta_list):
        #models.ItemAttributes.objects.filter(item__id=item.id).delete()
        if len(meta_list) > 0:
            for meta in meta_list:              
                item_attribute = models.ItemAttributes()
                item_attribute.item = item
                item_attribute.attribute_key = meta['parent_name']
                item_attribute.attribute_value = meta['item_value']
                item_attribute.save()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            item.quantity = quantity
            item.unit_price = unit_price
            item.save()

        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def update_qty(self, products=[]):
        for product in products:
            #item = self.check_if_item_exits(product)
            if product['item'] is not None:
                product['item'].quantity = product['quantity']
                product['item'].save()

    def currentProductQty(self,product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )            
            return item.quantity
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def check_address_if_item_exits(self, address):
        try:
            item = models.CartAddresses.objects.get(
                cart=self.cart,
                address=address
            )
            return item
        except models.CartAddresses.DoesNotExist:
            pass
        return None

    def create_address(self, address):

        item = models.CartAddresses()
        item.cart = self.cart
        item.address = address
        item.save()
        return item

    def create_payment_type(self, payment_method):
        models.CartPaymentType.objects.filter(cart=self.cart).delete()
        payment_type = models.CartPaymentType()
        payment_type.cart = self.cart
        payment_type.payment_type = payment_method
        payment_type.save()
        return payment_type
    
    def get_payment_type(self):
        payment_type = models.CartPaymentType.objects.filter(cart=self.cart)
        if len(payment_type) > 0:
            return payment_type[0].payment_type
        return None

    def add_addresses(self, addresses=[]):
        for address in addresses:            
            item = self.check_address_if_item_exits(address)
            if item is None:
                item = self.create_address(address)

    def get_addresses(self):
        return models.CartAddresses.objects.filter(cart=self.cart)

    def address_remove(self, address):
        try:
            address = models.CartAddresses.objects.get(
                cart=self.cart,
                address=address,
            )
        except models.CartAddresses.DoesNotExist:
            raise ItemDoesNotExist
        else:
            address.delete()
    
    def clear(self):
        for item in self.cart.item_set.all():
            models.ItemAttributes.objects.filter(item__id=item.id).delete()
        
        self.cart.item_set.all().delete()
        self.cart.cartaddresses_set.all().delete()
       

    def count(self):
        return int(sum(1 for _ in self))

    def checked_out(self,checked_out=True):
        models.Cart.objects.filter(pk=self.cart_id).update(checked_out=checked_out)
