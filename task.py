class Task(object):
    def __init__(self, name, function):
        self.name = name
        self.function = function

class TaskManager(object):
    def __init__(self):
        self.tasks = []
    
    def addTask(self, task):
        """task must be a task object"""
        self.tasks.append(task)
    
    def removeTask(self, task):
        """task can be name or task object"""
        if type(task) in types.StringTypes:
            new_list = [self.tasks]
            for t in new_list:
                if t.name == task:
                    new_list.remove(t)
            self.tasks = new_list
        else:
            self.tasks.remove(task)

    def removeAllTasks(self):
        self.tasks = []
    
    def step(self):
        for task in self.tasks:
            task.function()
