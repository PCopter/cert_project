from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Country, Certification, CertificateNumber

# view สำหรับแสดงรายชื่อประเทศ Country พร้อมทั้งจำนวน Certification ของประเทศนั้นๆ
def country_list(request):
    query = request.GET.get('q')
    countries = Country.objects.all()
    
    if query:
        countries = countries.filter(name__icontains=query)

    for country in countries:
        count = Certification.objects.filter(country=country).count()
        country.certification_count = count

    return render(request, 'app_certifications/country_list.html', {'countries': countries})

# view สำหรับแสดงใบอณุญาติ Certification พร้อมทั้งจำนวน CertificateNumber ภายใต้ Certification นั้นๆ
def certification_list(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    certifications = Certification.objects.filter(country=country)

    for certification in certifications:
        certification.certificate_number_count = certification.certificate_numbers.count()

    context = {
        'country': country,
        'certifications': certifications,
    }
    return render(request, 'app_certifications/certification_list.html', context)

# ฟังก์ชันสำหรับการอัปเดตสถานะของ certificate numbers ทั้งหมด
def update_all_certificate_numbers():
    certificate_numbers = CertificateNumber.objects.all()
    for certificate_number in certificate_numbers:
        old_status = certificate_number.status
        certificate_number.update_status()
        if old_status != certificate_number.status:
            certificate_number.save()

# view สำหรับการแสดงใบอนุญาตทั้งหมด โดยรวมถึงจำนวนใบอนุญาตในแต่ละสถานะ
def certifications(request):
    query = request.GET.get('q')
    all_certifications = Certification.objects.all()
    update_all_certificate_numbers()
    
    activating_count = CertificateNumber.objects.filter(status='activating').count()
    caution_count = CertificateNumber.objects.filter(status='caution').count()
    serious_count = CertificateNumber.objects.filter(status='serious').count()
    critical_count = CertificateNumber.objects.filter(status='critical').count()

    certifications_with_expiry = []
    for certification in all_certifications:
        certificate_numbers = certification.certificate_numbers.all()
        for certificate_number in certificate_numbers:
            expire_date = certificate_number.expire_date
            if expire_date:
                current_time = timezone.now()
                expire_date = timezone.make_aware(expire_date) if timezone.is_naive(expire_date) else expire_date
                days_until_expiry = (expire_date - current_time).days
            else:
                days_until_expiry = None

            certifications_with_expiry.append({
                'certification': certification,
                'certificate_number': certificate_number,
                'days_until_expiry': days_until_expiry,
            })

    context = {
        'certifications_with_expiry': certifications_with_expiry,
        'activating_count': activating_count,
        'caution_count': caution_count,
        'serious_count': serious_count,
        'critical_count': critical_count,
    }
    return render(request, 'app_certifications/certifications.html', context)

# view สำหรับการแสดงข้อมูลของใบอนุญาตเดี่ยว (Certification) รวมถึงหมายเลขใบอนุญาต (CertificateNumber) ที่เกี่ยวข้อง
def certification(request, cert_id):
    one_certification = get_object_or_404(Certification, id=cert_id)
    certificate_numbers = one_certification.certificate_numbers.all()

    certifications_with_expiry = []
    current_time = timezone.now()
    for certificate_number in certificate_numbers:
        expire_date = certificate_number.expire_date
        if expire_date:
            expire_date = timezone.make_aware(expire_date) if timezone.is_naive(expire_date) else expire_date
            days_until_expiry = (expire_date - current_time).days
        else:
            days_until_expiry = None

        certifications_with_expiry.append({
            'certificate_number': certificate_number,
            'days_until_expiry': days_until_expiry,
        })

    context = {
        'certification': one_certification,
        'certifications_with_expiry': certifications_with_expiry,
    }
    return render(request, 'app_certifications/certification.html', context)

# view สำหรับการแสดงใบอนุญาตในแต่ละประเทศ โดยรวมถึงจำนวนใบอนุญาตในแต่ละสถานะสำหรับประเทศนั้นๆ
def certifications_by_country(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    certifications = Certification.objects.filter(country=country)
    update_all_certificate_numbers()

    activating_count = CertificateNumber.objects.filter(certification__country=country, status='activating').count()
    caution_count = CertificateNumber.objects.filter(certification__country=country, status='caution').count()
    serious_count = CertificateNumber.objects.filter(certification__country=country, status='serious').count()
    critical_count = CertificateNumber.objects.filter(certification__country=country, status='critical').count()

    certifications_with_expiry = []
    current_time = timezone.now()
    for certification in certifications:
        certificate_numbers = certification.certificate_numbers.all()
        for certificate_number in certificate_numbers:
            expire_date = certificate_number.expire_date
            if expire_date:
                expire_date = timezone.make_aware(expire_date) if timezone.is_naive(expire_date) else expire_date
                days_until_expiry = (expire_date - current_time).days
            else:
                days_until_expiry = None

            certifications_with_expiry.append({
                'certification': certification,
                'certificate_number': certificate_number,
                'days_until_expiry': days_until_expiry,
            })

    context = {
        'certifications_with_expiry': certifications_with_expiry,
        'country': country,
        'activating_count': activating_count,
        'caution_count': caution_count,
        'serious_count': serious_count,
        'critical_count': critical_count,
    }

    return render(request, 'app_certifications/certifications_by_country.html', context)

# view สำหรับการแสดงรายการใบอนุญาตทั้งหมด รวมถึงประเทศ, certification, และสถานะต่างๆ
def listview(request):
    countries = Country.objects.all()
    update_all_certificate_numbers()
    certification_numbers = CertificateNumber.objects.select_related('certification__country').all()

    certifications = Certification.objects.values_list('certificate_name', flat=True).distinct()
    statuses = CertificateNumber.objects.values_list('status', flat=True).distinct()

    today = timezone.now().date()
    for cert_no in certification_numbers:
        if cert_no.expire_date:
            cert_no.days_until_expiry = (cert_no.expire_date.date() - today).days
        else:
            cert_no.days_until_expiry = 'N/A'

    # Calculate counts for each country
    country_data = []
    for country in countries:
        total_count = certification_numbers.filter(certification__country=country).count()
        activating_count = certification_numbers.filter(certification__country=country, status='activating').count()
        caution_count = certification_numbers.filter(certification__country=country, status='caution').count()
        serious_count = certification_numbers.filter(certification__country=country, status='serious').count()
        critical_count = certification_numbers.filter(certification__country=country, status='critical').count()
        
        country_data.append({
            'country': country,
            'total_count': total_count,
            'activating_count': activating_count,
            'caution_count': caution_count,
            'serious_count': serious_count,
            'critical_count': critical_count,
        })

    context = {
        'countries': countries,
        'certification_numbers': certification_numbers,
        'certifications': certifications,
        'statuses': statuses,
        'country_data': country_data,
    }

    return render(request, 'app_certifications/listview.html', context)
