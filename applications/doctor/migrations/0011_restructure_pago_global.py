# Generated migration for restructuring Pago_global model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0010_add_referencia_externa_to_pago_global'),
    ]

    operations = [
        # Primero agregar los nuevos campos
        migrations.AddField(
            model_name='pago_global',
            name='atencion',
            field=models.ForeignKey(
                default=1,  # Temporal, se actualizará después
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pagos_globales',
                to='doctor.atencion',
                verbose_name='Atención Médica',
                help_text='Atención médica asociada a este pago.'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago_global',
            name='paciente_nombre',
            field=models.CharField(
                default='',
                max_length=200,
                verbose_name='Nombre del Paciente',
                help_text='Nombre completo del paciente al momento del pago.'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago_global',
            name='paciente_identificacion',
            field=models.CharField(
                default='',
                max_length=20,
                verbose_name='Identificación del Paciente',
                help_text='Número de identificación del paciente.'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pago_global',
            name='paciente_email',
            field=models.EmailField(
                blank=True,
                max_length=254,
                null=True,
                verbose_name='Email del Paciente',
                help_text='Email del paciente para envío de comprobantes.'
            ),
        ),
        migrations.AddField(
            model_name='pago_global',
            name='paciente_telefono',
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                verbose_name='Teléfono del Paciente',
                help_text='Teléfono del paciente para contacto.'
            ),
        ),
        
        # Renombrar campos existentes
        migrations.RenameField(
            model_name='pago_global',
            old_name='fecha_procesamiento',
            new_name='fecha_pago',
        ),
        migrations.RenameField(
            model_name='pago_global',
            old_name='metodo_pago_modal',
            new_name='metodo_pago',
        ),
        migrations.RenameField(
            model_name='pago_global',
            old_name='monto_procesado',
            new_name='monto_total',
        ),
        migrations.RenameField(
            model_name='pago_global',
            old_name='estado_procesamiento',
            new_name='estado',
        ),
        migrations.RenameField(
            model_name='pago_global',
            old_name='observaciones_procesamiento',
            new_name='observaciones',
        ),
        
        # Actualizar choices del campo estado
        migrations.AlterField(
            model_name='pago_global',
            name='estado',
            field=models.CharField(
                choices=[
                    ('pagado', 'Pagado'),
                    ('pendiente', 'Pendiente'),
                    ('parcial', 'Parcial'),
                    ('cancelado', 'Cancelado'),
                    ('reembolsado', 'Reembolsado'),
                ],
                default='pagado',
                max_length=20,
                verbose_name='Estado del Pago'
            ),
        ),
        
        # Remover campos obsoletos
        migrations.RemoveField(
            model_name='pago_global',
            name='detalle_pago',
        ),
        migrations.RemoveField(
            model_name='pago_global',
            name='usuario_procesamiento',
        ),
        
        # Agregar índices
        migrations.AddIndex(
            model_name='pago_global',
            index=models.Index(fields=['atencion', 'estado'], name='idx_atencion_estado'),
        ),
        migrations.AddIndex(
            model_name='pago_global',
            index=models.Index(fields=['fecha_pago'], name='idx_fecha_pago'),
        ),
    ]
