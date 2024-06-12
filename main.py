import pygame
import sys
import videoDetection
import calib
import squatDetection1cam
import curlDetection1cam

pygame.init()

# Set up display
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fitness App')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_input_box(surface, x, y, w, h, text=''):
    pygame.draw.rect(surface, WHITE, (x, y, w, h))
    pygame.draw.rect(surface, BLACK, (x, y, w, h), 2)
    text_surface = font.render(text, True, BLACK)
    surface.blit(text_surface, (x + 5, y + 5))

def main():
    global screen

    nbCameras = ''
    exoType = None
    repetitions = ''
    sets = ''
    calibrate_cameras = ''

    input_active = None
    running = True

    while running:
        screen.fill(GRAY)
        draw_text('Select Options', font, BLACK, screen, 20, 20)

        draw_text('Number of Cameras:', font, BLACK, screen, 50, 100)
        draw_input_box(screen, 300, 100, 100, 40, nbCameras)

        draw_text('Exercise Type (1 for Curl, 2 for Squat):', font, BLACK, screen, 50, 200)
        draw_input_box(screen, 500, 200, 100, 40, str(exoType) if exoType is not None else '')

        draw_text('Number of Reps:', font, BLACK, screen, 50, 300)
        draw_input_box(screen, 300, 300, 100, 40, repetitions)

        draw_text('Number of Sets:', font, BLACK, screen, 50, 400)
        draw_input_box(screen, 300, 400, 100, 40, sets)

        if nbCameras == '2':
            draw_text('Do you want to calibrate the cameras? (1 for yes, 2 for no):', font, BLACK, screen, 50, 500)
            draw_input_box(screen, 750, 500, 100, 40, calibrate_cameras)

        pygame.draw.rect(screen, BLUE, (50, 550, 200, 40))
        draw_text('Start', font, WHITE, screen, 100, 560)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 300 <= mx <= 400 and 100 <= my <= 140:
                    input_active = 'nbCameras'
                elif 500 <= mx <= 600 and 200 <= my <= 240:
                    input_active = 'exoType'
                elif 300 <= mx <= 400 and 300 <= my <= 340:
                    input_active = 'repetitions'
                elif 300 <= mx <= 400 and 400 <= my <= 440:
                    input_active = 'sets'
                elif 750 <= mx <= 850 and 500 <= my <= 540:
                    input_active = 'calibrate_cameras'
                elif 50 <= mx <= 250 and 550 <= my <= 590:  # Start button
                    if nbCameras == '' or exoType is None or repetitions == '' or sets == '':
                        print("Please fill in all fields.")
                    else:
                        if nbCameras == '1':
                            if exoType == 1:
                                curlDetection1cam.main(int(repetitions), int(sets))
                            elif exoType == 2:
                                squatDetection1cam.main(int(repetitions), int(sets))
                        elif nbCameras == '2':
                            if calibrate_cameras == '1':
                                calib.main()
                            videoDetection.main(cam1, cam2, exoType, int(sets), int(repetitions))
                            input_active = None  # Clear input focus
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        pass  # Ignore return key press
                    elif event.key == pygame.K_BACKSPACE:
                        if input_active == 'nbCameras':
                            nbCameras = nbCameras[:-1]
                        elif input_active == 'exoType':
                            exoType = None
                        elif input_active == 'repetitions':
                            repetitions = repetitions[:-1]
                        elif input_active == 'sets':
                            sets = sets[:-1]
                        elif input_active == 'calibrate_cameras':
                            calibrate_cameras = calibrate_cameras[:-1]
                    else:
                        if input_active == 'nbCameras':
                            nbCameras += event.unicode
                        elif input_active == 'exoType':
                            if event.unicode.isdigit():
                                exoType = int(event.unicode)
                        elif input_active == 'repetitions':
                            repetitions += event.unicode
                        elif input_active == 'sets':
                            sets += event.unicode
                        elif input_active == 'calibrate_cameras':
                            if event.unicode.isdigit():
                                calibrate_cameras += event.unicode
        pygame.display.flip()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
