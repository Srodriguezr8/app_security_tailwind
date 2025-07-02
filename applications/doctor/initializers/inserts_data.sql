-- INSERTS PARA public.core_especialidad --
-- Estas especialidades deben insertarse en una tabla vacía.
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Anestesiología', 'Área de atención enfocada en brindar soluciones integrales a los pacientes.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Cardiología', 'Campo clínico orientado al cuidado preventivo y terapéutico.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Cirugía General', 'Especialidad médica centrada en el diagnóstico y tratamiento de enfermedades específicas.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Cirugía Plástica', 'Disciplina que combina ciencia médica con atención personalizada.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Dermatología', 'Especialidad médica centrada en el diagnóstico y tratamiento de enfermedades específicas.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Endocrinología', 'Campo clínico orientado al cuidado preventivo y terapéutico.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Fisioterapia', 'Especialidad médica centrada en el diagnóstico y tratamiento de enfermedades específicas.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Gastroenterología', 'Rama médica que mejora la calidad de vida de los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Geriatría', 'Área de atención enfocada en brindar soluciones integrales a los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Ginecología y Obstetricia', 'Rama médica que mejora la calidad de vida de los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Infectología', 'Área de atención enfocada en brindar soluciones integrales a los pacientes.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Medicina Deportiva', 'Especialidad médica centrada en el diagnóstico y tratamiento de enfermedades específicas.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Medicina Familiar', 'Disciplina que combina ciencia médica con atención personalizada.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Medicina General', 'Disciplina que combina ciencia médica con atención personalizada.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Nefrología', 'Rama médica que mejora la calidad de vida de los pacientes.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Neumología', 'Rama médica que mejora la calidad de vida de los pacientes.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Neurología', 'Rama médica que mejora la calidad de vida de los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Nutriología', 'Rama médica que mejora la calidad de vida de los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Odontología', 'Disciplina que combina ciencia médica con atención personalizada.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Oftalmología', 'Rama médica que mejora la calidad de vida de los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Oncología', 'Área de atención enfocada en brindar soluciones integrales a los pacientes.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Ortodoncia', 'Área de atención enfocada en brindar soluciones integrales a los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Otorrinolaringología', 'Área de atención enfocada en brindar soluciones integrales a los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Pediatría', 'Campo clínico orientado al cuidado preventivo y terapéutico.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Proctología', 'Disciplina que combina ciencia médica con atención personalizada.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Psiquiatría', 'Especialidad médica centrada en el diagnóstico y tratamiento de enfermedades específicas.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Radiología', 'Rama médica que mejora la calidad de vida de los pacientes.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Reumatología', 'Disciplina que combina ciencia médica con atención personalizada.', FALSE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Traumatología', 'Especialidad médica centrada en el diagnóstico y tratamiento de enfermedades específicas.', TRUE);
INSERT INTO public.core_especialidad (nombre, descripcion, activo) VALUES ('Urología', 'Rama médica que mejora la calidad de vida de los pacientes.', TRUE);

