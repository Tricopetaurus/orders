import sys
from .orders import main

if __name__ == '__main__':
    couriers_path = './orders.py'
    filename = './output.gif'
    if len(sys.argv) > 1:
        couriers_path = sys.argv[1]
    else:
        print(f'Loading default path {couriers_path}')
    if len(sys.argv) > 2:
        filename = sys.argv[2]
    else:
        print(f'Using default filename {filename}')
    main(couriers_path, filename)
