import pygame
import sys
from pygame.locals import *
import time
import os
from classes.tile import Tile
from classes.lab_item import LabItem, Player
from classes.labyrinth import Labyrinth, InvalidPattern


class Game:
    """
    Create the graphical environment of the game. It takes as a parameter a text file that contains the pattern
    Raise:
        IndexError: if rows and columns is not equiale to 15
        InvalidPattern: the pattern of the labyrinth does not correspond to he requests 
    """
    def __init__(self, pattern_file):
        self.tile_images = {
            'floor': pygame.image.load(os.path.join('images', 'green.png')),
            'water': pygame.image.load(os.path.join('images', 'blue.png')),
            'guard': pygame.image.load(os.path.join('images', 'black.png')),
            }

        self.item_images = {
            'player': pygame.image.load(os.path.join('images', 'octopus.png')),
            'object': pygame.image.load(os.path.join('images', 'perso.png')),
        }

        self.tile_size = 20

        try:
            self.labyrinth = Labyrinth(os.path.join('images', pattern_file))
            self.width = self.labyrinth.width
            self.height = self.labyrinth.height

            self.player = Player()
            self.labyrinth.canvas[self.player.x][self.player.y].add_lab_item(
                self.player)

            pygame.init()
            self.labyrinth.add_random_items(2)
            self.display_surface = pygame.display.set_mode(
                (self.width * self.tile_size, self.height * self.tile_size + self.tile_size))
            self.text_font = pygame.font.Font('freesansbold.ttf', 18)
        except (IndexError, InvalidPattern) as e:
            print('error: {}'.format(e))
            quit(0)
            #sys.exit(1)
        
    def display_tiles(self):
        """
        Display tile map of the labyrinth on the display screen.
        Raises:
            IndexError: if the pattern does not composed of 15 lines and 15 columns
        """
        try:
            for line in range(self.height):
                for column in range(self.width):
                    tile = self.labyrinth.canvas[line][column]
                    self.display_surface.blit(
                        self.tile_images[tile.tile_type], (column * self.tile_size, line * self.tile_size))
                    if tile.lab_item:
                        self.display_surface.blit(self.item_images[tile.lab_item.item_type], (
                            column * self.tile_size, line * self.tile_size))
        except IndexError:
            print('error: labyrinth size have to be 15 x 15.')
            quit(0)
            #sys.exit(1)

    def display_text(self, text, color, text_place):
        """
        Display text on the display screen
        Args :
            text (str): text that wanted to be displayed.
            color (tuple): RGB codes of the text color.
            text_place (tuple): the coordinates in pixels of the text position on the screen. 
        """
        text_surface = pygame.Surface((self.width * self.tile_size, self.tile_size))
        text_surface.fill((19, 157, 255))
        text_render = self.text_font.render(text, True, color) 
        self.display_surface.blit(text_surface, (0, self.height * self.tile_size))
        self.display_surface.blit(text_render, text_place)   

    def item_counter_text(self):
        """ 
        Display number of collected item on the screen   
        """     
        
        text = ' X ' + str(self.player.counter)
        text_position = (self.tile_size, self.height * self.tile_size)
        self.display_text(text, (0,0,0), text_position)
        self.display_surface.blit(self.item_images['object'], (0, self.height * self.tile_size))        
    
#    def game_over(self):
#        self.display_text('Game Over', (237, 41, 57), ((self.width * self.tile_size)/2, (self.height * self.tile_size)/2))
#        time.sleep(2)
#        quit(0)


    def run(self):
        """
        Run the game on the display screen 
        """
        while True:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == QUIT or self.labyrinth.is_winner(self.player):
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    tiles = self.labyrinth.canvas
                    if (event.key == K_RIGHT) and self.player.x < self.width - 1 and tiles[self.player.y][self.player.x + 1].tile_type == 'floor':
                        self.player.pick_up(
                            tiles[self.player.y][self.player.x + 1])
                        self.player.move_right(tiles)

                    if (event.key == K_LEFT) and self.player.x != 0 and tiles[self.player.y][self.player.x - 1].tile_type == 'floor':
                        self.player.pick_up(
                            tiles[self.player.y][self.player.x - 1])
                        self.player.move_left(tiles)

                    if (event.key == K_DOWN) and self.player.y < self.height - 1 and tiles[self.player.y + 1][self.player.x].tile_type == 'floor':
                        self.player.pick_up(
                            tiles[self.player.y + 1][self.player.x])
                        self.player.move_down(tiles)

                    if (event.key == K_UP) and self.player.y != 0 and tiles[self.player.y - 1][self.player.x].tile_type == 'floor':
                        self.player.pick_up(
                            tiles[self.player.y - 1][self.player.x])
                        self.player.move_up(tiles)

                self.display_tiles()
                self.item_counter_text()                 
                pygame.display.flip()
