# Generated by Django 3.0.7 on 2020-09-25 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickServiceVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_num', models.CharField(db_index=True, max_length=32, verbose_name='车牌号码')),
                ('wip', models.CharField(db_index=True, max_length=32, verbose_name='工单号')),
                ('quick_service_team', models.CharField(blank=True, max_length=32, null=True, verbose_name='快修班组')),
                ('oil_service', models.CharField(max_length=10, verbose_name='机油保养')),
                ('quick_service_status', models.CharField(db_index=True, default='正在维修', max_length=32, verbose_name='维修状态')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='开始日期')),
                ('finish_time', models.DateTimeField(auto_now=True, verbose_name='完工时间')),
            ],
            options={
                'verbose_name': '快修车辆信息表',
                'verbose_name_plural': '快修车辆信息表',
            },
        ),
        migrations.CreateModel(
            name='ServiceVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_num', models.CharField(db_index=True, max_length=32, verbose_name='车牌号码')),
                ('wip', models.CharField(db_index=True, max_length=32, verbose_name='工单号')),
                ('service_team', models.CharField(blank=True, max_length=32, null=True, verbose_name='机电班组')),
                ('service_status', models.CharField(db_index=True, default='正在维修', max_length=32, verbose_name='维修状态')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='开始日期')),
                ('finish_time', models.DateTimeField(auto_now=True, verbose_name='完工时间')),
            ],
            options={
                'verbose_name': '机电车辆信息表',
                'verbose_name_plural': '机电车辆信息表',
            },
        ),
        migrations.AddField(
            model_name='vehicleinfo',
            name='quick_service_status',
            field=models.CharField(default='正在维修', max_length=32, verbose_name='快修维修状态'),
        ),
        migrations.AlterField(
            model_name='vehicleinfo',
            name='service_status',
            field=models.CharField(default='正在维修', max_length=32, verbose_name='机电维修状态'),
        ),
        migrations.AlterField(
            model_name='vehicleinfo',
            name='vehicle_num',
            field=models.CharField(db_index=True, max_length=20, verbose_name='车牌号码'),
        ),
        migrations.AlterField(
            model_name='vehicleinfo',
            name='wip',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True, verbose_name='工单号码'),
        ),
    ]
