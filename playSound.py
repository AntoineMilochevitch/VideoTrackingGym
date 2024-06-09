from gtts import gTTS
import pygame
import threading

def play_sound(text):
    def _play_sound():
        lang = "en"
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(text + '.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(text +'.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    sound_thread = threading.Thread(target=_play_sound)
    sound_thread.start()