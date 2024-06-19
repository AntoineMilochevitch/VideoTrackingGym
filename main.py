import pygame
import pygame_gui
import sys
import videoDetection
import calib
import squatDetection1cam
import curlDetection1cam
import json
import cv2
import numpy as np

pygame.init()

# Set up display
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fitness App')

# Colors
DARK_GREEN = (75, 89, 67)
LIGHT_GREEN = (143, 180, 58)
LIGHT_GRAY = (220, 223, 218)

with open('theme.json', 'r') as f:
    theme = json.load(f)

font_path = theme['global']['font_path']
font_size = theme['global']['font_size']


# Load the theme
manager = pygame_gui.UIManager((width, height), 'theme.json')

# Set up UI elements
nbCameras_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((400, 100), (40, 40)), manager=manager, object_id='#nbCameras')
exoType_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['Curl', 'Squat'],
    starting_option='Curl',
    relative_rect=pygame.Rect((400, 200), (100, 40)),
    manager=manager,
)
repetitions_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((400, 300), (40, 40)), manager=manager, object_id='#repetitions')
sets_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((400, 400), (40, 40)), manager=manager, object_id='#sets')
calibrate_yes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 500), (50, 40)), text='Yes', manager=manager)
calibrate_no_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 500), (50, 40)), text='No', manager=manager)
calibrate_yes_button.hide()
calibrate_no_button.hide()
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 550), (150, 40)), text='Start', manager=manager)
demo_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 550), (150, 40)), text='Demo', manager=manager)

# Labels
font = pygame.font.Font(font_path, font_size)
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.flip(frame, True, False)
        frame = pygame.transform.scale(frame, (width, height))

        screen.blit(frame, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

        pygame.time.wait(10)

    cap.release()


def main():
    global screen

    calibrate_cameras = False

    running = True
    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        nbCameras = nbCameras_input.get_text()
                        exoType = exoType_dropdown.selected_option
                        repetitions = repetitions_input.get_text()
                        sets = sets_input.get_text()

                        if not nbCameras or exoType == 'Select' or not repetitions or not sets:
                            print("Please fill in all fields.")
                        else:
                            exoType_val = 1 if 'Curl' in exoType else 2
                            if nbCameras == '1':
                                if exoType_val == 1:
                                    curlDetection1cam.main(int(repetitions), int(sets))
                                elif exoType_val == 2:
                                    squatDetection1cam.main(int(repetitions), int(sets))
                            elif nbCameras == '2':
                                if calibrate_cameras:
                                    calib.main()
                                videoDetection.main(1, 2, exoType_val, int(sets), int(repetitions))

                    elif event.ui_element == calibrate_yes_button:
                        calibrate_cameras = True
                    elif event.ui_element == calibrate_no_button:
                        calibrate_cameras = False
                    elif event.ui_element == demo_button:
                        print("Demo")
                        exoType = exoType_dropdown.selected_option
                        exoType_val = 1 if 'Curl' in exoType else 2
                        if exoType_val == 1:
                            play_video('CurlTemplate.mp4')
                        elif exoType_val == 2:
                            pass
                        
            manager.process_events(event)
        nbCameras = nbCameras_input.get_text()
        if nbCameras.isdigit() and int(nbCameras) > 1:
            calibrate_yes_button.show()
            calibrate_no_button.show()
        else:
            calibrate_yes_button.hide()
            calibrate_no_button.hide()

        manager.update(time_delta)
        screen.fill(LIGHT_GRAY)

        draw_text('Select Options', font, LIGHT_GREEN, screen, 350, 20)
        draw_text('Number of Cameras:', font, LIGHT_GREEN, screen, 50, 100)
        draw_text('Exercise Type:', font, LIGHT_GREEN, screen, 50, 200)
        draw_text('Number of Reps:', font, LIGHT_GREEN, screen, 50, 300)
        draw_text('Number of Sets:', font, LIGHT_GREEN, screen, 50, 400)

        nbCameras = nbCameras_input.get_text()
        if nbCameras.isdigit() and int(nbCameras) > 1:
            draw_text('Calibrate Camera', font, LIGHT_GREEN, screen, 50, 500)


        manager.draw_ui(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
