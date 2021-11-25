import pygame

from canvas import Canvas
from mouse import Mouse
def main():

    background_colour = (255, 255, 255)
    (width, height) = (600, 600)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    canvas = Canvas(screen, 0, 0, 600, 600)
    mouse = Mouse(pygame.mouse.get_pos(), 10)


    running = True
    draw = False
    while running:

        mouse.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if mouse.pressed:
                if canvas.contains(*mouse.pos):
                    canvas.draw(mouse.pos, mouse.prev_pos, mouse.stroke_width)

            if pygame.mouse.get_pressed()[2]:
                print(canvas.to_binary())

        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
   main()