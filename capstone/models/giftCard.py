from django.core.validators import MinValueValidator
from django.db import models



class GiftCard(models.Model):

    barcode = models.CharField(max_length=20)
    inital_balance = models.IntegerField(validators=[MinValueValidator(0)],)
    remaining_balance = models.IntegerField(validators=[MinValueValidator(0)],)


    class Meta:
        verbose_name = ("giftcard")
        verbose_name_plural = ("giftcards")