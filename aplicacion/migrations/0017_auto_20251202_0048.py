from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0016_alter_fruta_options_fruta_imagen_and_more'),  # Ajusta según tu última migración aplicada
    ]

    operations = [
        # Ejemplo: agregar un nuevo campo
      
        # Ejemplo: modificar un campo existente
        migrations.AddField(
            model_name='pedido',
            name='tipo_envio',
            field=models.CharField(choices=[('Nacional', 'Nacional'), ('Internacional', 'Internacional')], default='Nacional', max_length=15, verbose_name='Tipo de Envío'),  # permite valores nulos si antes no los permitía
        ),
    ]