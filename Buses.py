import threading 
import time

def bus(n: int) -> list[int]:
    modulos: list[int] = [0] * n
    return modulos

def fill_module(bus: list[int],i:int):
    while bus[i] < 100:
        bus[i] += 1
        print(bus)
        time.sleep(1)
    return bus

def chargers(k: int) -> list[int]:
    cargadores: list[int] = [1] * k
    return cargadores

def thread_function(bus: list[int], chargers: list[int]):
    while True:
        for i in range(len(chargers)):
            if chargers[i] == 1:
                chargers[i] = 0
                for j in range(len(bus)):
                    fill_module(bus, j)
                chargers[i] = 1
                return bus
        print("No charger available, waiting...")
        time.sleep(5)