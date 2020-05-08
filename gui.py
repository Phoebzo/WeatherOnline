#empty

import pygame


class interface:
    def __init__(self):
        self.window = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Weather Online App")
        self.icon = pygame.image.load("Globe-icon.png")
        pygame.display.set_icon(self.icon)
        self.sun_b = pygame.image.load("Sun-button.png")
        self.sun_b_pos = (1000, 125)
        self.data_b = pygame.image.load("Data-button.png")
        self.data_b_pos = (self.sun_b_pos[0],self.sun_b_pos[1]+225)
        self.graph_b = pygame.image.load("Sun-button.png")
        self.graph_b_pos = (self.data_b_pos[0],self.data_b_pos[1]+225)
        self.buttons = [(self.sun_b, self.sun_b_pos), (self.data_b, self.data_b_pos), (self.graph_b, self.graph_b_pos)]

        pygame.init()

    def run(self):
        running = True
        while running:
            self.window.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.sun_b.get_pressed():
                    self.sun()
                elif self.data_b.get_pressed():
                    self.data()
                elif self.graph_b.get_pressed():
                    self.graph()

        self.draw_all()
        pygame.display.update()

    def draw_all(self):
        for button in self.buttons:
            self.window.blit(button[0], button[1])

    def sun(self):
        pass

    def data(self):
        pass

    def graph(self):
        pass
                    

