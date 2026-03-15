import csv
import os

ARCHIVO_CSV = "estudiantes.csv"
ENCABEZADOS = ["DNI", "Nombre", "Apellido", "Notas"]

def cargar_datos():
    estudiantes = {}
    if not os.path.exists(ARCHIVO_CSV):
        return estudiantes

    with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            notas_str = fila["Notas"]
            notas_lista = [float(n) for n in notas_str.split("-")] if notas_str else []
            
            estudiantes[fila["DNI"]] = {
                "nombre": fila["Nombre"],
                "apellido": fila["Apellido"],
                "notas": notas_lista
            }
    return estudiantes

def guardar_datos(estudiantes):
    with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=ENCABEZADOS)
        writer.writeheader()
        
        for dni, datos in estudiantes.items():
            notas_str = "-".join(str(n) for n in datos["notas"])
            writer.writerow({
                "DNI": dni,
                "Nombre": datos["nombre"],
                "Apellido": datos["apellido"],
                "Notas": notas_str
            })

def main():
    estudiantes = cargar_datos() 
    
    while True:
        print("\nGESTOR ACADÉMICO\n")
        opcion_select = input(
            "1. Registrar nuevo estudiante\n"
            "2. Registrar calificaciones\n"
            "3. Consultar datos de estudiantes\n"
            "4. Generar reportes y estadisticas\n"
            "5. Salir\n"
            "Selección: "
        ).strip()

        if opcion_select == "1":
            registrar_estudiante(estudiantes)
        
        elif opcion_select == "2":
            registrar_calificaciones(estudiantes)
        
        elif opcion_select == "3":
            print("\nDATOS DE ESTUDIANTES\n")
            opcion_select2 = input(
                "1. Ver listado completo (con promedios)\n"
                "2. Buscar estudiante en especifico (por DNI)\n"
                "3. Volver\n"
                "Selección: "
            ).strip()
            
            while opcion_select2 not in ["1", "2", "3"]:
                print("Nop. Por favor, ingresá 1, 2 o 3.")
                opcion_select2 = input("Selección: ").strip()
            
            if opcion_select2 == "1":
                ver_csv_promediado(estudiantes)
                
            elif opcion_select2 == "2":
                buscar_por_dni(estudiantes)
                
            elif opcion_select2 == "3":
                print("Volviendo...")
                continue 
        
        elif opcion_select == "4":
            print("\nREPORTES Y ESTADISTICAS\n")
            opcion_select3 = input(
                "1. Promedio general del curso\n"
                "2. Top 3 mejores promedios\n"
                "3. Lista ordenada alfabéticamente (por apellido)\n"
                "4. Volver\n"
                "Selección: "
            ).strip()
            
            while opcion_select3 not in ["1", "2", "3", "4"]:
                print("Nop. Por favor, ingresá 1, 2, 3 o 4.")
                opcion_select3 = input("Selección: ").strip()
            
            if opcion_select3 == "1":
                
                ver_promedio_general(estudiantes)
                
            elif opcion_select3 == "2":
                
                top_3_promedios(estudiantes)
                
            elif opcion_select3 == "3":
                
                alfabeticamente_por_apellido(estudiantes)
            
            elif opcion_select3 == "4":
                print("Volviendo...")
                continue

        
        elif opcion_select == "5":
            guardar_datos(estudiantes)
            print("Saliendo del sistema... ¡Chau!")
            break
        else:
            print("Nop. La seleccion no esta dentro de las opciones. Por favor, intenta de nuevo. ")


def registrar_estudiante(estudiantes): 
    print("\nREGISTRO DE NUEVO ESTUDIANTE")
    
    dni = input("Ingrese el DNI del estudiante (ej: 12345678): ").strip()
    while not dni.isdigit():
        print("Nop. El DNI solo puede tener números.")
        dni = input("Ingresa el DNI de nuevo: ").strip()

    while dni in estudiantes:
        print(f"Nop. Fijate que ya existe un estudiante con el DNI {dni}")
        dni = input("Ingresa un DNI distinto: ").strip()

    nombre = input("Ingrese el nombre: ").strip().title()
    
    while not nombre or not nombre.replace(" ", "").isalpha():
        print("Nop. El nombre no puede estar vacío ni tener números o símbolos.")
        nombre = input("Ingrese el nombre de nuevo: ").strip().title()
    
    apellido = input("Ingrese el apellido: ").strip().title()

    while not apellido or not apellido.replace(" ", "").isalpha():
        print("Nop. El apellido no puede estar vacío ni tener números o símbolos.")
        apellido = input("Ingrese el apellido de nuevo: ").strip().title()
        
    estudiantes[dni] = {"nombre": nombre, "apellido": apellido, "notas": []}    
    print(f"Se registró correctamente a {nombre} {apellido}.")
    guardar_datos(estudiantes)
    

def registrar_calificaciones(estudiantes):
    print("\nREGISTRO DE CALIFICACIONES")
    
    if not estudiantes:
        print("Nop. Primero tenés que tener registrado al menos un estudiante (la opción 1).")
        return

    dni = input("Ingresá el DNI del estudiante: ").strip()
    while not dni.isdigit():
        print("Nop. El DNI solo puede tener números.")
        dni = input("Ingresa el DNI de nuevo: ").strip()
    
    
    if dni not in estudiantes:
        print(f"Nop. No se encontró ningún estudiante con el DNI {dni}.")
        return 
        
    alumno = estudiantes[dni]
    print(f"\nEstudiante seleccionado: {alumno['nombre']} {alumno['apellido']}")

    while True:
        print("\n¿Qué querés hacer?")
        print("1. Agregar calificación")
        print("2. Finalizar carga para este alumno")
        opcion_sub = input("Elegí una opción (1 o 2): ").strip()

        if opcion_sub == "1":
            entrada = input(f"Ingresá la nota numérica para {alumno['nombre']}: ").strip()
            
            try:
                nota = float(entrada) 
                if 0 <= nota <= 10:
                    alumno["notas"].append(nota)
                    print(f"Se agrego el {nota} correctamente.")
                else:
                    print("Nop. La nota tiene que estar entre 0 y 10. Intentá de nuevo.")
            except ValueError:
                print("Nop. Tenés que ingresar un número (ej: 8 o 8.5). No letras.")

        elif opcion_sub == "2":
            print("Volviendo al menú principal...")
            guardar_datos(estudiantes)
            break 
            
        else:
            print("Nop. Opción inválida. Por favor ingresá 1 o 2.")
   

