from django.contrib import admin
from .models import (
    HorarioAtencion,
    CitaMedica,
    Atencion,
    DetalleAtencion,
    ServiciosAdicionales,
    Pago,
    DetallePago,
    Pago_global
)


@admin.register(HorarioAtencion)
class HorarioAtencionAdmin(admin.ModelAdmin):
    list_display = ("dia_semana", "hora_inicio", "hora_fin", "activo")
    list_filter = ("dia_semana", "activo")



@admin.register(CitaMedica)
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ("paciente","fecha", "hora_cita", "estado")
    list_filter = ("estado", "fecha")
    search_fields = ("paciente__nombres", "paciente__apellidos", "doctor__nombres", "doctor__apellidos")


class DetalleAtencionInline(admin.TabularInline):
    model = DetalleAtencion
    extra = 0


@admin.register(Atencion)
class AtencionAdmin(admin.ModelAdmin):
    list_display = ("paciente", "fecha_atencion", "es_control")
    list_filter = ("fecha_atencion", "es_control")
    search_fields = ("paciente__nombres", "paciente__apellidos")
    inlines = [DetalleAtencionInline]


@admin.register(ServiciosAdicionales)
class ServiciosAdicionalesAdmin(admin.ModelAdmin):
    list_display = ("nombre_servicio", "costo_servicio", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre_servicio",)


class DetallePagoInline(admin.TabularInline):
    model = DetallePago
    extra = 0


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "atencion", "monto_total", "estado", "metodo_pago", "fecha_pago", "fecha_creacion")
    list_filter = ("estado", "metodo_pago", "fecha_creacion")
    search_fields = ("atencion__paciente__nombres", "atencion__paciente__apellidos", "nombre_pagador")
    inlines = [DetallePagoInline]


@admin.register(DetallePago)
class DetallePagoAdmin(admin.ModelAdmin):
    list_display = (
        "pago", "servicio_adicional", "cantidad", "precio_unitario", "aplica_seguro", "valor_seguro", "subtotal"
    )
    list_filter = ("aplica_seguro", "servicio_adicional")
    search_fields = ("pago__atencion__paciente__nombres", "pago__atencion__paciente__apellidos")


@admin.register(Pago_global)
class PagoGlobalAdmin(admin.ModelAdmin):
    list_display = (
        "id", "get_paciente_nombre", "get_metodo_pago", "get_monto_total", 
        "get_estado", "get_fecha_pago"
    )
    list_filter = ("pago__estado", "pago__metodo_pago", "pago__fecha_pago")
    search_fields = (
        "pago__atencion__paciente__nombres", 
        "pago__atencion__paciente__apellidos",
        "pago__atencion__paciente__cedula_ecuatoriana"
    )
    readonly_fields = ("get_paciente_nombre", "get_paciente_identificacion", "get_fecha_pago", "get_estado", "get_metodo_pago", "get_monto_total")
    
    fieldsets = (
        ("Información del Pago", {
            "fields": ("pago",)
        }),
        ("Datos del Paciente (Solo lectura)", {
            "fields": ("get_paciente_nombre", "get_paciente_identificacion"),
            "classes": ("collapse",)
        }),
        ("Estado y Procesamiento (Solo lectura)", {
            "fields": ("get_estado", "get_fecha_pago", "get_metodo_pago", "get_monto_total"),
            "classes": ("collapse",)
        }),
        ("Datos de Procesamiento", {
            "fields": ("referencia_externa", "datos_procesamiento"),
            "classes": ("collapse",)
        }),
        ("Control", {
            "fields": ("activo",),
            "classes": ("collapse",)
        })
    )
    
    def get_paciente_nombre(self, obj):
        return obj.paciente.nombre_completo if obj.paciente else "Sin paciente"
    get_paciente_nombre.short_description = "Paciente"
    
    def get_paciente_identificacion(self, obj):
        return obj.paciente.cedula_ecuatoriana if obj.paciente else "Sin identificación"
    get_paciente_identificacion.short_description = "Identificación"
    
    def get_metodo_pago(self, obj):
        return obj.metodo_pago
    get_metodo_pago.short_description = "Método de Pago"
    
    def get_monto_total(self, obj):
        return obj.monto_total
    get_monto_total.short_description = "Monto Total"
    
    def get_estado(self, obj):
        return obj.estado
    get_estado.short_description = "Estado"
    
    def get_fecha_pago(self, obj):
        return obj.fecha_pago
    get_fecha_pago.short_description = "Fecha de Pago"
    
    def get_referencia_externa(self, obj):
        return obj.pago.referencia_externa if obj.pago else "Sin referencia"
    get_referencia_externa.short_description = "Referencia Externa"

