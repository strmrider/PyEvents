import uuid

def _get_id():
    return str(uuid.uuid4()).replace('-', '')

##################
# Event Emitter
##################

class Subscription:
    """
     Maintains a reference to the subscription
    """
    def __init__(self, emitter_id, sub_id, unsub_method):
        self.__emitter_id = emitter_id
        self.__sub_id = sub_id
        self.__unsub = unsub_method

    def unsubscribe(self):
        """
        Removes event subscription
        """
        self.__unsub(self.__sub_id)

    def __str__(self):
        """
        Subscription data
        """
        return "Event emitter: {}, subscription: {}".format(self.__emitter_id, self.__sub_id)

class Subscriber:
    """
    Contains subscriber data
    """
    def __init__(self, _id, func, calls):
        self.__id = _id
        self.__func = func
        self.__calls = calls
        self.__total_calls = 0

    def call(self, *args, **kwargs):
        """
        call the subscribed function and returns whether future calls are available
        """
        self.__func(*args, **kwargs)
        if self.__calls and self.__calls > 0:
            self.__total_calls += 1
            if self.__calls == self.__total_calls:
                return True
        return False

    def get_id(self):
        return self.__id

    def is_func(self, func):
        """
        Compares given function with the subscriber
        """
        return self.__func == func


class EventEmitter:
    """
    Handles single event by subscription
    """
    def __init__(self):
        self.__subscribers = []
        self.__emitter_id = _get_id()
        self.__max_subs = 0

    def subscribe(self, func, calls=None):
        """
        Subscribes a function. calls means number of maximum function calls.
        Any none positive number means infinite number of calls
        """
        if len(self.__subscribers) == self.__max_subs > 0:
            raise Exception('A max number of subscribers is set to {}'.format(self.__max_subs))
        method_id = _get_id()
        new_sub = Subscriber(method_id, func, calls)
        self.__subscribers.append(new_sub)

        return Subscription(self.__emitter_id, method_id, self.__unsub)

    def __unsub(self, sub_id):
        """
        Unsbubscribe method. Invoked from the Subscription reference
        """
        for subscriber in self.__subscribers:
            if subscriber.get_id() == sub_id:
                self.__subscribers.remove(subscriber)
                break

    def emit(self, *args, **kwargs):
        """
        Emits the event. All subscribed functions are called with the provided parameters
        """
        for subscriber in self.__subscribers:
            calls_over = subscriber.call(*args, **kwargs)
            if calls_over:
                self.__subscribers.remove(subscriber)

    def set_max(self, max_subs=0):
        """
        Set a maximum number of function subscriptions. 0 or less means no limit
        """
        self.__max_subs = max_subs

    def clear(self):
        """
        Clears all subscriptions
        """
        self.__subscribers = []

    def get_subscribers(self):
        """
        Returns a list containing all subscriptions
        """
        return self.__subscribers


##################
# Event Listener
##################

# subscriber alias
Listener = Subscriber

class EventListener:
    """
    Handles multiple events per event name
    """
    def __init__(self):
        self.__events = {}

    def on(self, event, listener, calls=0):
        """
        Registers a listener to an event. calls means number of maximum function calls.
        Any none positive number means infinite number of calls
        """
        new_listener = Listener(0, listener, calls)
        if event in self.__events:
            self.__events[event].append(new_listener)
        else:
            self.__events[event] = [new_listener]

    def trigger(self, event, *args, **kwargs):
        """
        Triggers a given event. All registered listeners are invoked with the provided parameters
        """
        if event in self.__events:
            listeners = self.__events[event]
            for listener in listeners:
                calls_over = listener.call(*args, **kwargs)
                if calls_over:
                    self.__events[event].remove(listener)

    def remove_listener(self, event, listener):
        """
        Removes a listener from an event
        """
        if event in self.__events:
            listeners = self.__events[event]
            for _listener in listeners:
                if _listener.is_func(listener):
                    listeners.removes(_listener)

    def remove_all_listeners(self, events:list):
        """
        Receives a list of events and removes all of their registered listeners
        """
        for event in events:
            if event in self.__events:
                self.__events[event] = []

    def clear_listeners(self):
        """
        Clears all registered listeners from all of the events
        """
        for event in events:
            self.__events[event] = []

    def clear_all(self):
        """
        Clears all events
        """
        self.__events = {}

    def get_listeners(self, event):
        """
        Returns all the listeners of a given event
        """
        return self.__events[event]


##################
# Observers
##################

class Observable:
    def __init__(self):
        self.__observers = []

    def attach(self, observer):
        """
        Attaches an observer
        """
        self.__observers.append(observer)

    def detach(self, observer):
        """
        Detaches an observer
        """
        self.__observers.remove(observer)

    def _notify_observers(self, *args, **kwargs):
        """
        Notify listed observers with given parameters
        """
        for observer in self.__observers:
            observer.notify(*args, **kwargs)

class Observer:
    def __init__(self, subject):
        subject.attach(self)

    # abstract method
    def notify(self, *args, **kwargs):
        """
        Observer's update method. must be overridden to meet user's requirements
        """
        raise Exception('Abstract method')
