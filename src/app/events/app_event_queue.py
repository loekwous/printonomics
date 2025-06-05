import queue
import logging

from .app_events import AppEvent


class EventQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def put(self, event: AppEvent):
        """Put an event in the queue."""
        self.queue.put(event)
        logging.debug(f"Event {event} added to the queue.")

    def get(self):
        """Get an event from the queue."""
        try:
            event = self.queue.get_nowait()
            logging.debug(f"Event {event} retrieved from the queue.")
            return event
        except queue.Empty:
            return None
