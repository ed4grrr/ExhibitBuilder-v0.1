

class Action:
    def __init__(self, object):
        self.actions = self.getMemberNamesAndDocstrings(object)


    def extractAllFunctionsFromClass(self, classObject):
        functions = []
        for name in dir(classObject):
            attribute = getattr(classObject, name)
            if callable(attribute):
                functions.append(attribute)
        return functions
    

    def extractAllPublicMembersFromClass(self, classObject):
        members = []
        for name in dir(classObject):
            attribute = getattr(classObject, name)
            if not name.startswith("__") and not name.startswith("_"):
                members.append(attribute)
        return members

    def getMemberNames(self, classObject):
        member_names = []
        for name in dir(classObject):
            if not name.startswith("__") and not name.startswith("_"):
                member_names.append(name)
        return member_names
    
    def getMemberNamesAndDocstrings(self, classObject):
        member_names = []
        for name in dir(classObject):
            if not name.startswith("__") and not name.startswith("_"):
                member_names.append((name, getattr(classObject, name).__doc__))
        return member_names
    """
    button has 
    wait_for_press
    wait_for_release
    is_pressed
    
    """