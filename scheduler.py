import uuid, threading, datetime


DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

_notify_execution = None

def _get_args_value(key, obj, false_value):
    return obj[key] if key in  obj else false_value

def build_date(**kwargs):
    """
    Builds a date according to the format.
    :param kwargs: int; year, month, day, hour, minute, second.
                    Sets current time for non given parameter
    :return: datetime;
    """
    values = kwargs.values()
    for value in values:
        if not isinstance(value, int):
            raise Exception("All values must be of integer type")

    now = datetime.datetime.now()
    str_date = "{}/{}/{} {}:{}:{} {}".format(_get_args_value('day', kwargs, now.day),
                                             _get_args_value('month', kwargs, now.month),
                                             _get_args_value('year', kwargs, now.year),
                                             _get_args_value('hour', kwargs, now.hour),
                                             _get_args_value('minute', kwargs, now.minute),
                                             _get_args_value('second', kwargs, now.second),
                                             DATE_FORMAT)
    return datetime.datetime.strptime(str_date,'%d/%m/%Y %H:%M:%S')

class Task:
    """
    Scheduled Task. Runs a task in a given time, whether a specific date or number of seconds
    """
    def __init__(self, **kwargs):
        """
        Creates a task
        :param kwargs: (callable) func; the task to be called when time is arrived
                       (any) args; the args to be passed with the task function (must be aligned with task's signature)
                       timing methods (one must be provided):
                       (datetime) date: a specific date on which the task will be executed
                       (int) sleep: number of seconds to wait until the task is executed
        """
        self.__id = str(uuid.uuid4()).replace('-', '')
        self.__callback = _get_args_value('func', kwargs, None)
        self.__args = _get_args_value('args', kwargs, None)
        self.__schedule = _get_args_value('date', kwargs, None)
        self.__sleep = _get_args_value('sleep', kwargs, None)

        self.__event = threading.Event() if self.__sleep else None

        self.__is_running = False
        self.__done = False
        self.__check_validity()

    def __check_validity(self):
        """
        Checks whether task's parameters are set and valid
        :return: throws exceptions
        """
        if not self.__callback:
            raise Exception("Task function is not provided")
        if not self.__schedule and not self.__sleep:
            raise Exception("Task timing is not provided")
        if self.__schedule and self.__sleep:
            raise Exception("Can't have multiple timing methods")
        if self.__schedule and not isinstance(self.__schedule, datetime.datetime):
            raise Exception("Date must be of datetime type")
        if self.__sleep and not isinstance(self.__sleep, int):
            raise Exception("Sleep timing must be an integer")

    def get_id(self):
        """
        task's id getter
        """
        return self.__id

    def is_running(self):
        """
        Returns whether the timing is running
        """
        return self.__is_running

    def is_done(self):
        """
        Returns whether the task has been already executed
        """
        return self.__done

    def __timeout(self):
        """
        Calculates task's timeout
        :return: bool
        """
        now = datetime.datetime.now()
        diff = self.__schedule - now
        mode = divmod(diff.days * (20 * 60 * 60) + diff.seconds, 60)

        return mode == (0, 0)

    def __set_done(self):
        """
        Sets task as done
        """
        self.__is_running = False
        self.__done = True
        global _notify_execution
        if _notify_execution:
            _notify_execution(self.__id)

    def __call_func(self):
        """
        Calls task's function
        """
        if self.__args:
            self.__callback(self.__args)
        else:
            self.__callback()

    def run(self):
        """
        Runs task depending on its timing method
        """
        if self.__is_running:
            return
        elif self.is_done():
            raise Exception("Task has already been executed")
        elif self.__sleep:
            threading.Thread(target=self.__run_sleep).start()
        elif self.__timeout():
            self.__set_done()
            self.__call_func()
        else:
            threading.Thread(target=self.__run).start()

    def __run(self):
        """
        Runs timing by specific date
        """
        self.__is_running = True
        while self.__is_running:
            if self.__timeout():
                self.__done = True
                self.__call_func()
                break

    def __run_sleep(self):
        """
        Runs by waiting/sleep method. Rerun will start from the beginning and not from remaining time
        """
        self.__is_running = True
        self.__event.wait(self.__sleep)
        if self.__is_running:
            self.__call_func()
            self.__set_done()

    def stop(self):
        """
        Stop task's timing
        """
        self.__is_running = False
        if self.__sleep:
            self.__event.set()

class TasksManager:
    """
    Task manager
    """
    def __init__(self):
        self.__tasks = {}
        global _notify_execution
        _notify_execution =  self.remove_task

    def size(self):
        """
        Returns number of available tasks
        :return: int
        """
        return len(self.__tasks)

    def add_task(self, task):
        """
        Adds a task to the manager
        :param task: Task
        """
        if task.get_id() not in self.__tasks:
            self.__tasks[task.get_id()] = task
        else:
            raise Exception("Task already exists")

    def new_task(self, **kwargs):
        """
        Creates new task, adds it to the manager and returns it to the user
        :param kwargs: Task arguments
        :return: Task
        """
        task = Task(**kwargs)
        self.__tasks[task.get_id()] = task
        return task

    def remove_task(self, task_id):
        """
        Removes task and returns it to the user
        :param task_id: (str); task's is
        :return: Task
        """
        task = self.__tasks[task_id]
        if task:
            task.stop()
            del self.__tasks[task_id]
        return task

    def get_task(self, task_id):
        """
        Returns a task
        :param task_id: str; task's id
        :return: Task
        """
        return self.__tasks[task_id]

    def clear(self):
        """
        Clears all tasks of the manager
        """
        self.stop_all()
        self.__tasks = {}

    def stop_all(self):
        """
        Stops all running tasks
        """
        tasks = self.__tasks.values()
        for task in tasks:
            task.stop()

    def run_all(self):
        """
        Runs all tasks
        """
        tasks = self.__tasks.values()
        for task in tasks:
            if not task.is_done():
                task.run()
