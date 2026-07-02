from Buses import *



def case1():
    num_cargadores(3)

    dispatcher_thread_manual  = threading.Thread(
    target=dispatcher,
    args=(bus_queue_manual,),
    daemon=True
    )

    dispatcher_thread_manual.start()
    generate_buses_manual(5,10,0.05)

def case2():

    num_cargadores(5)

    dispatcher_thread_manual  = threading.Thread(
    target=dispatcher,
    args=(bus_queue_manual,),
    daemon=True
    )

    dispatcher_thread_manual.start()
    generate_buses_manual(5, 100, 0.05)

def case3():

    num_cargadores(5)

    dispatcher_thread_manual  = threading.Thread(
    target=dispatcher,
    args=(bus_queue_manual,),
    daemon=True
    )

    dispatcher_thread_manual.start()
    generate_buses_manual(20,20,0.05)

def case4():

    num_cargadores(1)

    dispatcher_thread_manual  = threading.Thread(
    target=dispatcher,
    args=(bus_queue_manual,),
    daemon=True
    )

    dispatcher_thread_manual.start()
    generate_buses_manual(5,50,0.05)

def case5():

    num_cargadores(5)

    dispatcher_thread_cons  = threading.Thread(
    target=dispatcher,
    args=(bus_queue_cons,),
    daemon=True
    )

    dispatcher_thread_cons.start()
    generate_buses_cons(5,0.05)

def test1(bus):
    assert(len(bus) == 5)
    print("Test #1 passed: len(bus) == 5")

def test2(bus):
    for i in range(5):
        assert(bus[i] == 0)
        print("Test passed: bus[{}] == 0".format(i))

def test3(bus):
    fill_module(bus, 0)
    assert(bus[0] == 100)
    print("Test #3 passed: bus[0] == 100 after fill_module()")

def test4(bus):
    fill_module(bus, 0)
    assert(bus[0] == 100)
    fill_module(bus, 0)
    assert(bus[0] == 100)
    print("Test #4 passed: bus[0] == 100 after multiple fills")

def test5(bus):
    fill_module(bus, 1)
    assert(bus[1] == 100)
    fill_module(bus, 2)
    assert(bus[2] == 100)
    print("Test #5 passed: bus[1] and bus[2] == 100 after fill_module()")


bus_test = bus(5)

"""
test1(bus_test)
test2(bus_test)
test3(bus_test)
test4(bus_test)
test5(bus_test)
"""


inicio = time.perf_counter()
#REMPLAZAR POR CASE A MEDIR TIEMPO DE EJECUCION
case1()
while threading.active_count() > 2:
    time.sleep(0.1)
fin = time.perf_counter()
print(f"Tiempo de ejecución: {fin - inicio:.3f} segundos")

