from django.db import models


class SexoChoices(models.TextChoices):
    MASCULINO = 'masculino', 'Masculino'
    FEMENINO = 'femenino', 'Femenino'

class EstadoCivilChoices(models.TextChoices):
    SOLTERO = 'soltero', 'Soltero'
    CASADO = 'casado', 'Casado'
    DIVORCIADO = 'divorciado', 'Divorciado'
    VIUDO = 'viudo', 'Viudo'
    UNION_LIBRE = 'union_libre', 'Unión libre'
    
class CondicionMedicaChoices(models.TextChoices):
   # valor_en_base_de_datos = 'valor_en_base_de_datos', 'Nombre Visible en la UI'
    HIPERTENSION = 'hipertension', 'Hipertensión'
    DIABETES_TIPO2 = 'diabetes_tipo2', 'Diabetes Tipo 2'
    ASMA = 'asma', 'Asma'
    ARTRITIS = 'artritis', 'Artritis'
    HIPOTIROIDISMO = 'hipotiroidismo', 'Hipotiroidismo'
    ENFERMEDAD_CORONARIA = 'enfermedad_coronaria', 'Enfermedad Coronaria'
    MIGRANA_CRONICA = 'migrana_cronica', 'Migraña Crónica'
    DEPRESION = 'depresion', 'Depresión'
    ANSIEDAD_GENERALIZADA = 'ansiedad_generalizada', 'Ansiedad Generalizada'
    REFLUJO_GASTROESOFAGICO = 'reflujo_gastroesofagico', 'Reflujo Gastroesofágico'
    OSTEOPOROSIS = 'osteoporosis', 'Osteoporosis'
    ALERGIAS_ESTACIONALES = 'alergias_estacionales', 'Alergias Estacionales'
    CALCULOS_RENALES = 'calculos_renales', 'Cálculos Renales'
    FIBROMIALGIA = 'fibromialgia', 'Fibromialgia'
    DERMATITIS_ATOPICA = 'dermatitis_atopica', 'Dermatitis Atópica'
    CONTROL_RUTINARIO = 'control_rutinario', 'Control Rutinario'
    SEGUIMIENTO_POST_OPERATORIO = 'seguimiento_post_operatorio', 'Seguimiento Post-operatorio'
    CHEQUEO_GENERAL = 'chequeo_general', 'Chequeo General'
    INFECCION_RESPIRATORIA = 'infeccion_respiratoria', 'Infección Respiratoria'
    GRIPE_ESTACIONAL = 'gripe_estacional', 'Gripe Estacional'
    
    
class EstadoCitaChoices(models.TextChoices):
    PROGRAMADA = 'programada', 'Programada'
    CONFIRMADA = 'confirmada', 'Confirmada'
    REALIZADA = 'realizada', 'Realizada'
    CANCELADA = 'cancelada', 'Cancelada'
    REPROGRAMADA = 'reprogramada', 'Reprogramada'
    NO_ASISTIO = 'no_asistio', 'No Asistió'    
    
    
class TipoCitaChoices(models.TextChoices):
    URGENTE = 'urgente', 'Urgente'
    NORMAL = 'normal', 'Normal'
    SEGUIMIENTO = 'seguimiento', 'Seguimiento'    
    
class CondicionPacienteChoices(models.TextChoices):
    HIPERTENSION = 'hipertension', 'Hipertensión'
    DIABETES = 'diabetes', 'Diabetes'
    CONTROL_RUTINARIO = 'control_rutinario', 'Control Rutinario'
    CARDIOLOGIA = 'cardiologia', 'Cardiología' # Nota: Esto es más una especialidad, pero si así lo usas en 'condition'
    SEGUIMIENTO = 'seguimiento', 'Seguimiento' # Nota: Esto puede solaparse con TipoCitaChoices, revisa tu lógica
    NEUROLOGIA = 'neurologia', 'Neurología' # Nota: Esto es más una especialidad
    GINECOLOGIA = 'ginecologia', 'Ginecología' # Nota: Esto es más una especialidad
    ORTOPEDIA = 'ortopedia', 'Ortopedia' # Nota: Esto es más una especialidad
    DERMATOLOGIA = 'dermatologia', 'Dermatología' # Nota: Esto es más una especialidad
    OFTALMOLOGIA = 'oftalmologia', 'Oftalmología' # Nota: Esto es más una especialidad
    ARTRITIS = 'artritis', 'Artritis' # Añadido de tu 
    INFECION_RESPIRATOTORIA =  'infeccion_respiratoria', 'Infeccion respiratoria'
    OTORRINOLARINGOLOGIA = 'otorrinolaringologia', 'Otorrinolaringología'
    PEDIATRIA = 'pediatria', 'Pediatría'
    GASTROENTEROLOGIA = 'gastroenterologia', 'Gastroenterología'
