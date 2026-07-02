# error_deadlock_parametrico.py
import threading
import time

N = 5   # buses
K = 2   # cargadores, debe ser menor que N
M = 3   # módulos por bus, debe ser mínimo 2

assert N > K, "Debe cumplirse N > K"
assert K >= 1, "Debe haber al menos 1 cargador"
assert M >= 2, "Debe haber al menos 2 módulos para producir espera anidada"

chargers = [1] * K
chargers_mutex = threading.Lock()

# Solo los primeros K buses llegan a esta barrera,
# porque solo ellos alcanzan a tomar un cargador.
module_barrier = threading.Barrier(K)


def bus(n: int) -> list[int]:
    return [0] * n


def fill_module(bus_modules: list[int], i: int):
    while bus_modules[i] < 100:
        bus_modules[i] += 20
        print(f"[{threading.current_thread().name}] CURRENT BUS: {bus_modules}")
        time.sleep(0.2)


def acquire_charger(chargers_list: list[int]):
    with chargers_mutex:
        for i in range(len(chargers_list)):
            if chargers_list[i] == 1:
                chargers_list[i] = 0
                return i
    return None


def thread_function(bus_modules: list[int], chargers_list: list[int]):
    acquired_chargers = []

    for module_index in range(len(bus_modules)):
        charger_index = None

        while charger_index is None:
            charger_index = acquire_charger(chargers_list)

            if charger_index is None:
                print(f"[{threading.current_thread().name}] no charger available, waiting...")
                time.sleep(1)

        acquired_chargers.append(charger_index)
        print(f"[{threading.current_thread().name}] acquired charger {charger_index} for module {module_index + 1}")

        fill_module(bus_modules, module_index)

        print(f"[{threading.current_thread().name}] finished module {module_index + 1}: {bus_modules}")

        if module_index == 0:
            print(f"[{threading.current_thread().name}] keeps charger {charger_index} and waits at barrier")
            module_barrier.wait()

        # ERROR INTENCIONAL:
        # No libera el cargador después de cargar el módulo.
        # Intenta tomar otro cargador para el siguiente módulo.
        # Esto produce deadlock cuando los primeros K buses retienen todos los cargadores.

    print(f"[{threading.current_thread().name}] finished all modules: {bus_modules}")

    for _ in acquired_chargers:
        # En el deadlock nunca llega aquí.
        pass


buses = [bus(M) for _ in range(N)]

threads = []

for i in range(N):
    thread = threading.Thread(
        target=thread_function,
        args=(buses[i], chargers),
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

else:
    print("\nNo se detectó deadlock.")