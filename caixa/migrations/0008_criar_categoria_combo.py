# Generated migration for creating Combo category

from django.db import migrations


def criar_categoria_combo(apps, schema_editor):
    """Cria a categoria 'Combo' para todas as empresas"""
    Empresa = apps.get_model('authentication', 'Empresa')
    Categoria = apps.get_model('caixa', 'Categoria')
    
    for empresa in Empresa.objects.all():
        # Verificar se já existe categoria Combo para esta empresa
        if not Categoria.objects.filter(empresa=empresa, nome='Combo').exists():
            Categoria.objects.create(
                empresa=empresa,
                nome='Combo',
                emoji='🎁',
                descricao='Categoria especial para produtos do tipo combo',
                ativo=True,
                is_sistema=True
            )


def reverter_categoria_combo(apps, schema_editor):
    """Remove a categoria 'Combo' de todas as empresas"""
    Categoria = apps.get_model('caixa', 'Categoria')
    Categoria.objects.filter(nome='Combo', is_sistema=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0007_categoria_is_sistema'),
    ]

    operations = [
        migrations.RunPython(criar_categoria_combo, reverter_categoria_combo),
    ]
