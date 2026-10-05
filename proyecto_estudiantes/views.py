from models import Estudiante, CAMPOS_ESTUDIANTE

from shared.json_manager import GestorJSON

from shared.herramientas import es_email_valido


# Archivo donde se guardan los estudiantes
gestor = GestorJSON(
    "data/estudiantes.json"
)


# TUPLAS
CAMPOS_OBLIGATORIOS = (
    "nombre",
    "apellido",
    "email",
    "carnet"
)

CAMPOS_BUSCABLES = (
    "nombre",
    "apellido",
    "email",
    "carnet"
)


# ========================================
# AYUDAS INTERNAS
# ========================================

def siguiente_id():

    ids = []

    for registro in gestor.leer():
        ids.append(registro["id"])

    if ids:
        return max(ids) + 1

    return 1


def carnets_registrados(excepto_id=None):

    carnets = set()

    for registro in gestor.leer():

        if registro["id"] != excepto_id:

            carnets.add(
                registro["carnet"].lower()
            )

    return carnets


# ========================================
# C - CREATE
# ========================================

def crear_estudiante(datos):

    try:

        valores = {}

        for campo in CAMPOS_ESTUDIANTE:

            valores[campo] = str(
                datos.get(campo, "")
            ).strip()

        # Comprobar campos vacíos
        faltantes = []

        for campo in CAMPOS_OBLIGATORIOS:

            if not valores[campo]:
                faltantes.append(campo)

        if faltantes:

            return (
                False,
                "Faltan campos obligatorios: "
                + ", ".join(faltantes)
            )

        # Validar email
        if not es_email_valido(
            valores["email"]
        ):

            return (
                False,
                "El email no tiene un formato válido"
            )

        # Validar carnet repetido
        if (
            valores["carnet"].lower()
            in carnets_registrados()
        ):

            return (
                False,
                "Ese carnet ya está registrado"
            )

        # Crear objeto estudiante
        estudiante = Estudiante(
            siguiente_id(),
            valores["nombre"],
            valores["apellido"],
            valores["email"],
            valores["carnet"]
        )

        # Leer lista actual
        registros = gestor.leer()

        # Agregar nuevo estudiante
        registros.append(
            estudiante.a_diccionario()
        )

        # Guardar JSON
        if not gestor.guardar(registros):

            return (
                False,
                "No se pudo guardar el archivo"
            )

        return (
            True,
            f"Estudiante "
            f"{estudiante.obtener_nombre_completo()} "
            f"creado con id {estudiante.id}"
        )

    except Exception as error:

        return (
            False,
            f"Error inesperado: {error}"
        )


# ========================================
# R - READ
# ========================================

def obtener_todos():

    estudiantes = []

    for registro in gestor.leer():

        estudiante = (
            Estudiante.desde_diccionario(
                registro
            )
        )

        estudiantes.append(estudiante)

    return estudiantes


def obtener_por_id(id_estudiante):

    estudiantes = obtener_todos()

    for estudiante in estudiantes:

        if estudiante.id == id_estudiante:
            return estudiante

    return None


# ========================================
# S - SEARCH
# ========================================

def buscar_estudiantes(termino):

    termino = termino.strip().lower()

    if not termino:
        return []

    encontrados = []

    for registro in gestor.leer():

        for campo in CAMPOS_BUSCABLES:

            valor = str(
                registro.get(campo, "")
            ).lower()

            if termino in valor:

                encontrados.append(
                    Estudiante.desde_diccionario(
                        registro
                    )
                )

                break

    return encontrados


# ========================================
# U - UPDATE
# ========================================

def actualizar_estudiante(
    id_estudiante,
    cambios
):

    try:

        campos_validos = set(
            CAMPOS_ESTUDIANTE
        )

        desconocidos = (
            set(cambios)
            - campos_validos
        )

        if desconocidos:

            return (
                False,
                "Campos no válidos: "
                + ", ".join(desconocidos)
            )

        if not cambios:

            return (
                False,
                "No se indicó ningún cambio"
            )

        # Validar email
        if "email" in cambios:

            if not es_email_valido(
                cambios["email"]
            ):

                return (
                    False,
                    "El email no tiene "
                    "un formato válido"
                )

        # Validar nuevo carnet
        if "carnet" in cambios:

            if (
                cambios["carnet"].lower()
                in carnets_registrados(
                    excepto_id=id_estudiante
                )
            ):

                return (
                    False,
                    "Ese carnet ya lo usa "
                    "otro estudiante"
                )

        registros = gestor.leer()

        posicion = None

        for indice, registro in enumerate(
            registros
        ):

            if (
                registro["id"]
                == id_estudiante
            ):

                posicion = indice

                break

        if posicion is None:

            return (
                False,
                f"No existe un estudiante "
                f"con id {id_estudiante}"
            )

        registros[posicion].update(
            cambios
        )

        gestor.guardar(registros)

        return (
            True,
            f"Estudiante {id_estudiante} "
            "actualizado correctamente"
        )

    except Exception as error:

        return (
            False,
            f"Error inesperado: {error}"
        )


# ========================================
# D - DELETE
# ========================================

def eliminar_estudiante(id_estudiante):

    registros = gestor.leer()

    quedan = []

    for registro in registros:

        if (
            registro["id"]
            != id_estudiante
        ):

            quedan.append(registro)

    if len(quedan) == len(registros):

        return (
            False,
            f"No existe un estudiante "
            f"con id {id_estudiante}"
        )

    gestor.guardar(quedan)

    return (
        True,
        f"Estudiante {id_estudiante} "
        "eliminado correctamente"
    )


# ========================================
# AGREGAR NOTA
# ========================================

def agregar_nota(
    id_estudiante,
    materia,
    nota
):

    estudiante = obtener_por_id(
        id_estudiante
    )

    if estudiante is None:

        return (
            False,
            "El estudiante no existe"
        )

    # La tarea pide notas de 0 a 20
    if nota < 0 or nota > 20:

        return (
            False,
            "La nota debe estar "
            "entre 0 y 20"
        )

    materia = materia.strip()

    if not materia:

        return (
            False,
            "La materia no puede "
            "estar vacía"
        )

    estudiante.agregar_nota(
        materia,
        nota
    )

    registros = gestor.leer()

    for indice, registro in enumerate(
        registros
    ):

        if (
            registro["id"]
            == id_estudiante
        ):

            registros[indice] = (
                estudiante.a_diccionario()
            )

            break

    gestor.guardar(registros)

    return (
        True,
        f"Nota {nota} agregada "
        f"en {materia}"
    )


# ========================================
# MATERIAS OFERTADAS
# ========================================

def materias_ofertadas():

    materias = set()

    for estudiante in obtener_todos():

        materias.update(
            estudiante.materias
        )

    return materias


# ========================================
# MATERIAS EN COMÚN
# ========================================

def estudiantes_en_comun(
    id_a,
    id_b
):

    estudiante_a = obtener_por_id(
        id_a
    )

    estudiante_b = obtener_por_id(
        id_b
    )

    if estudiante_a is None:

        return (
            False,
            "El primer estudiante no existe"
        )

    if estudiante_b is None:

        return (
            False,
            "El segundo estudiante no existe"
        )

    materias = (
        estudiante_a.materias_en_comun(
            estudiante_b
        )
    )

    return (
        True,
        materias
    )