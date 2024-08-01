from time import time
from multiprocessing import cpu_count, Pool
import logging

def factorize(number):
    return [i for i in range(1, number +1) if number % i ==0 ]

def test(res):
    a, b, c, d = res
    logging.info(f'\n{a}\n{b}\n{c}\n{d}')
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    args =(128, 255, 99999, 10651060)
    cpu = cpu_count()
    logging.info(f'cpu count: {cpu}')

# paralel execution  time 1.156635046005249
    start_time = time()
    with Pool(processes=cpu) as pool:
        results = pool.map(factorize, args)
    logging.info(f'paralel execution time {time()- start_time}')
    test(results)

# synchronous execution  time 1.0677387714385986
    t1=time()
    results = [factorize(i) for i in args]
    logging.info(f'synchronous execution time {time()-t1}')
    test(results)
