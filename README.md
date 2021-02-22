# PyEvents
Simple Python events handling system

## Features
* Single events handler
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
* **`subscribe (self, func, calls=None)`**
* **`emit(self, *args, **kwargs)`**
* **`set_max(max_subs=0)`**
* **`clear()`**
* **`get_subscribers()`**

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
* **`trigger(event, *args, **kwargs)`**
* **`remove_listener(event, listener)`**
* **`remove_all_listeners(events)`**
* **`get_listeners(event)`**

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
```
Output:
```
subject's property was updated to 5
```
