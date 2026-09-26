import streamlit as st
from datetime import date, time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Socio, Actividad, Profesor, Clase, Asistencia, Inscripcion

# --- CONFIGURACIÓN ÚNICA DE LA PÁGINA (DEBE IR PRIMERO) ---
st.set_page_config(page_title="Gestión de Gimnasio", page_icon="🏋️‍♂️", layout="wide")

# --- CONFIGURACIÓN DE BASE DE DATOS ---
db_url = st.secrets["db_url"]
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- SISTEMA DE LOGUEO / AUTENTICACIÓN ---
def check_password():
    """Devuelve True si el usuario ingresó la contraseña correcta."""
    def password_entered():
        if (
            st.session_state["username"] == st.secrets["admin_user"]
            and st.session_state["password"] == st.secrets["admin_password"]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.markdown("<h2 style='text-align: center;'>🔒 Acceso al Sistema de Gestión</h2>", unsafe_allow_html=True)
    st.write("Por favor, introduce tus credenciales de administrador para continuar.")
    
    with st.form("login_form"):
        st.text_input("Usuario", key="username")
        st.text_input("Contraseña", type="password", key="password")
        st.form_submit_button("Iniciar Sesión", on_click=password_entered)

    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("❌ Usuario o contraseña incorrectos.")
        
    return False

# --- CONTROL DE FLUJO DE LA APLICACIÓN ---
if check_password():
    # TODO LO QUE ESTÁ AQUÍ ADENTRO DEBE LLEVAR UNA INDENTACIÓN/TABULACIÓN EXTRA
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state["password_correct"] = False
        st.rerun()
        
    st.title("🏋️‍♂️ Panel de Control - Gimnasio")

    opcion = st.sidebar.selectbox(
        "Selecciona una sección:",
        [
            "Registrar Socio", 
            "Ver Socios", 
            "Registrar Profesor", 
            "Registrar Actividad", 
            "Programar Clase", 
            "Inscribir Socio a Actividad",  
            "Marcar Asistencia",
            "Administrar Bajas y Eliminaciones"  
        ]
    )

    # ¡IMPORTANTE! Fíjate que a partir de aquí todo el código lleva 4 espacios de sangría:
    

# --- SECCIÓN: REGISTRAR SOCIO ---
    if opcion == "Registrar Socio":
        st.header("👤 Alta de Nuevo Socio")
        
        with st.form("formulario_socio", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre")
                apellido = st.text_input("Apellido")
                nro_documento = st.text_input("Número de Documento (DNI/CI)")
            with col2:
                email = st.text_input("Correo Electrónico")
                telefono = st.text_input("Teléfono (Opcional)")
                f_nacimiento = st.date_input("Fecha de Nacimiento", min_value=date(1940, 1, 1))
                sexo = st.selectbox("Sexo", ["M", "F", "O"])
            
            enviar = st.form_submit_button("Guardar Socio")
            
            if enviar:
                if not nombre or not apellido or not nro_documento or not email:
                    st.error("Por favor, completa todos los campos obligatorios.")
                else:
                    session = SessionLocal()
                    try:
                        nuevo_socio = Socio(
                            nombre=nombre,
                            apellido=apellido,
                            nro_documento=nro_documento,
                            email=email,
                            telefono=telefono if telefono else None,
                            f_nacimiento=f_nacimiento,
                            sexo=sexo
                        )
                        session.add(nuevo_socio)
                        session.commit()
                        st.success(f"¡Socio {nombre} {apellido} registrado con éxito!")
                    # CÓDIGO NUEVO (Muestra el error técnico)
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error al guardar: el documento o email ya podrían existir.")
                        st.code(f"Detalle técnico del error:\n{str(e)}") # Esto te mostrará la causa real en pantalla
                    finally:
                        session.close()
    
    # --- SECCIÓN: VER SOCIOS ---
    elif opcion == "Ver Socios":
        st.header("📋 Listado de Socios Registrados")
        
        session = SessionLocal()
        socios = session.scalars(select(Socio)).all()
        session.close()
        
        if socios:
            # Transformar a una lista de diccionarios para mostrar en una tabla limpia
            datos_tabla = [{
                "ID": s.id,
                "Apellido": s.apellido,
                "Nombre": s.nombre,
                "Documento": s.nro_documento,
                "Email": s.email,
                "Teléfono": s.telefono,
                "Fecha Alta": s.f_alta
            } for s in socios]
            
            st.dataframe(datos_tabla, use_container_width=True)
        else:
            st.info("No hay socios registrados todavía.")
    
    # --- SECCIÓN: PROGRAMAR CLASE ---
    elif opcion == "Programar Clase":
        st.header("📅 Programar Nueva Clase")
        
        session = SessionLocal()
        profesores = session.scalars(select(Profesor)).all()
        actividades = session.scalars(select(Actividad)).all()
        session.close()
        
        if not profesores or not actividades:
            st.warning("Necesitas tener Profesores y Actividades cargadas en la Base de Datos para crear una clase.")
        else:
            with st.form("formulario_clase"):
                dia = st.selectbox("Día de la semana", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"])
                hora = st.time_input("Horario de la clase", value=time(9, 0))
                
                profe_opciones = {f"{p.apellido}, {p.nombre}": p.id for p in profesores}
                profe_seleccionado = st.selectbox("Profesor", list(profe_opciones.keys()))
                
                act_opciones = {a.nombre: a.id for a in actividades}
                act_seleccionada = st.selectbox("Actividad", list(act_opciones.keys()))
                
                guardar_clase = st.form_submit_button("Crear Clase")
                
                if guardar_clase:
                    session = SessionLocal()
                    try:
                        nueva_clase = Clase(
                            dia_de_la_semana=dia,
                            horario=hora,
                            profesor_id=profe_opciones[profe_seleccionado],
                            actividad_id=act_opciones[act_seleccionada]
                        )
                        session.add(nueva_clase)
                        session.commit()
                        st.success("¡Clase programada con éxito!")
                    except Exception as e:
                        session.rollback()
                        st.error("Error: Ya existe una clase de esa actividad en el mismo día y horario.")
                    finally:
                        session.close()
    
    # --- SECCIÓN: MARCAR ASISTENCIA ---
    # --- SECCIÓN: MARCAR ASISTENCIA ---
    elif opcion == "Marcar Asistencia":
        st.header("📝 Registro de Asistencia Diario")
        
        session = SessionLocal()
        socios = session.scalars(select(Socio)).all()
        clases = session.scalars(select(Clase)).all()
        
        if not socios or not clases:
            st.warning("Debes tener socios y clases cargadas para registrar asistencias.")
            session.close()
        else:
            # Armamos los diccionarios para los selects de la interfaz
            socio_opciones = {f"{s.apellido}, {s.nombre} ({s.nro_documento})": s.id for s in socios}
            clase_opciones = {f"{c.actividad.nombre} - {c.dia_de_la_semana} {c.horario.strftime('%H:%M')}": c.id for c in clases}
            session.close()
            
            socio_sel = st.selectbox("Selecciona el Socio", list(socio_opciones.keys()))
            clase_sel = st.selectbox("Selecciona la Clase", list(clase_opciones.keys()))
            fecha_asistencia = st.date_input("Fecha", value=date.today())
            
            if st.button("Registrar Asistencia"):
                session = SessionLocal()
                try:
                    # 1. Obtener el ID de la clase seleccionada
                    id_clase_elegida = clase_opciones[clase_sel]
                    
                    # 2. Buscar la clase y su actividad para conocer el cupo máximo
                    clase_objeto = session.get(Clase, id_clase_elegida)
                    cupo_maximo = clase_objeto.actividad.cupo_max
                    nombre_actividad = clase_objeto.actividad.nombre
                    
                    # 3. Contar cuántas asistencias ya existen para esta clase en esta fecha
                    asistencias_actuales = session.scalar(
                        select(Asistencia)
                        .where(Asistencia.clase_id == id_clase_elegida)
                        .where(Asistencia.f_asistencia == fecha_asistencia)
                    )
                    
                    # Contamos cuántos registros devolvió la consulta
                    cantidad_anotados = session.query(Asistencia).filter(
                        Asistencia.clase_id == id_clase_elegida,
                        Asistencia.f_asistencia == fecha_asistencia
                    ).count()
                    
                    # 4. Validar el cupo antes de insertar
                    if cantidad_anotados >= cupo_maximo:
                        st.error(f"❌ ¡Cupo Completo! La actividad '{nombre_actividad}' tiene un límite de {cupo_maximo} personas para el día de hoy.")
                    else:
                        # Si hay lugar, registramos la asistencia
                        nueva_asistencia = Asistencia(
                            socio_id=socio_opciones[socio_sel],
                            clase_id=id_clase_elegida,
                            f_asistencia=fecha_asistencia
                        )
                        session.add(nueva_asistencia)
                        session.commit()
                        
                        lugares_libres = cupo_maximo - (cantidad_anotados + 1)
                        st.success(f"✅ Asistencia registrada correctamente. Quedan {lugares_libres} lugares disponibles para esta clase.")
                        
                except Exception as e:
                    session.rollback()
                    st.error("⚠️ El socio ya tiene registrada la asistencia a esta clase en el día de hoy.")
                finally:
                    session.close()
    
    # --- SECCIÓN: REGISTRAR PROFESOR ---
    elif opcion == "Registrar Profesor":
        st.header("👨‍🏫 Alta de Nuevo Profesor")
        
        with st.form("formulario_profesor", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nombre_p = st.text_input("Nombre")
                apellido_p = st.text_input("Apellido")
                doc_p = st.text_input("Número de Documento")
            with col2:
                email_p = st.text_input("Correo Electrónico")
                tel_p = st.text_input("Teléfono (Opcional)")
                
            enviar_p = st.form_submit_button("Guardar Profesor")
            
            if enviar_p:
                if not nombre_p or not apellido_p or not doc_p or not email_p:
                    st.error("Por favor, completa los campos obligatorios.")
                else:
                    session = SessionLocal()
                    try:
                        nuevo_profe = Profesor(
                            nombre=nombre_p,
                            apellido=apellido_p,
                            nro_documento=doc_p,
                            email=email_p,
                            telefono=tel_p if tel_p else None
                        )
                        session.add(nuevo_profe)
                        session.commit()
                        st.success(f"¡Profesor {nombre_p} {apellido_p} registrado con éxito!")
                    except Exception as e:
                        session.rollback()
                        st.error("Error: El documento ya se encuentra registrado.")
                    finally:
                        session.close()
    
    # --- SECCIÓN: REGISTRAR ACTIVIDAD ---
    elif opcion == "Registrar Actividad":
        st.header("🏋️‍♀️ Nueva Actividad Deportiva")
        
        with st.form("formulario_actividad", clear_on_submit=True):
            nombre_a = st.text_input("Nombre de la Actividad (Ej: Pilates, Crossfit)")
            descripcion_a = st.text_area("Descripción")
            
            col1, col2 = st.columns(2)
            with col1:
                duracion_a = st.number_input("Duración (en minutos)", min_value=10, max_value=300, value=60)
            with col2:
                cupo_a = st.number_input("Cupo Máximo de Alumnos", min_value=1, max_value=100, value=20)
                
            enviar_a = st.form_submit_button("Guardar Actividad")
            
            if enviar_a:
                if not nombre_a or not descripcion_a:
                    st.error("Por favor, completa el nombre y la descripción.")
                else:
                    session = SessionLocal()
                    try:
                        nueva_act = Actividad(
                            nombre=nombre_a,
                            descripcion=descripcion_a,
                            duracion=int(duracion_a),
                            cupo_max=int(cupo_a)
                        )
                        session.add(nueva_act)
                        session.commit()
                        st.success(f"¡Actividad '{nombre_a}' creada con éxito!")
                    except Exception as e:
                        session.rollback()
                        st.error("Error: Ya existe una actividad con ese nombre.")
                    finally:
                        session.close()
    
    # --- SECCIÓN: INSCRIBIR SOCIO A ACTIVIDAD ---
    elif opcion == "Inscribir Socio a Actividad":
        st.header("📋 Inscripción Fija a una Actividad")
        st.caption("Asocia de forma permanente a un socio con una disciplina deportiva.")
    
        session = SessionLocal()
        socios = session.scalars(select(Socio)).all()
        actividades = session.scalars(select(Actividad)).all()
        session.close()
    
        if not socios or not actividades:
            st.warning("Debes tener socios y actividades creadas en el sistema para realizar inscripciones.")
        else:
            socio_opciones = {f"{s.apellido}, {s.nombre} ({s.nro_documento})": s.id for s in socios}
            act_opciones = {a.nombre: a.id for a in actividades}
    
            with st.form("formulario_inscripcion", clear_on_submit=True):
                socio_sel = st.selectbox("Selecciona el Socio", list(socio_opciones.keys()))
                act_sel = st.selectbox("Selecciona la Actividad", list(act_opciones.keys()))
                fecha_inscripcion = st.date_input("Fecha de Inscripción", value=date.today())
                
                guardar_inscripcion = st.form_submit_button("Confirmar Inscripción")
    
                if guardar_inscripcion:
                    session = SessionLocal()
                    try:
                        id_actividad = act_opciones[act_sel]
                        id_socio = socio_opciones[socio_sel]
    
                        # 1. Validar si la actividad ya alcanzó su cupo máximo de inscriptos fijos
                        actividad_obj = session.get(Actividad, id_actividad)
                        cupo_maximo = actividad_obj.cupo_max
    
                        total_inscriptos = session.query(Inscripcion).filter(
                            Inscripcion.actividad_id == id_actividad
                        ).count()
    
                        if total_inscriptos >= cupo_maximo:
                            st.error(f"❌ No hay vacantes. '{actividad_obj.nombre}' ya tiene {total_inscriptos} socios inscriptos fijos (Cupo máximo: {cupo_maximo}).")
                        else:
                            # 2. Guardar la inscripción fija si hay vacantes
                            nueva_inscripcion = Inscripcion(
                                actividad_id=id_actividad,
                                socio_id=id_socio,
                                f_inscripcion=fecha_inscripcion
                            )
                            session.add(nueva_inscripcion)
                            session.commit()
                            st.success(f"🎉 ¡Socio inscripto con éxito en la actividad '{act_sel}'!")
                    except Exception as e:
                        session.rollback()
                        st.error("⚠️ El socio ya se encuentra inscripto en esta actividad específica.")
                    finally:
                        session.close()
    
    
    # --- SECCIÓN: ADMINISTRAR BAJAS Y ELIMINACIONES ---
    elif opcion == "Administrar Bajas y Eliminaciones":
        st.header("🗑️ Centro de Bajas y Eliminaciones")
        st.caption("Gestiona la eliminación segura de registros de la base de datos.")
    
        sub_opcion = st.tabs(["Eliminar Socio", "Cancelar Inscripción", "Eliminar Clase / Horario"])
    
        # SUB-PESTAÑA 1: ELIMINAR SOCIO
        with sub_opcion[0]:
            st.subheader("Socios Activos")
            session = SessionLocal()
            socios = session.scalars(select(Socio)).all()
            session.close()
    
            if not socios:
                st.info("No hay socios registrados para eliminar.")
            else:
                socio_eliminar_opciones = {f"{s.apellido}, {s.nombre} (Doc: {s.nro_documento})": s.id for s in socios}
                socio_sel = st.selectbox("Selecciona el socio que deseas dar de baja:", list(socio_eliminar_opciones.keys()))
                
                if st.button("🔴 Eliminar Socio permanentemente", key="btn_del_socio"):
                    session = SessionLocal()
                    try:
                        socio_obj = session.get(Socio, socio_eliminar_opciones[socio_sel])
                        session.delete(socio_obj)
                        session.commit()
                        st.success("Socio y todos sus registros asociados (inscripciones/asistencias) han sido eliminados.")
                        st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error al eliminar: {e}")
                    finally:
                        session.close()
    
        # SUB-PESTAÑA 2: CANCELAR INSCRIPCIÓN FIJA
        with sub_opcion[1]:
            st.subheader("Inscripciones Vigentes")
            session = SessionLocal()
            # Traemos las inscripciones e incluimos los nombres de socio y actividad para que sea legible
            inscripciones = session.scalars(select(Inscripcion)).all()
            
            if not inscripciones:
                st.info("No hay inscripciones fijas registradas.")
                session.close()
            else:
                insc_opciones = {
                    f"Socio: {i.socio.apellido}, {i.socio.nombre} ➡️ Actividad: {i.actividad.nombre}": i.id 
                    for i in inscripciones
                }
                session.close()
                
                insc_sel = st.selectbox("Selecciona la inscripción a dar de baja:", list(insc_opciones.keys()))
                
                if st.button("❌ Cancelar Inscripción", key="btn_del_insc"):
                    session = SessionLocal()
                    try:
                        insc_obj = session.get(Inscripcion, insc_opciones[insc_sel])
                        session.delete(insc_obj)
                        session.commit()
                        st.success("La inscripción fue cancelada de forma correcta.")
                        st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error al cancelar: {e}")
                    finally:
                        session.close()
    
        # SUB-PESTAÑA 3: ELIMINAR CLASE / HORARIO
        with sub_opcion[2]:
            st.subheader("Grilla Horaria Actual")
            session = SessionLocal()
            clases = session.scalars(select(Clase)).all()
            
            if not clases:
                st.info("No hay clases programadas en la agenda.")
                session.close()
            else:
                clase_del_opciones = {
                    f"{c.actividad.nombre} - {c.dia_de_la_semana} a las {c.horario.strftime('%H:%M')} (Prof: {c.profesor.apellido})": c.id 
                    for c in clases
                }
                session.close()
                
                clase_sel = st.selectbox("Selecciona la clase a remover del calendario:", list(clase_del_opciones.keys()))
                
                if st.button("🗑️ Eliminar Clase del Cronograma", key="btn_del_clase"):
                    session = SessionLocal()
                    try:
                        clase_obj = session.get(Clase, clase_del_opciones[clase_sel])
                        session.delete(clase_obj)
                        session.commit()
                        st.success("La clase ha sido removida del cronograma.")
                        st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Error: No se puede eliminar una clase que ya cuenta con registros de asistencia guardados.")
                    finally:
                        session.close()
