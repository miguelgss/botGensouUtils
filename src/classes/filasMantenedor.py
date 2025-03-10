class FilasMantenedor():
    isGroupListLocked = False
    areListsLooping = False
    groupList = [[]]
    waitList = []

    def __init__(self):
        self.groupList = [[]]
        self.waitList = []