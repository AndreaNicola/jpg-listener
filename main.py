import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from pathlib import Path, PurePath


class MyEventHandler(FileSystemEventHandler):

    def __init__(self, write_path):
        self.write_path = write_path

    def on_moved(self, event):
        logging.debug("Something has been moved... nothing to do! %s", event.src_path)

    def on_created(self, event):
        logging.debug("Something has been created... %s", event.src_path)
        filename = str(event.src_path)
        if filename.endswith(".jpg"):
            wp = str(PurePath(Path(self.write_path), Path(filename)))
            logging.info("New jpg file in %s, Creating thumbnail in %s", event.src_path, wp)
            image = Image.open(filename)
            max_size = (320, 240)
            image.thumbnail(max_size)
            image.save(wp)

    def on_deleted(self, event):
        logging.debug("Something has been deleted... nothing to do! %s", event.src_path)

    def on_modified(self, event):
        logging.debug("Something has been modified... nothing to do! %s", event.src_path)


def logic():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    read_path = sys.argv[0] if len(sys.argv) > 1 else '.'
    write_path = sys.argv[1] if len(sys.argv) > 2 else 'thumbnails'
    event_handler = MyEventHandler(write_path)
    observer = Observer()
    observer.schedule(event_handler, read_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    logic()