-- INSERTS PARA public.core_doctor --
-- Inserta información de médicos ficticios para pruebas.
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Isidoro', 'Bosch Meléndez', '6834972674843', '1976-09-16', 'Avenida Félix Lillo 25 Apt. 93 
Burgos, 15759', -2.214711, -79.683187, '21FE70B15F3545CA8B51', '+34875 581 642', 'guillenrenato@example.net', 'Miércoles y Viernes, 07h00 - 12h00', 30, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Sebastian', 'Perelló Arnau', '1892024270962', '1985-05-01', 'Rambla de Jessica Casals 2
Badajoz, 48140', -2.168279, -79.687091, '71E3D9624386454C96D5', '+34 887 514 593', 'ibauza@example.net', 'Miércoles y Viernes, 07h00 - 12h00', 20, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Juan Luis', 'Riera Vizcaíno', '4189816267267', '1973-01-09', 'Via Reina Quero 63 Apt. 12 
Baleares, 32292', -2.206278, -79.694288, '27C11260DEF64333A6AA', '+34921150591', 'casalsarturo@example.net', 'Miércoles y Viernes, 07h00 - 12h00', 30, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Salomón', 'Menendez Bru', '2119590420935', '1962-10-16', 'Plaza Samu Arana 44
Barcelona, 48294', -2.211708, -79.691307, '25AC3678A6164E12AA10', '+34 861 549 540', 'ngodoy@example.net', 'Lunes a Viernes, 14h00 - 19h00', 30, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Alejandro', 'Robledo Cantón', '2694626343163', '1988-07-18', 'Cuesta de Macarena Planas 89 Apt. 02 
Santa Cruz de Tenerife, 26424', -2.155786, -79.729514, 'F8032C83F21749669D2B', '+34922602150', 'ramonfabra@example.org', 'Lunes a Viernes, 14h00 - 19h00', 20, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Lázaro', 'Riba Goñi', '5796535988838', '1986-12-02', 'Rambla Florentina Cabañas 42
Badajoz, 11380', -2.202809, -79.787231, '76E9880474FD46DCABC2', '+34705 93 45 71', 'pcolom@example.org', 'Lunes a Viernes, 14h00 - 19h00', 20, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Eligia', 'Arcos Aguiló', '0088359980175', '1978-09-02', 'Avenida de Jose Francisco Tejedor 38 Puerta 0 
Murcia, 23349', -2.181602, -79.764988, '00683F5966D14E46BA0A', '+34924 161 621', 'pulidovalero@example.net', 'Lunes a Viernes, 09h00 - 14h00', 30, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Eutropio', 'Garmendia Sanmartín', '8540500508400', '1965-06-16', 'Camino Marisa Tena 67
Jaén, 18639', -2.164864, -79.769397, 'BA13468DC5554CC9A831', '+34921889303', 'graciaroque@example.net', 'Martes y Jueves, 10h00 - 17h00', 30, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Óscar', 'Rocha Bou', '8784359509914', '1991-08-05', 'Acceso de Bautista Abellán 212 Apt. 43 
Melilla, 43921', -2.157137, -79.730629, 'E5789B722DC64B1B80D0', '+34800 10 23 51', 'qmendizabal@example.org', 'Lunes a Viernes, 14h00 - 19h00', 15, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Almudena', 'Bastida Barbero', '5372595419202', '1979-11-23', 'Paseo Merche Vives 186
Huesca, 39352', -2.16824, -79.657741, 'FFA4A48BCD1E41C5B517', '+34 806363377', 'ojedarosario@example.net', 'Miércoles y Viernes, 07h00 - 12h00', 15, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Agustín', 'Cornejo Espejo', '4717859706197', '1969-10-29', 'Paseo Duilio Téllez 586 Puerta 8 
Badajoz, 42296', -2.240792, -79.745953, '82FCAA9384444C1AA39E', '+34928 42 98 08', 'benito05@example.org', 'Miércoles y Viernes, 07h00 - 12h00', 30, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Reyna', 'Blanca Barón', '2122787411850', '1980-10-29', 'Camino de Octavio Murcia 6 Apt. 72 
Ciudad, 16421', -2.18769, -79.672312, '6D29F86E7F634444A3F6', '+34 820 622 240', 'maricelaesteban@example.net', 'Lunes a Viernes, 14h00 - 19h00', 30, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('José', 'Amador Pinto', '4072614494231', '1988-02-11', 'Alameda Mónica Raya 88
Burgos, 22938', -2.242649, -79.716849, 'D9F177E578FC4B43826C', '+34 944 069 338', 'sorianodafne@example.net', 'Martes y Jueves, 10h00 - 17h00', 20, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Valentina', 'Velasco Sancho', '3513050386587', '1974-01-03', 'Callejón de Carlota Rueda 71 Piso 8 
Lleida, 25453', -2.181569, -79.65479, 'D2D46B6558F241329289', '+34968 290 736', 'anselmodiaz@example.net', 'Miércoles y Viernes, 07h00 - 12h00', 20, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Vera', 'Lobo Jáuregui', '4571766323781', '1959-11-16', 'Cuesta de Encarnita Moll 40
Vizcaya, 06779', -2.185964, -79.747363, '8A876D24327D45D38F40', '+34876 445 094', 'emperatriz67@example.com', 'Miércoles y Viernes, 07h00 - 12h00', 30, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Evangelina', 'Lloret Calvet', '1994426968578', '1978-01-02', 'Via José Manuel Bravo 9 Apt. 22 
Vizcaya, 04928', -2.209787, -79.689999, '1E391E6A6D5F4981A770', '+34948626946', 'luisinasalas@example.org', 'Lunes a Viernes, 08h00 - 13h00', 20, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Noé', 'Adán Doménech', '6672714318015', '1984-11-01', 'Rambla de Calisto Zabala 71
Guadalajara, 08872', -2.218637, -79.655727, '4C252A0C455D4FE99D11', '+34947956065', 'baudeliotirado@example.com', 'Lunes a Viernes, 08h00 - 13h00', 30, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Rufina', 'Azcona Royo', '4039872390884', '1961-01-13', 'Avenida Esmeralda Vazquez 4 Puerta 3 
Córdoba, 15149', -2.155633, -79.663351, '6F9C40FDEDA444FAAEAB', '+34949 645 403', 'ana-sofia85@example.org', 'Lunes a Viernes, 08h00 - 13h00', 20, FALSE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Sosimo', 'Gomila Mendizábal', '3965848682970', '1954-11-21', 'Ronda de Crescencia Ochoa 3
Madrid, 40984', -2.168718, -79.700058, 'BF5FE724A62B4046B27E', '+34823 84 17 91', 'martagaliano@example.com', 'Lunes a Viernes, 08h00 - 13h00', 20, TRUE, NULL, NULL, NULL, NULL);
INSERT INTO public.core_doctor (nombres, apellidos, ruc, fecha_nacimiento, direccion, latitud, longitud, codigo_unico_doctor, telefonos, email, horario_atencion, duracion_atencion, activo, curriculum, firma_digital, foto, imagen_receta) VALUES ('Federico', 'Ferrero Laguna', '6997907395318', '1964-09-30', 'Urbanización Tecla Verdú 905
Zamora, 06597', -2.227103, -79.786915, 'FFC2146367A842F5979F', '+34826 903 367', 'carmela55@example.net', 'Martes y Jueves, 10h00 - 17h00', 30, FALSE, NULL, NULL, NULL, NULL);

-- INSERTS PARA public.core_doctor_especialidad (relaciones Many-to-Many) --
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (1, 8);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (2, 27);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (2, 25);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (2, 30);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (3, 24);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (3, 4);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (4, 22);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (4, 2);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (4, 7);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (5, 30);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (5, 28);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (6, 15);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (6, 12);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (7, 10);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (7, 17);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (7, 28);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (8, 24);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (8, 11);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (8, 3);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (9, 6);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (9, 20);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (9, 22);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (10, 16);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (11, 11);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (11, 29);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (11, 26);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (12, 6);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (12, 30);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (13, 25);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (13, 28);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (13, 16);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (14, 3);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (15, 30);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (15, 24);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (15, 9);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (16, 15);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (17, 30);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (17, 11);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (18, 15);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (18, 8);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (18, 26);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (19, 19);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (19, 26);
INSERT INTO public.core_doctor_especialidad (doctor_id, especialidad_id) VALUES (20, 13);

-- Fin del archivo generado correctamente --
