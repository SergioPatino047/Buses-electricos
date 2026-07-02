# error_deadlock_parametrico.py
import threading
import time

N = 7
K = 4
M = 4

assert N > K
assert K >= 1
assert M >= 2

cargadores = threading.Semaphore(K)
module_barrier = threading.Barrier(K)


def bus(n: int) -> list[int]:
    return [0] * n


def fill_module(bus_modules: list[int], i: int):
    while bus_modules[i] < 100:
        bus_modules[i] += 20
        print(f"[{threading.current_thread().name}] CURRENT BUS: {bus_modules}")
        time.sleep(0.2)


def thread_function(bus_modules: list[int]):
    print(f"[{threading.current_thread().name}] intenta tomar cargador para módulo 1")
    cargadores.acquire()
    print(f"[{threading.current_thread().name}] tomó cargador para módulo 1")

    fill_module(bus_modules, 0)

    print(f"[{threading.current_thread().name}] terminó módulo 1 y retiene el cargador")
    module_barrier.wait()

    print(f"[{threading.current_thread().name}] intenta tomar OTRO cargador para módulo 2")
    cargadores.acquire()  # Aquí queda bloqueado

    fill_module(bus_modules, 1)


buses = [bus(M) for _ in range(N)]

threads = []

for i in range(N):
    thread = threading.Thread(
        target=thread_function,
        args=(buses[i],),
        name=f"Bus-{i + 1}",
        daemon=True
    )
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join(timeout=10)

alive_threads = [thread.name for thread in threads if thread.is_alive()]

if alive_threads:
    print("\nDEADLOCK DETECTADO")
    print(f"Hilos bloqueados: {alive_threads}")
    print("Los primeros K buses tomaron todos los cargadores.")
    print("Cada uno retuvo su cargador después de cargar el módulo 1.")
    print("Luego intentaron tomar otro cargador para el módulo 2.")
    print("Como no queda ningún cargador libre, quedan bloqueados.")
else:
    print("\nNo se detectó deadlock.")