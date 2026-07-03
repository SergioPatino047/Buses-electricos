from queue import Queue
import threading
import time

#FUNCION QUE INICIALIZA EL SEMAFORO CON EL NUMERO DE CARGADORES
def num_cargadores(k: int):
    global semaphore
    semaphore = threading.Semaphore(k)

#FUNCION QUE GENERA UNA LISTA DE MODULOS DE CARGA PARA EL BUS
def bus(n: int) -> list[int]:
    modulos: list[int] = [0] * n
    return modulos

#FUNCION QUE LLENA LOS MODULOS DE CARGA DEL BUS
def fill_module(bus: list[int],i:int):
    while bus[i] < 100:
        bus[i] += 20
        if bus[i] > 100:
            bus[i] = 100
        print(f"[{threading.current_thread().name}] Bus: {bus}")
    return bus

#FUNCION QUE SIMULA EL PROCESO DE CARGA DE UN BUS PARA UN HILO
def thread_function(bus):

    print(f"[{threading.current_thread().name}] started charging")
    for i in range(len(bus)):
        fill_module(bus, i)
    print(f"[{threading.current_thread().name}] finished charging")

    semaphore.release()

#FUNCION QUE CREA UN HILO POR BUS
def threads_buses(num_modules, bus_id):

    bus_instance = bus(num_modules)

    return threading.Thread(
        target=thread_function,
        args=(bus_instance,),
        name=f"Bus-{bus_id}"
    )

#FUNCION QUE GENERA BUSES DE FORMA CONSTANTE Y LOS AGREGA A LA COLA
def generate_buses_cons(num_modules,time_sleep):
    bus_id = 1
    while True:
        thread = threads_buses(num_modules, bus_id)
        bus_queue_cons.put(thread)
        print(f"[Generator] Bus-{bus_id} arrived.")
        bus_id += 1
        time.sleep(time_sleep)  

#FUNCION QUE GENERA BUSES DE FORMA MANUAL Y LOS AGREGA A LA COLA
def generate_buses_manual(num_modules, num_buses, time_sleep):
    bus_id = 1
    while bus_id <= num_buses:
        thread = threads_buses(num_modules, bus_id,)
        bus_queue_manual.put(thread)
        print(f"[Generator] Bus-{bus_id} arrived.")
        bus_id += 1
        time.sleep(time_sleep)  

#FUNCION QUE RECIBE LOS BUSES DE LA COLA Y LOS INICIA
def dispatcher(bus_queue):

    while True:

        thread = bus_queue.get()

        semaphore.acquire()

        thread.start()

        bus_queue.task_done()

#NUMERO DE CARGADORES
num_cargadores(5)

#INSTANCIAS DE COLA MANUAL Y CONSTANTE
bus_queue_manual = Queue()
bus_queue_cons = Queue()

#HILO EN SEGUNDO PLANO QUE RECIBE LOS BUSES Y LOS INICIA DE FORMA CONSTANTE
"""dispatcher_thread_cons  = threading.Thread(
    target=dispatcher,
    args=(bus_queue_cons,),
    daemon=True
)

dispatcher_thread_cons.start()
generate_buses_cons(5,0.05)
"""


#HILO EN SEGUNDO PLANO QUE RECIBE LOS BUSES Y LOS INICIA DE FORMA MANUAL
dispatcher_thread_manual  = threading.Thread(
    target=dispatcher,
    args=(bus_queue_manual,),
    daemon=True
)

dispatcher_thread_manual.start()
generate_buses_manual(5, 3,0.05)