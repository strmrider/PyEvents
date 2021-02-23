# PyEvents
Simple Python events handling system

## Features
* Single event handler
* Multiple events handler
* Observer pattern

## Examples
Sample functions
```Python
def print_text(text):
    print('print text function:', text)

def add(x, y):
    print ('sum:', x + y)
```

### Single event handler
```Python
from .events import EventEmitter

# Event emitter
event = EventEmitter()
# subscribe functions to the emitter
subscription = event.subscribe(print_text)
lambda_subscription = event.subscribe(lambda text: print('lambda function: ', text))
# emit event
event.emit('first event emission')
# remove subscription
subscription.unsubscribe()
event.emit('second event emission')
```
Output:
```
print text function: first event emission
lambda function:  first event emission
lambda function:  second event emission
```

#### API
* **`subscribe (self, func, calls=-1)`**

    Subscribes a function. *calls* means number of maximum function calls. Any none positive number means infinite number of calls.

* **`emit(self, *args, **kwargs)`**

    Emits the event. All subscribed functions are called with the provided parameters.

* **`set_max(max_subs=0)`**

    Set a maximum number of function subscriptions. 0 or less means no limit.

* **`clear()`**

    Clears all subscriptions.
    
* **`get_subscribers()`**

    Returns a list containing all subscriptions.

### Multiple events handler
```Python
from .events import EventListener

# Event listener
listener  = EventListener()
listener.on('print', print_text)
listener.on('add', add)
listener.trigger('print', 'event listener triggered')
listener.trigger('add', 4, 12)
```
Output:
```
print text function: event listener triggered
sum: 16
```
#### API
* **`on(event, listener, calls=0)`**
    
    Registers a listener to an event. *calls* means number of maximum function calls. Any none positive number means infinite number of calls.

* **`trigger(event, *args, **kwargs)`**
    
    Triggers a given event. All registered listeners are invoked with the provided parameters.
    
* **`remove_listener(event, listener)`**

    Removes a listener from an event.
    
* **`remove_all_listeners(events)`**

    Receives a list of events and removes all of their registered listeners.

* **`clear_listeners()`**

    Clears all registered listeners from all of the events.

* **`clear_all(events)`**

    Clears all events.

* **`get_listeners(event)`**

    Returns all the listeners of a given event.

### Observers
```Python
from events import Observable, Observer

class A(Observable):
    def __init__(self):
        super().__init__()
        self.number = 0

    def set_number(self, number):
        self.number = number
        self._notify_observers(self.number)


class B(Observer):
    def __init__(self, subject):
        super().__init__(subject)

    # must be overridden
    def notify(self, number):
        print("subject's property was updated to {}".format(number))

a = A()
b = B(a)
a.set_number(5)
a.set_number(891)
```
Output:
```
subject's property was updated to 5
subject's property was updated to 891
```
