# Generated by Django 2.2.5 on 2020-04-14 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='Band',
        ),
        migrations.RenameField(
            model_name='membership',
            old_name='group',
            new_name='band',
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('type', models.CharField(choices=[('RE', 'Recruitment Member'), ('JO', 'Join a Group'), ('SU', 'Support')], max_length=30)),
                ('prefecture', models.IntegerField(choices=[(1, 'Hokkaido'), (2, 'Aomori Prefecture'), (3, 'Iwate Prefecture'), (4, 'Miyagi Prefecture'), (5, 'Akita Prefecture'), (6, 'Yamagata Prefecture'), (7, 'Fukushima Prefecture'), (8, 'Ibaraki Prefecture'), (9, 'Tochigi Prefecture'), (10, 'Gunma Prefecture'), (11, 'Saitama Prefecture'), (12, 'Chiba Prefecture'), (13, 'Tokyo Prefecture'), (14, 'Kanagawa Prefecture'), (15, 'Niigata Prefecture'), (16, 'Toyama Prefecture'), (17, 'Ishikawa Prefecture'), (18, 'Fukui Prefecture'), (19, 'Yamanashi Prefecture'), (20, 'Nagano Prefecture'), (21, 'Gifu Prefecture'), (22, 'Shizuoka Prefecture'), (23, 'Aichi Prefecture'), (24, 'Mie Prefecture'), (25, 'Shiga Prefecture'), (26, 'Kyoto Prefecture'), (27, 'Osaka Prefecture'), (28, 'Hyogo Prefecture'), (29, 'Nara Prefecture'), (30, 'Wakayama Prefecture'), (31, 'Tottori Prefecture'), (32, 'Shimane Prefecture'), (33, 'Okayama Prefecture'), (34, 'Hiroshima Prefecture'), (35, 'Yamaguchi Prefecture'), (36, 'Tokushima Prefecture'), (37, 'Kagawa Prefecture'), (38, 'Ehime Prefecture'), (39, 'Kochi Prefecture'), (40, 'Fukuoka Prefecture'), (41, 'Saga Prefecture'), (42, 'Nagasaki Prefecture'), (43, 'Kumamoto Prefecture'), (44, 'Oita Prefecture'), (45, 'Miyazaki Prefecture'), (46, 'Kagoshima Prefecture'), (47, 'Okinawa Prefecture')])),
                ('area', models.CharField(blank=True, max_length=20, null=True, verbose_name='Area')),
                ('day_week', models.CharField(choices=[('WD', 'Weekdays'), ('WE', 'Weekends'), ('AL', 'Always')], max_length=20)),
                ('direction', models.CharField(choices=[('OR', 'Original'), ('CO', 'Copy'), ('AL', 'All')], max_length=20)),
                ('part', models.TextField(verbose_name='Part')),
                ('genre', models.TextField(verbose_name='Genre')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]