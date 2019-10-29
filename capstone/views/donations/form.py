from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from capstone.models import Company

@login_required
def Donation_Form(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        template = 'donations/form.html'
        context = {
            'all_companies': companies
        }

        return render(request, template, context)