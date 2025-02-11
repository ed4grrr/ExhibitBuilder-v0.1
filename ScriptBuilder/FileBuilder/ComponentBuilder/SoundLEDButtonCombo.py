from gpiozero import Button, LED
import pygame

class SoundLEDButtonCombo:

    def __init__(self, name:str, GPIO_LED: int, GPIO_Button:int, audio_File_Path:str, volume:float, isDuringPress:bool):
        
        self.name = name
        self.Current_Volume = volume  # Default volume
        pygame.mixer.music.set_volume(self.Current_Volume)
        self.MyButton=Button(GPIO_Button)
        self.MyLED = LED(GPIO_LED)
        self.isDuringPress = isDuringPress

        self.MyButton.when_pressed = self.playduringPress if isDuringPress else self.playAfterPress
        
        self.mySound =pygame.mixer.Sound(audio_File_Path)
    
    
    def playSong(self):
        self.mySound.play()

    def playAfterPress(self):
    
        self.playSong()
        #this keeps the led on until the audio quits playing.
        while self.isPlaying():
            self.MyLED.on()
        self.cleanUpAfterButtonRelease()

    def playduringPress(self):
        self.playSong()
        while self.MyButton.is_pressed:
            self.MyLED.on()
        self.cleanUpAfterButtonRelease()

    
    def cleanUpAfterButtonRelease(self):
        self.stopSong()
    
        self.MyLED.off()

    def stopSong(self):
        self.mySound.stop()

    

    def isPlaying(self):
        return pygame.mixer.music.get_busy()



    def isPressed(self):
        return self.MyButton.is_pressed

    def isReleased(self):
        return self.MyButton.is_released

    def isHeld(self):
        return self.MyButton.is_held

    def cleanUp(self):
        self.MyButton.close()
        self.MyLED.close() 
        self.stopSong()

    def __repr__(self):
        return f"SoundLEDButtonCombo({self.name},{self.MyLED.pin},{self.MyButton.pin},{self.mySound},{self.Current_Volume},{self.isDuringPress})"