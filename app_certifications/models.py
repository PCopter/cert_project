from django.db import models
from django.utils import timezone


# แต่ละประเทศจะมี จำนวนวันก่อนจะเปลี่ยนสถานะของใบอณุญาติแตกต่างกันไป
class Country(models.Model):
    name = models.CharField(max_length=255)
    caution_threshold = models.IntegerField(default=90)
    serious_threshold = models.IntegerField(default=60)
    critical_threshold = models.IntegerField(default=30)
    image_relative_url = models.CharField(max_length=255, default='default.jpg')
    def __str__(self):
        return self.name
    

# แต่ละประเทศจะประกอบด้วยใบอณุญาติที่หลากหลาย
class Certification(models.Model):
    country = models.ForeignKey(Country, related_name='certifications', on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=255 , null=False , default='Please enter the certificate name. ')
    # image_relative_url = models.CharField(max_length=255, default='default.jpg')
    def __str__(self):
        return '{} - {}'.format(self.country.name, self.certificate_name)


# IndoorModel
class IndoorModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

# OutdoorModel
class OutdoorModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

# สำหรับการจับคู่ระหว่าง indoor และ outdoor models
class IndoorOutdoorPair(models.Model):
    indoor_model = models.ForeignKey(IndoorModel, related_name='outdoor_pairs', on_delete=models.CASCADE)
    outdoor_model = models.ForeignKey(OutdoorModel, related_name='indoor_pairs', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.indoor_model.name, self.outdoor_model.name)
    

# โดยหมายเลขใบอณุญาติ(certificate_no) แต่ละหมายเลขจะมี สถานะ(status), วันออกใบอณุญาติ(issue_date), 
# วันหมดอายุ(expire_date),report_issue_date,report_noและรายชื่อของ indoor_models และ outdoor_modelsที่ครอบคลุมโดยรายชื่อนี้อาจมีมากกว่า 1
class CertificateNumber(models.Model):
    certification = models.ForeignKey(Certification, related_name='certificate_numbers', on_delete=models.CASCADE )
    certificate_no = models.CharField(max_length=255)
    issue_date = models.DateTimeField(null=True, blank=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    report_issue_date = models.DateTimeField(null=True, blank=True)
    report_no = models.CharField(max_length=255, null=True, blank=True)
    STATUS_CHOICES = (
        ('activating', 'Activating'),
        ('caution', 'Caution'),
        ('serious', 'Serious'),
        ('critical', 'Critical'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='activate')
    indoor_models = models.ManyToManyField(IndoorModel, related_name='certificate_numbers')
    outdoor_models = models.ManyToManyField(OutdoorModel, related_name='certificate_numbers')
    
    def update_status(self):
        current_date = timezone.localtime(timezone.now()).date()
        if self.expire_date:
            days_until_expiry = (self.expire_date.date() - current_date).days
        else:
            days_until_expiry = None

        if days_until_expiry is not None:
            if days_until_expiry > self.certification.country.caution_threshold:
                self.status = 'activating'
            elif days_until_expiry > self.certification.country.serious_threshold:
                self.status = 'caution'
            elif days_until_expiry > self.certification.country.critical_threshold:
                self.status = 'serious'
            else:
                self.status = 'critical'
        else:
            self.status = 'activating'


    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.certification.certificate_name, self.certificate_no)

