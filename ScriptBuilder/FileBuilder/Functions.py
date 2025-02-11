

SLBComboCreatorFunctionString = """def createSLDBCombos( listOfNames:list[str],listofButtonGPIO:list[int], listofLEDGPIO:list[int], listofAudioFiles:list[str], volume:list[float], isDuringPress:bool)->list[SoundLEDButtonCombo.SoundLEDButtonCombo]:

    returnable = []
    for name, button,led,audio,volume in zip(listOfNames,listofButtonGPIO,listofLEDGPIO,listofAudioFiles,volume):
        returnable.append(SoundLEDButtonCombo.SoundLEDButtonCombo(name, button, led, audio, volume, isDuringPress))
    return returnable"""