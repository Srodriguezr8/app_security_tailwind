

from django.shortcuts import render
from applications.core.models import Doctor
from applications.doctor.models import Atencion, DetalleAtencion


def obtener_atencion(request,pk):
    atencion = Atencion.objects.get(pk=pk)
    detalle = DetalleAtencion.objects.filter(atencion=atencion)
    prescripciones = [
    {
        'medicamento': item.medicamento.nombre,
        'concentracion': item.medicamento.concentracion,
        'via_administracion': item.medicamento.via_administracion,
        'cantidad': item.cantidad,
        'prescripcion': item.prescripcion,
        'duracion_tratamiento': item.duracion_tratamiento,
        'frecuencia': item.frecuencia_diaria,
    }
        for item in detalle
    ]
        

    doctor= Doctor.objects.first()
    context={
        'doctor': doctor.nombres.split()[0]+ " " +doctor.apellidos.split()[0],
        'especialidades': list(doctor.especialidad.all()),
        'direccion':doctor.direccion,
        'telefono': doctor.telefonos,
        'email': doctor.email,
        'firma': doctor.firma_digital,
        'logo': doctor.imagen_receta,
        'paciente':atencion.paciente.nombre_completo,
        'cedula':atencion.paciente.cedula_ecuatoriana,
        'dni':atencion.paciente.dni,
        'edad':atencion.paciente.edad,
        'fecha_atencion':atencion.fecha_atencion,
        'presion_arterial':atencion.presion_arterial,
        'pulso':atencion.pulso,
        'temperatura':atencion.temperatura,
        'peso':atencion.peso,
        'altura':atencion.altura,
        'diagnosticos':list(atencion.diagnostico.all()),
        'detalle_atencion':prescripciones


    }
    return render(request,'doctor/atenciones/receta.html',context=context)
