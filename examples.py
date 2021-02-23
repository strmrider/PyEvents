from events import EventEmitter, EventListener, Observable, Observer

def print_text(text):
    print('print text function:', text)

def add(x, y):
    print ('sum:', x + y)

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


# Event listener
listener  = EventListener()
listener.on('print', print_text)
listener.on('add', add)
listener.trigger('print', 'event listener triggered')
listener.trigger('add', 4, 12)

# observers
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