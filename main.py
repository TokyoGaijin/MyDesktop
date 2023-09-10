import pygame
import pygame.freetype
import colorswatch as cs
import sqlite3
import os
import pyautogui
import time
import tkinter as tk
from tkinter.simpledialog import askstring
import subprocess

pygame.init()
pygame.font.init()

SCREEN_X, SCREEN_Y = 1760, 990
SURFACE = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
BG = cs.cornflower_blue["pygame"]
FPS = 60
CLOCK = pygame.time.Clock()
BASE_DIR = os.path.dirname(__file__)

def input_dialog(header, prompt):
    root = tk.Tk()
    root.withdraw()
    
    result = askstring(header, prompt)
    
    return result


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
            
    class AppsMenu(SubMenu):
        def __init__(self, posX, posY, menu_name, width = 35):
            super().__init__(posX, posY, menu_name, width)
            self.apps_icon = pygame.image.load(os.path.join(BASE_DIR, "png_icons", "mac.png"))
            self.selected_icon = pygame.image.load(os.path.join(BASE_DIR, "png_icons", "mac_selected.png"))
            self.current_icon = self.apps_icon
            self.rect = pygame.Rect(posX, posY, self.apps_icon.get_width(), self.apps_icon.get_height())
            self.apps_list = []
            
        def on_click(self):
            if len(self.apps_list) <= 0:
                pyautogui.alert("No applications installed.")
            
        def update(self):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.is_mouse_over = True
                if pygame.mouse.get_pressed()[0]:
                    self.on_click()
            else:
                self.is_mouse_over = False
                
            if self.is_mouse_over:
                self.current_icon = self.selected_icon
            else:
                self.current_icon = self.apps_icon
            
        def draw(self):
            SURFACE.blit(self.current_icon, (self.posX, self.posY))
            
    class SystemMenu(SubMenu):
        def __init__(self, posX, posY, menu_name, width = 57):
            super().__init__(posX, posY, menu_name, width)
            ## TODO: Add drop-down menu
            
        ## TODO: Add new on_click command
        
    class RunMenu(SubMenu):
        def __init__(self, posX, posY, menu_name, width = 35):
            super().__init__(posX, posY, menu_name, width)
            ## TODO: Add drop-down menu
            
        def on_click(self):
            path_to_open = input_dialog("Run", "Type in the destination path.")
            try:
                subprocess.Popen(path_to_open)
            except Exception as e:
                pyautogui.alert("Program not found.")
    
    
    class SettingsMenu(SubMenu):
        def __iniit__(self, posX, posY, menu_name, width = 75):
            super().__init__(posX, posY, menu_name, width)
            ## TODO: Add drop-down menu
            
        ## TODO: add new on_click command    
        
        
    class HelpMenu(SubMenu):
        def __init__(self, posX, posY, menu_name, width = 38):
            super().__init__(posX, posY, menu_name, width)
            ## TODO: Add drop-down Menu
            
        ## TODO: add new on_click command
            
                
    class ShutDownCommand(SubMenu):
        def __init__(self, posX, posY, menu_name, width = 80):
            super().__init__(posX, posY, menu_name, width)
            
        def on_click(self):
            result = pyautogui.confirm("Are you sure you want to shut down?", buttons=["Yes", "No"])
            if result == "Yes":
                exit(1)
                
            
            
        
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.apps_menu = self.AppsMenu(30, 0, "Apps")
        self.system_menu = self.SystemMenu(self.posX + 70, self.posY, "System")
        self.run_menu = self.RunMenu(self.system_menu.posX + self.system_menu.rect.width, self.posY, "Run")
        self.settings_menu = self.SettingsMenu(self.run_menu.posX + self.run_menu.rect.width, self.posY, "Settings", width = 65)
        self.help_menu = self.HelpMenu(self.settings_menu.posX + self.settings_menu.rect.width, self.posY, "Help")
        self.shut_down_menu = self.ShutDownCommand(self.help_menu.posX + self.help_menu.rect.width, self.posY, "Shut Down")
        self.rect = pygame.Rect(posX, posY, SCREEN_X, self.system_menu.rect.height)
        self.color = self.system_menu.unselected_color
        
        
    def update(self):
        self.system_menu.update()
        self.run_menu.update()
        self.settings_menu.update()
        self.help_menu.update()
        self.shut_down_menu.update()
        self.apps_menu.update()
        
        
    def draw(self):
        pygame.draw.rect(SURFACE, self.color, self.rect)
        self.apps_menu.draw()
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