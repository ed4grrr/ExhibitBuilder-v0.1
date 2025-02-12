1. Currently, editing an IU will force a new set of GPIO pins to be requested
    This clearly needs to fill a locked entry box with teh existing assigned pins

2. how can the program account for when the user closes the create element window without saving
    in regards to how GPIO pinner would account for the wasted requested pin.

Currently, having a static Pinner in the MainGUI class is the way we are going, but how to handle Pin assignments when:
    - when the user exits before creating a unit?
    - when the user opens an item to edit?
    - when a user deletes an already assigned pin?
    - when a user copy and pastes an already assigned pin?