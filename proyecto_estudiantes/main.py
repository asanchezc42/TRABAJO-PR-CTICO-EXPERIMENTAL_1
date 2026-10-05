from models import CAMPOS_ESTUDIANTE

from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import (
    crear_estudiante,
    obtener_todos,
    obtener_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    agregar_nota,
    materias_ofertadas,
    estudiantes_en_comun
)


def pausa():
    input(
        "\nPresione Enter para continuar..."
    )


def mostrar_tabla(estudiantes):

    print(
        f"{'ID':<5}"
        f"{'NOMBRE':<25}"
        f"{'EMAIL':<30}"
        f"{'CARNET':<15}"
        f"{'PROMEDIO':<10}"
    )

    print("-" * 85)

    for estudiante in estudiantes:

        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<30}"
            f"{estudiante.carnet:<15}"
            f"{estudiante.obtener_promedio():<10}"
        )

    print("-" * 85)

    imprimir_info(
        f"Total: {len(estudiantes)} "
        "estudiante(s)"
    )


# ========================================
# 1. CREAR
# ========================================

def opcion_crear():

    imprimir_titulo(
        "CREAR NUEVO ESTUDIANTE"
    )

    datos = {}

    for campo in CAMPOS_ESTUDIANTE:

        datos[campo] = input(
            f"{campo.capitalize()}: "
        )

    exito, mensaje = crear_estudiante(
        datos
    )

    if exito:
        imprimir_exito(mensaje)

    else:
        imprimir_error(mensaje)

    pausa()


# ========================================
# 2. VER TODOS
# ========================================

def opcion_ver_todos():

    imprimir_titulo(
        "LISTA DE ESTUDIANTES"
    )

    estudiantes = obtener_todos()

    if not estudiantes:

        imprimir_info(
            "Todavía no hay estudiantes."
        )

    else:

        mostrar_tabla(estudiantes)

    pausa()


# ========================================
# 3. BUSCAR
# ========================================

def opcion_buscar():

    imprimir_titulo(
        "BUSCAR ESTUDIANTE"
    )

    termino = input(
        "Nombre, apellido, email o carnet: "
    )

    encontrados = buscar_estudiantes(
        termino
    )

    if not encontrados:

        imprimir_info(
            "No se encontraron resultados"
        )

    else:

        mostrar_tabla(encontrados)

    pausa()


# ========================================
# 4. VER POR ID
# ========================================

