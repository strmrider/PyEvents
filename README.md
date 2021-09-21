# PyEvents
Simple Python events handling system

## Features
* Single event handler
* Multiple events handler
* Observer pattern
* Task scheduler

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

    Subscribes a function. *calls* means the number of maximum function calls. Any none positive number means an infinite number of calls.

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
    
    Registers a listener to an event. *calls* means the number of maximum function calls. Any none positive number means an infinite number of calls.

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
        print(f"subject's property was updated to {number}")

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

    Subscribes a function. *calls* means the number of maximum function calls. Any none positive number means an infinite number of calls.

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
    
    Registers a listener to an event. *calls* means the number of maximum function calls. Any none positive number means an infinite number of calls.

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
        print(f"subject's property was updated to {number}")

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

### Task scheduling
#### Task
Task has two timing options: A specific date or number of seconds to wait.
```Python
from .schedule import *

# task's callback
def done(text):
    print(f'{text} task is done')
    
# sleep method    
sleep_task = Task(sleep=60, func=done, arg='sleep')

# schedule date
# create date
new_date = datetime.datetime.strptime('15/04/2019 12:21:00', DATE_FORMAT)
# or use a date builder
new_date = build_date(year=2019, month=4, day=15, hour=12, minute=21, second=0)

date_task = Task(date=new_date, func=done, arg='date')

sleep_date.run()
date_task.run()
```
Output
```
sleep task is done
date task is done
```
##### API
* **`Task(**kwargs)`**
    
    Creates a task. Receives timing method data: seconds (int) for 'sleep' or datetime type for 'date' (at least one method must be provided); 
    task callback function for 'func' (mandatory); 'arg' is any type of argument (optional, but must be aligned with task's callback function's signature)

* **`get_id()`**
    
    Returns task's id.
    
* **`is_running()`**

    Returns whether the timing is running.
    
* **`is_done()`**

    Returns whether the task has been already executed.

* **`run()`**

    Runs the task depending on its timing method.

* **`stop()`**

    Stop task's timing.
    
#### Task manager
Handles multiple tasks. Tasks are automatically removed from the manager after execution.
```Python
manager = TasksManager()
manager.add_task(sleep_task)
manager.add_task(date_task)
manager.run_all()
```
Output
```
sleep task is done
date task is done
```
##### API
* **`new_task(**kwargs)`**
    
    Creates a new task, adds it to the manager and returns it to the user. Receives the same arguments as Task type.

* **`add_task(task)`**
    
    Adds a task to the manager.
    
* **`remove_task(task_id)`**
    
    Removes a task by given id and returns it to the user.
    
* **`get_task(task_id)`**

    Returns a task by id.
    
* **`clear()`**

    Clears manager of all tasks.

* **`run_all()`**

    Runs all tasks.

* **`stop_all()`**

    Stops all running tasks.

