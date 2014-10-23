# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(default=b'', max_length=256)),
                ('position', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(default=b'', max_length=256)),
                ('description', models.TextField(default=b'', blank=True)),
                ('category', models.ForeignKey(to='healthhabitplan.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Magnet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('item', models.ForeignKey(to='healthhabitplan.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('saved', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user', 'saved'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='magnet',
            name='session',
            field=models.ForeignKey(to='healthhabitplan.Session'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='item',
            order_with_respect_to='category',
        ),
    ]
