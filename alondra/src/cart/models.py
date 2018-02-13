from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.FloatField(
            verbose_name=_('unit price')
        )
    # product as generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price

    def the_unit_price(self):
        return "%0.2f" % self.unit_price

    the_unit_price = property(the_unit_price)
    
    def total_price_2(self):
        return "%0.2f" % self.total_price

    total_price = property(total_price)
    total_price_2 = property(total_price_2)
    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    def getAttributes(self):
        return ItemAttributes.objects.filter(item__id=self.id)
        
    product = property(get_product, set_product)

class ItemAttributes(models.Model):
    item = models.ForeignKey(Item, verbose_name=_('item'))
    # product as generic relation
    attribute_key = models.TextField(
            _('Attribute Key'), 
            max_length=255,
            blank=True,
            null=True
        )

    attribute_value = models.TextField(
            _('Attribute Value'),
            max_length=255,
            blank=True,
            null=True
        )

    class Meta:
        verbose_name = _('Item Attribute')
        verbose_name_plural = _('Item Attributes')
        ordering = ('item',)
        db_table = 'cart_item_attributes'

    def __unicode__(self):
        return u'%d units of %s' % (self.item.quantity, self.variant.__class__.__name__)
    
    def get_attributes(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

class AddressManager(models.Manager):
    def get(self, *args, **kwargs):

        if 'address' in kwargs:

            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['address']))
            kwargs['object_id'] = kwargs['address'].pk
            del(kwargs['address'])
        return super(AddressManager, self).get(*args, **kwargs)

class CartAddresses(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    objects = AddressManager()
    
    def get_address(self):
        return self.content_type.get_object_for_this_type(id=self.object_id)

    def set_address(self, address):
        self.content_type = ContentType.objects.get_for_model(type(address))
        self.object_id = address.pk

    address = property(get_address, set_address)

    class Meta:
        verbose_name = _('Cart Address')
        verbose_name_plural = _('Cart Addresses')
        ordering = ('cart',)
        db_table = 'cart_addresses'


class CartPaymentType(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))

    payment_type = models.TextField(
            _('Payment Type'), 
            max_length=10,
            blank=True,
            null=True
        )

    class Meta:
        verbose_name = _('Payment Type')
        verbose_name_plural = _('Payment Types')
        ordering = ('cart',)
        db_table = 'cart_payment_type'