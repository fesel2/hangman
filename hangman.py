import random
import pandas as pd
import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# create the core class
class Word():
    def __init__(self) -> None:
        # opens file and stores a random word in attribute .word
        with open("new_words.txt") as file:
            word_list = []
            for line in file:
                word_list.append(line)
        number = random.randint(0, len(word_list))
        self.word = word_list[number]
    
    def make_list(self):
        # list comprehension iterating over the word and taking the letters
        # slicing to get rid of \n
        return [letter for letter in self.word][:-1]
    
class Hider(pygame.sprite.Sprite):
    def __init__(self):
        super(Hider, self).__init__()
        self.surf = pygame.Surface((40,60))
        self.surf.fill((10,10,50))
        self.rect = self.surf.get_rect()


class Counter():
    def __init__(self) -> None:
        self.level = 5

    def mistake(self):
        self.level -= 1

class Button(pygame.sprite.Sprite):
    def __init__(self, let):
        self.letter = let
        self.surf = pygame.Surface((40,40))
        self.surf.fill((194,163,25))
        self.rect = self.surf.get_rect()

# make the game
pygame.init()

# window settings
SCREENWIDTH = 800
SCREENHEIGHT = 500
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])

#initial settings
def init():
    global new_word, font, hangman, alphabet_data, df_word, b1
    new_word = Word()
    hangman = Counter()
    font = pygame.font.SysFont(None, 60)
    # create data storage if visible or not
    
    df_word = pd.DataFrame({
        "letter": new_word.make_list(),
        "visible": [False for i in range(len(new_word.make_list()))]
        })
    alphabet_data = pd.read_csv("alphabet.csv")
    b1 = Button("a")


    

def main():
    init()
    running = True    

    while running:
        # options to close the game
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                    running = False
        
        # fill background 
        screen.fill((0,0,0))

        # render text
        i = 20
        for char in new_word.make_list():
            # render the letter               
            text_img = font.render(str(char), True, (100,255,255))
            screen.blit(text_img, (i, 35))

            # render the placeholder
            if char == " ":
                placeholder_img = font.render(" ", True, (100,255,255))
            else:
                placeholder_img = font.render("_", True, (100,255,255))
            screen.blit(placeholder_img, (i, 45))
            i += 40

        # render hiding obstacles
        i = 10
        for index, row in df_word.iterrows():
            if row[1] == False:
                obstacle = Hider()
                screen.blit(obstacle.surf, (i,20))
            else:
                pass
            i += 40
        
        # render counter
        counter_img = font.render(str(hangman.level), True, (100,255,255))
        screen.blit(counter_img, (100, 350))

        screen.blit(b1.surf, (500,200))
        
    

        # refresh screen
        pygame.display.flip()
    print(df_word)

    

if __name__ == "__main__":
    main()

