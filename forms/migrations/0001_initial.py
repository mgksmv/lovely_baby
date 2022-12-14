# Generated by Django 4.1.1 on 2022-09-11 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialProposalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя или название компании')),
                ('contact', models.CharField(max_length=64, verbose_name='Номер или Email')),
            ],
            options={
                'verbose_name': 'заявка на коммерческое предложение',
                'verbose_name_plural': 'Заявки на коммерческое предложение',
            },
        ),
    ]
