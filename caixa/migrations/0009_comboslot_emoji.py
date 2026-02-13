# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0008_criar_categoria_combo'),
    ]

    operations = [
        migrations.AddField(
            model_name='comboslot',
            name='emoji',
            field=models.CharField(default='📋', help_text='Emoji do slot', max_length=10),
        ),
    ]
