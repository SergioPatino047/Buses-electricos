import threading 

def bus(n: int) -> list[int]:
    modulos: list[int] = [0] * n
    return modulos

def fill_module(bus: list[int]):
    for i in range(len(bus)):
        while bus[i] < 100:
            bus[i] += 1
    return bus
        

print(fill_module(bus(5)))