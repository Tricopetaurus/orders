import sys
from .orders import main

if __name__ == '__main__':
    couriers_path = './orders.py'
    if len(sys.argv) > 1:
        couriers_path = sys.argv[1]
    else:
        print(f'Loading default path {couriers_path}')
    main(couriers_path)
