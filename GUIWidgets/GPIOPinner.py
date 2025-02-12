
class NoAvailablePinsException(Exception):
    """A custom exception to be thrown when no available GPIO pins are found"""
    def init(self, message):
        self.message = message
        super().__init__(self.message)


class ComponentNotFoundException(Exception):
    """A custom exception to be thrown when a pin is already assigned"""
    def init(self, message):
        self.message = message
        super().__init__(self.message)


class PinAlreadyAssignedException(Exception):
    """A custom exception to be thrown when a pin is already assigned"""
    def init(self, message):
        self.message = message
        super().__init__(self.message)
    
# todo add crud operations for the assigned pins
class GPIOPinner:
    # a class to handle assigning the available Raspberry pi (BCM Numbering GPI pin) GPIO pins to the various components automatically to assure the appropriate pins are used and pins are not double-assigned or incorrectly assigned.
    def __init__(self):
        self.GPIOPins = { # a dictionary of the available GPIO pins on the Raspberry Pi in BCM numbering
            1: '3.3V Power',
            2: '5V Power',
            3: '2',
            4: '5V Power',
            5: '3',
            6: 'Ground',
            7: '4',
            8: '14',
            9: 'Ground',
            10: '15',
            11: '17',
            12: '18',
            13: '27',
            14: 'Ground',
            15: '22',
            16: '23',
            17: '3.3V Power',
            18: '24',
            19: '10',
            20: 'Ground',
            21: '9',
            22: '25',
            23: '11',
            24: '8',
            25: 'Ground',
            26: '7',
            27: None,
            28: None,
            29: '5',
            30: 'Ground',
            31: '6',
            32: '12',
            33: '13',
            34: 'Ground',
            35: '19',
            36: '16',
            37: '26',
            38: '20',
            39: 'Ground',
            40: '21'
        }

        self.usedPins = {} # a list of the pins that have been assigned to a component

        self.assignedpins = { # a dictionary of assigned GPIO pins to their components
            1: '3.3V Power',
            2: '5V Power',
            3: '',
            4: '5V Power',
            5: '',
            6: 'Ground',
            7: '',
            8: '',
            9: 'Ground',
            10: '',
            11: '',
            12: '',
            13: '',
            14: 'Ground',
            15: '',
            16: '',
            17: '3.3V Power',
            18: '',
            19: '',
            20: 'Ground',
            21: '',
            22: '',
            23: '',
            24: '',
            25: '',
            26: '',
            27: None,
            28: None,
            29: '',
            30: '',
            31: '',
            32: '',
            33: '',
            34: 'Ground',
            35: '',
            36: '',
            37: '',
            38: '',
            39: 'Ground',
            40: ''
        }
        self.currentlyRentedPins = [] # a list of the pins that have been returned using returnFirstAvailablePin method. This is used to allow for calling the returnFirstAvailablePin method multiple times without returning the same pin multiple times.

    def removeCurrentlyRentedPin(self, pin:int):
        """ a method to remove a pin from the currentlyRentedPins list
        
        This method removes a pin from the currentlyRentedPins list. This method is used to allow for calling the returnFirstAvailablePin method multiple times without returning the same pin multiple times.
        Args:
            pin (int): the pin to remove from the currentlyRentedPins list
            """
        if pin in self.currentlyRentedPins:
            self.currentlyRentedPins.remove(pin)



    def returnFirstAvailablePin(self)->list[int,str]:
        """ A method to return the first available GPIO pin in BCM numbering"""
        for pin in self.assignedpins.keys():
            if self.assignedpins[pin] == "" and pin not in self.currentlyRentedPins:
                self.currentlyRentedPins.append(pin)
                return self.GPIOPins[pin]
        raise NoAvailablePinsException("No available GPIO pins to assign")
    

        
    def unasignPin(self, component:str):
        """ a method to unassign a GPIO pin from a component
        
        This method unassigns a GPIO pin from a component. This method returns the GPIO pin number in BCM numbering if the pin is available, otherwise it throws a PinAlreadyAssignedException.
        Args:
            component (str): the name of the component to unassign a GPIO pin from
            """
        for pin in self.assignedpins.keys():
            if self.assignedpins[pin] == component:
                self.assignedpins[pin] = ""
                self.usedPins.pop(pin)
                return 
        raise ComponentNotFoundException(f"The provided componponent {component} was not found in the assigned pins dictionary")


    def assignPinManually(self, component:str, pin:int):
        """ a method to assign a GPIO pin to a component manually
        
        This method assigns a GPIO pin to a component manually. This method returns the GPIO pin number in BCM numbering if the pin is available, otherwise it throws a PinAlreadyAssignedException.
        Args:
            component (str): the name of the component to assign a GPIO pin to
            pin (int): the GPIO pin number in BCM numbering to assign to the component
            """
        if self.assignedpins[pin] != "":
            raise PinAlreadyAssignedException(f"The pin {pin} is already assigned to a component {self.assignedpins[pin]}")
        if self.GPIOPins[pin] not in [None, "3.3V Power", "5V Power", "Ground"] and self.assignedpins[pin] == "":
            self.assignedpins[pin] = component
            self.usedPins[pin] = component
            if pin in self.currentlyRentedPins:
                self.currentlyRentedPins.remove(pin)
            return self.GPIOPins[pin]
        
        # Maybe this is not necessary, but CYA
        raise NoAvailablePinsException(f"Provided pin {pin} cannot be assigned to the component {component}")

    def assignPinAutomatically(self, component:str )->int | None:
        """ a method to assign a GPIO pin to a component automatically without double-assigning or incorrectly assigning pins
        
        This method assigns a GPIO pin to a component automatically without double-assigning or incorrectly assigning pins to power or ground. This method does not account for special devices like I2C or SPI devices that require specific pins. This method returns the GPIO pin number in BCM numbering if a pin is available, otherwise it throws a NoAvailablePinsException.
        Args:
            component (str): the name of the component to assign a GPIO pin to
            """
        
        # a method to assign a GPIO pin to a component
        # TODO: account for special devices like I2C or SPI devices that require specific pins and features enabled within the Raspberry Pi OS.
        for pin in self.assignedpins.keys():
            if self.GPIOPins[pin] not in [None, "3.3V Power", "5V Power", "Ground"] and self.assignedpins[pin] == "":
                self.assignedpins[pin] = component
                self.usedPins[pin] = component
                return self.GPIOPins[pin]
        raise NoAvailablePinsException(f"No available GPIO pins to assign to the component {component}")


