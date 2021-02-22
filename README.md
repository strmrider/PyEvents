# PyEvents
Simple Python events handling system

### Features
* Single events handler
* Multiple events handler
* Observer pattern

### Examples
First create some sample functions
```Python
def print_text(text):
    print('print text function:', text)

def add(x, y):
    print (x + y)
```

#### Single event handler
```Python
from .events import EventEmitter

emitter = EventEmitter()
sub = emitter.subscribe(print_text)
lambda_sub = emitter.subscribe(lambda text:print('lambda function: ', text))

emitter.emit(text='hello')
subscription.unsubscribe()
emitter.emit(text='hello')
```
Output:
```
print text function: hello
lambda function:  hello
lambda function:  hello
```

#### Multi Events handler
```Python
from .events import EventListener

event_listener = EventListener()
event_listener.on('print', print_text)
event_listener.on('add', add)
event_listener.trigger('print', text='hello')
event_listener.trigger('add', x=4, y=12)
```
Output:
```
print text function: hello
16
```

#### Observers
```Python
class A(Observable):
    def __init__(self):
        super().__init__()
        self.a = 0

    def set_a(self, number):
        self.a = number
        self._notify_observers(a=self.a)

class B(Observer):
    def __init__(self, subject):
        super().__init__(subject)

    def notify(self, **kwargs):
        print("subject's property was updated to {}".format(kwargs['a']))

a = A()
b = B(a)
a.set_a(5)
```
Output:
```
subject's property was updated to 5
```
