from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from app_certifications.models import Country, Certification, CertificateNumber
from django.urls import reverse
from .models import Subscription
from app_general.forms import SubscriptionForm , SubscriptionModelForm
from django.http import HttpRequest
# Create your views here.


def home(request):
    country_count = Country.objects.count()
    certification_count = Certification.objects.count()
    certificate_number_count = CertificateNumber.objects.count()

    certificate_numbers_activate = CertificateNumber.objects.filter(status='activate').count()
    certificate_numbers_risk = CertificateNumber.objects.filter(status='risk').count()
    certificate_numbers_alert = CertificateNumber.objects.filter(status='alert').count()

    context = {
        'country_count': country_count,
        'certification_count': certification_count,
        'certificate_number_count': certificate_number_count,
        'certificate_numbers_activate': certificate_numbers_activate,
        'certificate_numbers_risk': certificate_numbers_risk,
        'certificate_numbers_alert': certificate_numbers_alert,
    }
    
    return render(request, 'app_general/home.html', context)
  

# def certifications_by_country(request, country):
#     certifications = Certification.objects.filter(country=country)
#     return render(request, 'app_general/certifications_by_country.html', {'certifications': certifications, 'country': country})



def about(request : HttpRequest):
    return render(request , 'app_general/about.html')

def subscription(request : HttpRequest):
    if request.method == 'POST':
        form = SubscriptionModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('subscription_thankyou'))
    else:
        form = SubscriptionModelForm()
    context = {'form' : form}
    return render(request , 'app_general/subscription_form.html',context)

def subscription_thankyou(request : HttpRequest):
    return render(request,'app_general/subscription_thankyou.html')




