import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def main():
    """
    main function of spacefight, the game. I will add more and more functinality here
    as I continue to code the game.
    """

    # Initialize the game
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SpaceFight")

    # set up the game clock
    clock = pygame.time.Clock()

    # Set up font
    font = pygame.font.Font(
        None, 36
    )  # None is the default font, 36 is the size of the font

    # Game loop
    running = True
    while running:
        # event handiing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # game logic will go here

        # draw the game
        screen.fill((0, 0, 0))

        #render the text
        text = font.render("SpaceFight", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text, text_rect)

        # update the display
        pygame.display.flip()

        # tick the clock
        clock.tick(60)

    # Quit the game
    pygame.quit()


if __name__ == "__main__":
    main()
