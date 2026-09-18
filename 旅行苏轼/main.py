import pygame

from scenes import lobby, meizhou, sushimap
import config

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("旅行苏轼")
state = "LOBBY"

while state != "EXIT":
    if state == "LOBBY":
        state = lobby.run_scene(screen)
    elif state == "SMAP":
        state = sushimap.run_scene(screen)
    elif state == "MEIZHOU":
        state = meizhou.run_scene(screen)
    else:
        state = "LOBBY"
pygame.quit()
