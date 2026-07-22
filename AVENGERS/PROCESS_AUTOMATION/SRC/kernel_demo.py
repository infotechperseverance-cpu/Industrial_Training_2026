import os
import platform

def show_kernel_usage():

    print("\n========== KERNEL SPACE DEMO ==========")

    print("Operating System      :", platform.system())
    print("OS Version            :", platform.version())
    print("Machine Architecture  :", platform.machine())
    print("Processor             :", platform.processor())
    print("Current Process ID    :", os.getpid())
    print("Current Working Dir   :", os.getcwd())

    print("\nThese operations are handled by the operating system kernel.")