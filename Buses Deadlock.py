import threading
import time

# Número de buses, cargadores y módulos por bus
N = 20
K = 10
M = 2

# Validaciones del escenario
assert N > K
assert K >= 1
assert M >= 2

# Semáforo que representa los cargadores disponibles
cargadores = threading.Semaphore(K)

# Barrera para sincronizar los primeros K buses
module_barrier = threading.Barrier(K)


def bus(n: int) -> list[int]:
    """
    Crea un bus con n módulos de batería al 0%.
    """
    return [0] * n


def fill_module(bus_modules: list[int], i: int):
    """
    Carga el módulo i hasta el 100%.
    """
    while bus_modules[i] < 100:
        bus_modules[i] += 20
        print(f"[{threading.current_thread().name}] CURRENT BUS: {bus_modules}")
        time.sleep(0.2)


def thread_function(bus_modules: list[int]):
    """
    Simula el proceso de carga de un bus.

    El bus toma un cargador, carga el módulo 1 y lo retiene.
    Luego intenta tomar un segundo cargador para el módulo 2,
    provocando un deadlock.
    """
    print(f"[{threading.current_thread().name}] intenta tomar cargador para módulo 1")

    # Toma el primer cargador
    cargadores.acquire()
    print(f"[{threading.current_thread().name}] tomó cargador para módulo 1")

    # Carga el primer módulo
    fill_module(bus_modules, 0)

    print(f"[{threading.current_thread().name}] terminó módulo 1 y retiene el cargador")

    # Espera a los demás buses
    module_barrier.wait()

    print(f"[{threading.current_thread().name}] intenta tomar OTRO cargador para módulo 2")

    # Punto donde ocurre el bloqueo
    cargadores.acquire()

    fill_module(bus_modules, 1)


# Creación de los buses
buses = [bus(M) for _ in range(N)]

# Lista de hilos
threads = []

# Creación de un hilo por cada bus
for i in range(N):
    thread = threading.Thread(
        target=thread_function,
        args=(buses[i],),
        name=f"Bus-{i + 1}",
        daemon=True
    )
    threads.append(thread)

# Inicia todos los hilos
for thread in threads:
    thread.start()

# Espera un máximo de 10 segundos por cada hilo
for thread in threads:
    thread.join(timeout=10)

# Verifica si hay hilos bloqueados
alive_threads = [thread.name for thread in threads if thread.is_alive()]

if alive_threads:
    print("\nDEADLOCK DETECTADO")
    print(f"Hilos bloqueados: {alive_threads}")
    print("Todos los cargadores quedaron retenidos y ningún bus pudo obtener un segundo.")
else:
    print("\nNo se detectó deadlock.")