if __name__ == "__main__":
    # a test to check if the class works as expected
    gpiopinner = GPIOPinner()
    print(gpiopinner.assignPinAutomatically("blueLED1"))
    print(gpiopinner.assignPinAutomatically("greenLED1")) 
    print(gpiopinner.assignPinAutomatically("yellowLED1")) 
    print(gpiopinner.assignPinAutomatically("purpleLED1")) 
    print(gpiopinner.assignPinAutomatically("greenLED2")) 
    print(gpiopinner.assignPinAutomatically("redButton1")) 
    print(gpiopinner.assignPinAutomatically("magentaButton1")) 
    print(gpiopinner.assignPinAutomatically("redLED2")) 
    print(gpiopinner.assignPinAutomatically("redLED3")) 
    print(gpiopinner.assignPinAutomatically("redLED4")) 
    print(gpiopinner.assignPinAutomatically("redLED5")) 
    print(gpiopinner.assignPinAutomatically("redLED2")) 
    print(gpiopinner.assignPinAutomatically("redLED3")) 
    print(gpiopinner.assignPinAutomatically("redLED4")) 
    print(gpiopinner.assignPinAutomatically("redLED5")) 
    print(gpiopinner.assignPinAutomatically("redLED2")) 
    print(gpiopinner.assignPinAutomatically("redLED3")) 
    print(gpiopinner.assignPinAutomatically("redLED4")) 
    print(gpiopinner.assignPinAutomatically("redLED5")) 
    print(gpiopinner.assignPinAutomatically("redLED2")) 
    print(gpiopinner.assignPinAutomatically("redLED3")) 
    print(gpiopinner.assignPinAutomatically("redLED4")) 
    print(gpiopinner.assignPinAutomatically("redLED5")) 
    print(gpiopinner.assignPinAutomatically("redLED2")) 
    print(gpiopinner.assignPinAutomatically("redLED3")) 
    print(gpiopinner.assignPinAutomatically("redLED4")) 
    print(gpiopinner.assignPinAutomatically("redLED5")) 