def ver_csv_promediado(estudiantes):
    if not estudiantes:
        print("\nNop. No hay estudiantes registrados todavía.")
        return
    
    print("\nTABLA DE ESTUDIANTES (CON PROMEDIOS)")
    print(f"{'DNI':<10} | {'NOMBRE':<15} | {'APELLIDO':<15} | {'PROMEDIO'}")
    print("-" * 60)
    
    for dni, datos in estudiantes.items():
        promedio_calculado = calcular_promedio(datos["notas"])
        print(f"{dni:<10} | {datos['nombre']:<15} | {datos['apellido']:<15} | {promedio_calculado:.2f}")
        
    print("-" * 60)
    
def calcular_promedio(notas_input):
    if not notas_input:
        return 0.0
    
    if isinstance(notas_input, str):
        notas_lista = [float(n) for n in notas_input.split("-")]
    else:
        notas_lista = notas_input
        
    return sum(notas_lista) / len(notas_lista)

def buscar_por_dni(estudiantes):
    print("\nBUSCAR ESTUDIANTE")

    if not estudiantes:
        print("Nop. Tenes que tener registrado por lo menos a un estudiante.")
        return

    dni_buscado = input("Ingresá el DNI del estudiante a buscar: ").strip()
    
    while not dni_buscado.isdigit():
        print("Nop. El DNI solo puede tener números.")
        dni_buscado = input("Ingresá el DNI de nuevo: ").strip()
    
    if dni_buscado in estudiantes:
        alumno = estudiantes[dni_buscado]
        notas = alumno["notas"]
        
        promedio = calcular_promedio(notas)
            
        print("\nESTUDIANTE ENCONTRADO:")
        print(f"{'DNI':<10} | {'NOMBRE':<15} | {'APELLIDO':<15} | {'NOTAS':<20} | {'PROMEDIO'}")
        print("-" * 81)
        
        notas_str = str(notas) 
        
        print(f"{dni_buscado:<10} | {alumno['nombre']:<15} | {alumno['apellido']:<15} | {notas_str:<20} | {promedio:.2f}")
        print("-" * 81)
        
    else:
        print(f"Nop. No se encontró ningún estudiante registrado con el DNI {dni_buscado}.")

def ver_promedio_general(estudiantes):
    print("\nPROMEDIO GENERAL DEL CURSO")
    
    if not estudiantes:
        print("Nop. No hay estudiantes registrados todavía.")
        return
        
    suma_total = 0
    
    for datos in estudiantes.values():
        promedio_alumno = calcular_promedio(datos["notas"])
        suma_total += promedio_alumno
        
    promedio_curso = suma_total / len(estudiantes)
    
    print("-" * 50)
    print(f"EL PROMEDIO GENERAL DEL CURSO ES: {promedio_curso:.2f}")
    print("-" * 50)

def top_3_promedios(estudiantes):
    print("\nTOP 3 MEJORES PROMEDIOS\n")
    
    if not estudiantes:
        print("Nop. No hay estudiantes registrados.")
        return

    lista_ranking = []
    for dni, datos in estudiantes.items():
        prom = calcular_promedio(datos["notas"])
        lista_ranking.append({
            "dni": dni,
            "nombre": datos["nombre"],
            "apellido": datos["apellido"],
            "promedio": prom
        })

    lista_ranking.sort(key=lambda x: x["promedio"], reverse=True)

    print(f"{'POS':<4} | {'DNI':<10} | {'NOMBRE':<15} | {'APELLIDO':<15} | {'PROMEDIO'}")
    print("-" * 65)
    
    top_3 = lista_ranking[:3]
    
    for i, alumno in enumerate(top_3, 1):
        print(f"{i:<4} | {alumno['dni']:<10} | {alumno['nombre']:<15} | {alumno['apellido']:<15} | {alumno['promedio']:.2f}")
    
    print("-" * 65)

def alfabeticamente_por_apellido(estudiantes):
    print("\nLISTADO ORDENADO POR APELLIDO\n")
    
    if not estudiantes:
        print("Nop. No hay estudiantes registrados.")
        return

    lista_ordenada = []
    for dni, datos in estudiantes.items():
        prom = calcular_promedio(datos["notas"])
        
        lista_ordenada.append({
            "dni": dni,
            "nombre": datos["nombre"],
            "apellido": datos["apellido"],
            "promedio": prom
        })

    lista_ordenada.sort(key=lambda x: x["apellido"].lower())

    
    print(f"{'DNI':<10} | {'APELLIDO':<15} | {'NOMBRE':<15} | {'PROMEDIO'}")
    print("-" * 57)
    
    for alumno in lista_ordenada:
        print(f"{alumno['dni']:<10} | {alumno['apellido']:<15} | {alumno['nombre']:<15} | {alumno['promedio']:>8.2f}")
    
    print("-" * 57)

if __name__ == "__main__":
    main()