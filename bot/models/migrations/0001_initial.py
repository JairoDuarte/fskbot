# Generated by Django 2.0.6 on 2018-06-17 18:14

import chatterbot.conversation.statement
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time that this response was created at.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400, unique=True)),
                ('extra_data', models.CharField(blank=True, max_length=500)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, chatterbot.conversation.statement.StatementMixin),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('statements', models.ManyToManyField(related_name='tags', to='models.Statement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='response',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='models.Statement'),
        ),
        migrations.AddField(
            model_name='response',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_response', to='models.Statement'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='responses',
            field=models.ManyToManyField(help_text='The responses in this conversation.', related_name='conversations', to='models.Response'),
        ),
    ]