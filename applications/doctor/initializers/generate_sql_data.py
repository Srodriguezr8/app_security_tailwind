from faker import Faker
import random
import uuid

# Inicializa Faker con español genérico
fake = Faker('es')

def escape_sql_string(texto):
    if texto is None:
        return 'NULL'
    return f"'{texto.replace("'", "''")}'"

def generar_sql_especialidades(archivo):
    archivo.write("-- INSERTS PARA public.core_especialidad --\n")
    archivo.write("-- Estas especialidades deben insertarse en una tabla vacía.\n")

    lista_especialidades = [
        "Cardiología", "Pediatría", "Ginecología y Obstetricia",
        "Dermatología", "Neurología", "Oftalmología",
        "Otorrinolaringología", "Psiquiatría", "Radiología",
        "Medicina General", "Traumatología", "Urología",
        "Oncología", "Endocrinología", "Gastroenterología",
        "Anestesiología", "Cirugía General", "Nefrología",
        "Reumatología", "Infectología", "Neumología", "Geriatría",
        "Medicina Familiar", "Proctología", "Nutriología", "Cirugía Plástica",
        "Medicina Deportiva", "Odontología", "Ortodoncia", "Fisioterapia"
    ]

    descripciones = [
        "Especialidad médica centrada en el diagnóstico y tratamiento de enfermedades específicas.",
        "Área de atención enfocada en brindar soluciones integrales a los pacientes.",
        "Disciplina que combina ciencia médica con atención personalizada.",
        "Campo clínico orientado al cuidado preventivo y terapéutico.",
        "Rama médica que mejora la calidad de vida de los pacientes."
    ]

    mapa_especialidades = {}
    id_actual = 1

    for nombre in sorted(set(lista_especialidades)):
        descripcion = escape_sql_string(random.choice(descripciones))
        activo = 'TRUE' if random.choice([True, False]) else 'FALSE'

        sql = (
            f"INSERT INTO public.core_especialidad (nombre, descripcion, activo) "
            f"VALUES ({escape_sql_string(nombre)}, {descripcion}, {activo});\n"
        )
        archivo.write(sql)
        mapa_especialidades[nombre] = id_actual
        id_actual += 1

    archivo.write("\n")
    return mapa_especialidades

def generar_sql_doctores(archivo, mapa_especialidades, cantidad_doctores=20):
    archivo.write("-- INSERTS PARA public.core_doctor --\n")
    archivo.write("-- Inserta información de médicos ficticios para pruebas.\n")

    especialidades_disponibles = list(mapa_especialidades.values())
    relaciones_m2m = []

    horarios = [
        "Lunes a Viernes, 08h00 - 13h00",
        "Lunes a Viernes, 09h00 - 14h00",
        "Lunes a Viernes, 14h00 - 19h00",
        "Martes y Jueves, 10h00 - 17h00",
        "Miércoles y Viernes, 07h00 - 12h00"
    ]

    for i in range(cantidad_doctores):
        nombres = escape_sql_string(fake.first_name())
        apellidos = escape_sql_string(fake.last_name() + " " + fake.last_name())
        ruc = ''.join([str(random.randint(0, 9)) for _ in range(13)])
        codigo_unico = str(uuid.uuid4()).replace('-', '').upper()[:20]
        fecha_nacimiento = fake.date_of_birth(minimum_age=30, maximum_age=70).isoformat()
        direccion = escape_sql_string(fake.address())
        latitud = round(random.uniform(-2.25, -2.15), 6)
        longitud = round(random.uniform(-79.80, -79.65), 6)
        telefono = escape_sql_string(fake.phone_number()[:20])
        correo = escape_sql_string(fake.email())
        horario = escape_sql_string(random.choice(horarios))
        duracion = random.choice([15, 20, 30])
        activo = 'TRUE' if random.choice([True, False]) else 'FALSE'

        sql_doctor = (
            f"INSERT INTO public.core_doctor ("
            f"nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, "
            f"codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, "
            f"curriculum, firma_digital, foto, imagen_receta"
            f") VALUES ("
            f"{nombres}, {apellidos}, '{ruc}', '{fecha_nacimiento}', {direccion}, "
            f"{latitud}, {longitud}, '{codigo_unico}', {telefono}, {correo}, "
            f"{horario}, {duracion}, {activo}, NULL, NULL, NULL, NULL"
            f");\n"
        )
        archivo.write(sql_doctor)

        doctor_id = i + 1
        num_especialidades = random.randint(1, 3)
        especialidades_asignadas = random.sample(especialidades_disponibles, num_especialidades)

        for id_especialidad in especialidades_asignadas:
            sql_m2m = (
                f"INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) "
                f"VALUES ({doctor_id}, {id_especialidad});\n"
            )
            relaciones_m2m.append(sql_m2m)

    archivo.write("\n-- INSERTS PARA public.core_doctor_especialidad (relaciones Many-to-Many) --\n")
    for rel in relaciones_m2m:
        archivo.write(rel)

    archivo.write("\n-- Fin del archivo generado correctamente --\n")

if __name__ == '__main__':
    with open("inserts_data.sql", "w", encoding="utf-8") as archivo:
        mapa = generar_sql_especialidades(archivo)
        generar_sql_doctores(archivo, mapa, cantidad_doctores=20)
