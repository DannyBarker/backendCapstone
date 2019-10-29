from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..connection import Connection
from capstone.models import Payment
from capstone.models import GiftCard
from capstone.models import Customer
from capstone.models import Company
import datetime



@login_required
def Donation_List(request):
    user = request.user
    current_customer = Customer.objects.get(pk=user.id)
    if request.method == 'GET':
        try:
            user_donations = current_customer.donations.all()
        except Payment.DoesNotExist:
            user_donations = []


        template_name = "donations/list.html"
        return render(request, template_name, {'all_donations': user_donations})

    elif request.method == 'POST':
        form_data = request.POST
        try:
            new_card = GiftCard.objects.get(company__id=form_data["company_card_name"], barcode=form_data["barcode"])

            new_payment = Payment.objects.create(
            payment_date=datetime.date.today(),
            customer=current_customer,
            giftcard=new_card,
            discription=form_data['description'],
            )
            return redirect(reverse('capstone:donations'))
        except GiftCard.DoesNotExist:
            companies = Company.objects.all()
            company_name = companies.get(pk=form_data["company_card_name"])
            messages.info(request, f"Could not find that card for {company_name.name}!")
            return render(request, "donations/form.html",{"form": form_data, "all_companies": companies})
