from django.db import models
from sorl.thumbnail import ImageField


# Create your models here.

SPECIALIZATIONS = ((1, 'Bioteknologi'),
                (2, 'Organisk kjemi'),
                (3, 'Anvendt teoretisk kjemi'),
                (4, 'Analytisk kjemi'),
                (5, 'Kjemisk prosessteknologi'),
                (6, 'Materialkjemi og energiteknologi'))


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="corporate", verbose_name="Logo")
    #specializations = models.(choices=SPECIALIZATIONS)
