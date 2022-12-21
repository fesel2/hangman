import random
import pandas as pd
import pygame
from pygame.locals import (
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
    def __init__(self, let, font):
        self.letter = let
        self.surf = pygame.Surface((40,40))
        self.surf.fill((194,163,25))
        self.rect = self.surf.get_rect()
        self.font = font
        self.text = self.font.render(let, 1, (0,0,0))

    def guess(self):
        self.surf = pygame.Surface((100,60))



    def click(self, event):
        x,y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x,y):
                    self.guess()

class Button2:

    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.letter = "e"
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
        
    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])        
        
    def show(self):
        screen.blit(button1.surface, (self.x, self.y))
        
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    # dataFrame operation: changes to True in visible column if letter in word                    
                    df_word.loc[df_word["letter"]== self.letter, "visible"]= True

# make the game
pygame.init()

# window settings
SCREENWIDTH = 800
SCREENHEIGHT = 500
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])

#initial settings
def init():
    random.seed(17)
    global new_word, font, hangman, alphabet_data, df_word, button1
    new_word = Word()
    hangman = Counter()
    font = pygame.font.SysFont(None, 60)
    # create data storage if visible or not
    
    df_word = pd.DataFrame({
        "letter": new_word.make_list(),
        "visible": [False for i in range(len(new_word.make_list()))]
        })
    
    alphabet_data = pd.read_csv("alphabet.csv")
    
    button1 = Button2(
    "e",
    (500, 100),
    font=30,
    bg="navy",
    feedback="You clicked me")


    

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
            button1.click(event)
         

        # fill background 
        screen.fill((0,0,0))

        # render button
        button1.show() 

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

        
        
        # render counter aka hangman
        counter_img = font.render(str(hangman.level), True, (100,255,255))
        screen.blit(counter_img, (100, 350))

        

        # refresh screen
        pygame.display.flip()
    print(df_word)

    

if __name__ == "__main__":
    main()

