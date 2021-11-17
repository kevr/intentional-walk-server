# Generated by Django 3.2.9 on 2021-12-22 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_new_demographic_cols'),
    ]

    operations = [
        # Small edit to help text
        migrations.AlterField(
            model_name='dailywalk',
            name='date',
            field=models.DateField(help_text='The specific date for which the steps are recorded'),
        ),
        # Remove many-to-many relationship to Race table (we delete and recreate below as many-to-one)
        migrations.RemoveField(
            model_name='account',
            name='race',
        ),
        migrations.AddField(
            model_name='account',
            name='race_other',
            field=models.CharField(blank=True, help_text="Free-form text field for 'race' value 'OT'", max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(blank=True, help_text='Self-identified gender identity of user', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='gender_other',
            field=models.CharField(blank=True, help_text="Free-form text field for 'gender' value 'OT'", max_length=75, null=True),
        ),
        migrations.DeleteModel(
            name='Race',
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='race',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.account'),
        ),
    ]
