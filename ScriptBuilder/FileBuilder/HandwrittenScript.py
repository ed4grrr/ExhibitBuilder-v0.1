import ComponentBuilder.SoundLEDButtonCombo as SoundLEDButtonCombo
import signal

def createSLDBCombos( listOfNames:list[str],listofButtonGPIO:list[int], listofLEDGPIO:list[int], listofAudioFiles:list[str], volume:list[float], isDuringPress:bool)->list[SoundLEDButtonCombo.SoundLEDButtonCombo]:
    """Creates a list of SoundLEDButtonCombos
    listOfNames: list[str] - a list of names for the combos
    listofButtonGPIO: list[int] - a list of GPIO pins for the buttons
    listofLEDGPIO: list[int] - a list of GPIO pins for the LEDs
    listofAudioFiles: list[str] - a list of file paths for the audio files
    volume: float - the volume for the audio files
    isDuringPress: bool - True if the audio should play during the button press, False if it should play after the button press
    """
    returnable = []
    for name, button,led,audio,volume in zip(listOfNames,listofButtonGPIO,listofLEDGPIO,listofAudioFiles,volume):
        returnable.append(SoundLEDButtonCombo.SoundLEDButtonCombo(name, button, led, audio, volume, isDuringPress))
    return returnable

if __name__ == '__main__':

    # TODO write the user entered Names and Audio Files as lists of strings

    # this function is hardcoded
    listOfSLDBCombos = createSLDBCombos(["12_Northern mocking, bird", "11_Tufted titmouse"], [17, 27], [4, 22], ["sound_files/12_Northern mockingbird.wav", "sound_files/11_Tufted titmouse.wav"], [0.5, 0.5], True)
    signal.pause()