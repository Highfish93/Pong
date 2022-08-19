import pygame

WHITE = (255, 255, 255)
GREY = (60, 60, 60)
DARK_GREY = (45, 45, 45)
LIGHT_GREY = (75, 75, 75)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


class Button:
    class Font:
        def __init__(self, color, hoverColor, fontSize, bold=False):
            self.color = color
            self.hoverColor = hoverColor
            self.fontSize = fontSize
            self.bold = bold

    def __init__(self, win, x, y,width=100,height=50,text='', click=None):
        pygame.init()
        self.win = win
        self.color = DARK_GREY
        self.hoverColor = GREY
        self.x = x
        self.y = y
        if text !='':
            self.text = text
        else: self.text='Button'
        self.font = self.Font(LIGHT_GREY, WHITE, 25, False)
        self.outlineHovered = LIGHT_GREY
        self.outlineUnhovered = LIGHT_GREY
        self.pressedOutline = BLACK
        self.width = width
        self.height = height
        self.pressed = False
        self.onClick = self.clickDummy
        self.onClick = click

    def clickDummy(self):
        pass

    def draw(self):
        # Call this method to draw the button on the screen
        font = pygame.font.SysFont('Comic Sans MS', self.font.fontSize, self.font.bold)
        text = font.render(self.text, True, self.font.color)
        if self.isOver(pygame.mouse.get_pos()):
            text = font.render(self.text, True, self.font.hoverColor)
            pygame.draw.rect(self.win, self.outlineHovered, (self.x - 4, self.y - 4, self.width + 8, self.height + 8),
                             0)
            pygame.draw.rect(self.win, self.hoverColor, (self.x, self.y, self.width, self.height),
                             0)
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.win, self.pressedOutline, (self.x - 4, self.y - 4, self.width + 8, self.height + 8),
                                 0)
                pygame.draw.rect(self.win, self.hoverColor, (self.x, self.y, self.width, self.height),
                                 0)
                if not self.pressed:
                    self.pressed = True
            else:
                if self.pressed:
                    print('Im pressed')
                    self.onClick()
                    self.pressed = False
        else:
            pygame.draw.rect(self.win, self.outlineUnhovered, (self.x - 4, self.y - 4, self.width + 8, self.height + 8),
                             0)
            pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height), 0)
        self.win.blit(text,
                 (self.x + (self.width / 2 - text.get_width() / 2),
                  self.y + (self.height / 2 - text.get_height() / 2)))
        pygame.display.update()

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
