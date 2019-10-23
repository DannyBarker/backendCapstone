from django.db import models
from django.core.validators import MinValueValidator
from .customer import Customer
from .company import Company
from .giftCard import GiftCard

class Payment(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="donations")
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name="payments")
    giftcard = models.OneToOneField(GiftCard, on_delete=models.DO_NOTHING,)
    amount =  models.IntegerField(validators=[MinValueValidator(0)],)
    payment_date = models.DateField(default="0000-00-00",)

    class Meta:
        verbose_name = ("payment")
        verbose_name_plural = ("payments")
