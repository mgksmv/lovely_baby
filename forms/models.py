from django.db import models


class CommercialProposalRequest(models.Model):
    name = models.CharField('Имя или название компании', max_length=200)
    contact = models.CharField('Номер или Email', max_length=64)
    date_created = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'заявка на коммерческое предложение'
        verbose_name_plural = 'Заявки на коммерческое предложение'
