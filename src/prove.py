from hulk_parser.hulk_parser import hulk_build
import time

start_time = time.time()
print(hulk_build())
end_time = time.time()

execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time} segundos")