#empty

import pygame


class Interface:
    def __init__(self):
        self.window = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Weather Online App")
        self.icon = pygame.image.load("Globe-icon.png")
        pygame.display.set_icon(self.icon)
        self.sun_b = Button("Sun-button.png", (1000, 125))
        self.data_b = Button("Data-button.png", (1000, 125+225))
        self.graph_b = Button("Sun-button.png", (1000 ,125+225+225))
        self.buttons = [self.sun_b, self.data_b, self.graph_b]

        pygame.init()

    def run(self):
        self.running = True
        while self.running:
            self.window.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1,0,0):
                        self.mouse_pos = pygame.mouse.get_pos()
                        if self.sun_b.is_pressed(self.mouse_pos):
                            self.sun()
                        elif self.data_b.is_pressed(self.mouse_pos):
                            self.data()
                        elif self.graph_b.is_pressed(self.mouse_pos):
                            self.graph()

        self.draw_all()
        pygame.display.update()

    def draw_all(self):
        for button in self.buttons:
            button.draw()

    def sun(self):
        pass

    def data(self):
        pass

    def graph(self):
        pass
                    

class Button(Interface):
    def __init__(self, path, pos):
        self.image = pygame.image.load(path)
        self.pos = pos

    def draw(self):
        super.window.blit(self.image, self.pos)

    def is_pressed(self, mouse_pos):
        if mouse_pos[0] in (self.pos[0] + 150):
            if mouse_pos[1] in (self.pos[1] + 100):
                return True
        else:
            return False