class FilasMantenedor():
    def __init__(self):
        self.groupList = [[]]
        self.waitList = []
        self._listeners = []
        self.isGroupListLocked = False
        self.areListsLooping = False

    def add_listener(self, callback):
        self._listeners.append(callback)

    def notify_listeners(self):
        for callback in self._listeners:
            callback()
