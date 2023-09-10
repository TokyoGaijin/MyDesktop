import pygame
import pygame.freetype
import colorswatch as cs
import sqlite3
import os
import pyautogui
import time

pygame.init()
pygame.font.init()

SCREEN_X, SCREEN_Y = 1760, 990
SURFACE = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
BG = cs.cornflower_blue["pygame"]
FPS = 60
CLOCK = pygame.time.Clock()
BASE_DIR = os.path.dirname(__file__)


class SystemMenuBar:
    class SubMenu:
        def __init__(self, posX, posY, menu_name, width = 30):
            self.posX, self.posY = posX, posY
            self.menu_name = menu_name
            self.selected = False
            self.selected_color = cs.purple_rain["pygame"]
            self.unselected_color = cs.light_gray["pygame"]
            self.font = pygame.font.Font(os.path.join(BASE_DIR, "fonts", "ChicagoFLF.ttf"), 12)
            self.unselected_font_color = (0, 0, 0)
            self.selected_font_color = (255, 255, 255)
            self.current_font_color = self.unselected_font_color
            self.current_color = self.unselected_color
            self.rect = pygame.Rect(posX, posY, width, 30)
            self.is_mouse_over = False
            
        def on_click(self):
            pyautogui.alert("Under Construction")
            
        def update(self):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.is_mouse_over = True
                if pygame.mouse.get_pressed()[0]:
                    self.on_click()
            else:
                self.is_mouse_over = False
                    
            
            if self.is_mouse_over:
                self.current_color = self.selected_color
                self.current_font_color = self.selected_font_color
            else:
                self.current_color = self.unselected_color
                self.current_font_color = self.unselected_font_color
                
        def draw(self):
            pygame.draw.rect(SURFACE, self.current_color, self.rect)
            text = self.font.render(self.menu_name, True, self.current_font_color)
            SURFACE.blit(text, (self.posX + 5, self.posY + 10))
            
    class ShutDownCommand(SubMenu):
        def __init__(self, posX, posY, menu_name, width = 30):
            super().__init__(posX, posY, menu_name, width)
            
        def on_click(self):
            result = pyautogui.confirm("Are you sure you want to shut down?", buttons=["Yes", "No"])
            if result == "Yes":
                exit(1)
            
            
        
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.system_menu = self.SubMenu(self.posX + 70, self.posY, "System", width = 57)
        self.run_menu = self.SubMenu(self.posX + 70 + self.system_menu.rect.width, self.posY, "Run", width = 35)
        self.settings_menu = self.SubMenu(self.posX + 70 + self.system_menu.rect.width + self.run_menu.rect.width, self.posY, "Settings", width = 65)
        self.help_menu = self.SubMenu(self.posX + 70 + self.system_menu.rect.width + self.run_menu.rect.width + self.settings_menu.rect.width, self.posY, "Help", width = 38)
        self.shut_down_menu = self.ShutDownCommand(self.help_menu.posX + self.help_menu.rect.width, self.posY, "Shut Down", width = 80)
        self.rect = pygame.Rect(posX, posY, SCREEN_X, self.system_menu.rect.height)
        self.color = self.system_menu.unselected_color
        
        #Teehee
        
    def update(self):
        self.system_menu.update()
        self.run_menu.update()
        self.settings_menu.update()
        self.help_menu.update()
        self.shut_down_menu.update()
        
        
    def draw(self):
        pygame.draw.rect(SURFACE, self.color, self.rect)
        self.system_menu.draw()
        self.run_menu.draw()
        self.settings_menu.draw()
        self.help_menu.draw()
        self.shut_down_menu.draw()
            


system_menu = SystemMenuBar(0, 0)


def draw():
    system_menu.draw()


def update():
    CLOCK.tick(FPS)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (keys[pygame.K_LCTRL] and keys[pygame.K_q]):
            exit(1)
            

            
    draw()
    
    system_menu.update()
    pygame.display.update()
    SURFACE.fill(BG)
    
def run():
    while True:
        update()
        
if __name__ == '__main__':
    run()