def opcion_ver_por_id():

    imprimir_titulo(
        "VER ESTUDIANTE POR ID"
    )

    try:

        id_estudiante = int(
            input(
                "Id del estudiante: "
            )
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        pausa()

        return

    estudiante = obtener_por_id(
        id_estudiante
    )

    if estudiante is None:

        imprimir_error(
            "El estudiante no existe"
        )

    else:

        print(
            f"ID: {estudiante.id}"
        )

        print(
            "Nombre:",
            estudiante.obtener_nombre_completo()
        )

        print(
            f"Email: {estudiante.email}"
        )

        print(
            f"Carnet: {estudiante.carnet}"
        )

        print(
            "Materias:",
            ", ".join(
                sorted(estudiante.materias)
            )
            if estudiante.materias
            else "Ninguna"
        )

        print(
            "Promedio:",
            estudiante.obtener_promedio()
        )

    pausa()


# ========================================
# 5. ACTUALIZAR
# ========================================

def opcion_actualizar():

    imprimir_titulo(
        "ACTUALIZAR ESTUDIANTE"
    )

    try:

        id_estudiante = int(
            input(
                "Id del estudiante: "
            )
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        pausa()

        return

    estudiante = obtener_por_id(
        id_estudiante
    )

    if estudiante is None:

        imprimir_error(
            "El estudiante no existe"
        )

        pausa()

        return

    imprimir_info(
        "Editando a "
        + estudiante.obtener_nombre_completo()
    )

    print(
        "Deje vacío lo que "
        "no quiera cambiar.\n"
    )

    cambios = {}

    for campo in CAMPOS_ESTUDIANTE:

        actual = getattr(
            estudiante,
            campo
        )

        nuevo = input(
            f"{campo.capitalize()} "
            f"[{actual}]: "
        ).strip()

        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = (
        actualizar_estudiante(
            id_estudiante,
            cambios
        )
    )

    if exito:
        imprimir_exito(mensaje)

    else:
        imprimir_error(mensaje)

    pausa()


# ========================================
# 6. ELIMINAR
# ========================================

def opcion_eliminar():

    imprimir_titulo(
        "ELIMINAR ESTUDIANTE"
    )

    try:

        id_estudiante = int(
            input(
                "Id del estudiante: "
            )
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        pausa()

        return

    estudiante = obtener_por_id(
        id_estudiante
    )

    if estudiante is None:

        imprimir_error(
            "El estudiante no existe"
        )

        pausa()

        return

    imprimir_info(
        f"Se eliminará: {estudiante}"
    )

    if confirmar(
        "¿Confirma la eliminación?"
    ):

        exito, mensaje = (
            eliminar_estudiante(
                id_estudiante
            )
        )

        if exito:
            imprimir_exito(mensaje)

        else:
            imprimir_error(mensaje)

    else:

        imprimir_info(
            "Operación cancelada"
        )

    pausa()


# ========================================
# 7. AGREGAR NOTA
# ========================================

def opcion_agregar_nota():

    imprimir_titulo(
        "AGREGAR NOTA"
    )

    try:

        id_estudiante = int(
            input(
                "Id del estudiante: "
            )
        )

        nota = float(
            input(
                "Nota (0 - 20): "
            )
        )

    except ValueError:

        imprimir_error(
            "El id y la nota "
            "deben ser números"
        )

        pausa()

        return

    materia = input(
        "Materia: "
    )

    exito, mensaje = agregar_nota(
        id_estudiante,
        materia,
        nota
    )

    if exito:
        imprimir_exito(mensaje)

    else:
        imprimir_error(mensaje)

    pausa()


# ========================================
# 8. VER PROMEDIO
# ========================================

def opcion_ver_promedio():

    imprimir_titulo(
        "VER PROMEDIO"
    )

    try:

        id_estudiante = int(
            input(
                "Id del estudiante: "
            )
        )

    except ValueError:

        imprimir_error(
            "El id debe ser un número entero"
        )

        pausa()

        return

    estudiante = obtener_por_id(
        id_estudiante
    )

    if estudiante is None:

        imprimir_error(
            "El estudiante no existe"
        )

    else:

        print(
            "Estudiante:",
            estudiante.obtener_nombre_completo()
        )

        print(
            "Promedio:",
            estudiante.obtener_promedio()
        )

        print()

        if estudiante.notas:

            print(
                "Notas por materia:"
            )

            for materia, notas in (
                estudiante.notas.items()
            ):

                print(
                    f"  {materia}: {notas}"
                )

        else:

            imprimir_info(
                "Todavía no tiene notas"
            )

    pausa()


# ========================================
# 9. MATERIAS OFERTADAS
# ========================================

def opcion_materias():

    imprimir_titulo(
        "MATERIAS OFERTADAS"
    )

    materias = materias_ofertadas()

    if not materias:

        imprimir_info(
            "Todavía no existen materias"
        )

    else:

        for materia in sorted(
            materias
        ):

            print(
                f"- {materia}"
            )

    pausa()


# ========================================
# 10. MATERIAS EN COMÚN
# ========================================

def opcion_materias_comun():

    imprimir_titulo(
        "MATERIAS EN COMÚN"
    )

    try:

        id_a = int(
            input(
                "Id del primer estudiante: "
            )
        )

        id_b = int(
            input(
                "Id del segundo estudiante: "
            )
        )

    except ValueError:

        imprimir_error(
            "Los ids deben ser números"
        )

        pausa()

        return

    exito, resultado = (
        estudiantes_en_comun(
            id_a,
            id_b
        )
    )

    if not exito:

        imprimir_error(resultado)

    elif not resultado:

        imprimir_info(
            "No tienen materias en común"
        )

    else:

        print(
            "Materias en común:"
        )

        for materia in sorted(
            resultado
        ):

            print(
                f"- {materia}"
            )

    pausa()


def salir():

    imprimir_info(
        "¡Hasta luego!"
    )

    return "salir"


# DICCIONARIO:
# tecla -> (texto, función)

OPCIONES = {

    "1": (
        "Crear estudiante",
        opcion_crear
    ),

    "2": (
        "Ver todos",
        opcion_ver_todos
    ),

    "3": (
        "Buscar estudiante",
        opcion_buscar
    ),

    "4": (
        "Ver estudiante por ID",
        opcion_ver_por_id
    ),

    "5": (
        "Actualizar estudiante",
        opcion_actualizar
    ),

    "6": (
        "Eliminar estudiante",
        opcion_eliminar
    ),

    "7": (
        "Agregar nota",
        opcion_agregar_nota
    ),

    "8": (
        "Ver promedio",
        opcion_ver_promedio
    ),

    "9": (
        "Materias ofertadas",
        opcion_materias
    ),

    "10": (
        "Materias en común",
        opcion_materias_comun
    ),

    "0": (
        "Salir",
        salir
    )
}


def mostrar_menu():

    imprimir_titulo(
        "SISTEMA ACADÉMICO - ESTUDIANTES"
    )

    for tecla, datos in OPCIONES.items():

        texto = datos[0]

        print(
            f"  {tecla}. {texto}"
        )

    print()


def main():

    while True:

        mostrar_menu()

        tecla = input(
            "Seleccione una opción: "
        ).strip()

        if tecla not in OPCIONES:

            imprimir_error(
                "Opción no válida"
            )

            pausa()

            continue

        texto, funcion = (
            OPCIONES[tecla]
        )

        resultado = funcion()

        if resultado == "salir":
            break


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\nPrograma interrumpido "
            "por el usuario."
        )