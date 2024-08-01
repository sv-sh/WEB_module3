import os
import shutil
import argparse
from pathlib import Path
#from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import logging
from time import time
#import concurrent.futures

parser = argparse.ArgumentParser(description="Copying and sorting files in directories of the extensions")
parser.add_argument("--source", "-s", help="Source directory", required=True)
parser.add_argument("--destination", "-dst", help="Destination directory", default="sorted")

args = vars(parser.parse_args())  # {'source': 'dump', 'destination': 'sorted'}
src = args.get("source")
dst = args.get("destination")
count = 0
files = set()

def get_files_set(src: Path):
    for dir_path, dirnames, filename in os.walk(src):
        for file in filename:
            files.add(Path(dir_path) / file)
        for dir in dirnames:
              var = Path(dir_path)/dir
              if var.is_symlink():
                 if var.is_dir():
                    files.update(get_files_set(var))
    return files

def copy_file(file: Path):
    global count
    ext = file.suffix[1:].lower()
    path_dst = Path(dst) / ext
    if not os.path.exists(path_dst):
        os.makedirs(path_dst)
    target_file = path_dst / file.name
    try:
        shutil.copyfile(file, target_file)
        count += 1
    except Exception as err:
        logging.info(f"Error: {err}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(threadName)s - %(message)s')
    start = time()
    src_files = get_files_set(Path(src))

    # with ThreadPoolExecutor() as executor: #2024-07-26 17:30:37,392 - MainThread - Processed: 67 files in  0.05495190620422363
    #     features = [executor.submit(copy_file,file) for file in src_files]
    #     [concurrent.futures.as_completed(feature) for feature in features]


    # threads = []  # 2024-07-19 17:02:03,126 - MainThread - Processed: 69 files in 0.21259760856628418 seconds
    # for file in src_files:
    #     th = Thread(target=copy_file, args=(file,))
    #     threads.append(th)
    #     th.start()
    #     logging.info(th)
    # [thr.join() for thr in threads]
   
    with ThreadPoolExecutor() as executor: # 2024-07-26 17:28:32,905 - MainThread - Processed: 69 files in 0.05957365036010742 seconds
        list(executor.map(copy_file, src_files))
    logging.info(f"Processed: {count} files in {time() - start} seconds")

