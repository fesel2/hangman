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
        self.surf.fill((46,52,54))
        self.rect = self.surf.get_rect()


class Counter():
    def __init__(self) -> None:
        self.level = 5

    def mistake(self):
        self.level -= 1

class Button():
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font, bg=(194,163,25)):
        self.x, self.y = pos
        self.letter = text
        self.font = pygame.font.SysFont("Arial", font)
        self.text = self.font.render(self.letter, 1, pygame.Color("White"))
        
        self.feedback(bg)
        
    def feedback(self, bg="black"):
        """Change the button when you click"""

        self.size = (40,40)
        self.surface = pygame.Surface((40,40))
        self.surface.fill(bg)
        self.surface.blit(self.text, (10, 5))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])        
        
    def show(self):
        screen.blit(self.surface, (self.x, self.y))
        
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    # dataFrame operation: changes to True in visible column if letter in word                    
                    df_word.loc[df_word["letter"]== self.letter, "visible"]= True
                    self.feedback((145,69,43))

# make the game
pygame.init()

# window settings
SCREENWIDTH = 800
SCREENHEIGHT = 500
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])

#initial settings
def init():
    random.seed(17)
    global new_word, font, hangman, alphabet_data, df_word, button_list
    new_word = Word()
    hangman = Counter()
    font = pygame.font.SysFont(None, 60)
    # create data storage if visible or not
    
    df_word = pd.DataFrame({
        "letter": new_word.make_list(),
        "visible": [False for i in range(len(new_word.make_list()))]
        })
    
    alphabet_data = pd.read_csv("alphabet.csv")
    
    button_list = []

    for index, row in alphabet_data.iterrows():
        button = Button(str(row[2]), (row[0], row[1]), font = 30)
        button_list.append(button)

    # button1 = Button(
    # "e",
    # (500, 100),
    # font=30,
    # bg="navy")


    

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
            for button in button_list:
                button.click(event)
         

        # fill background 
        screen.fill((46,52,54))

        # render button
        for button in button_list:
            button.show() 

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

