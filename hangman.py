import random
import pandas as pd
import pygame
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class Word():
    """core class: takes a random word from the textfile and makes it accessible"""
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
    """rectangles covering the letters which arent guessed so far"""
    def __init__(self):
        super(Hider, self).__init__()
        self.surf = pygame.Surface((50,60))
        self.surf.fill((46,52,54))
        self.rect = self.surf.get_rect()


class Counter():
    """the actual hangman"""
    def __init__(self) -> None:
        self.level = 7
        self.tag = ""

    def mistake(self):
        self.level -= 1
    
    def compare(self, letter_button):
        if letter_button in new_word.make_list():
            print("True")
        else:
            print("False")
            self.mistake()
    
    class Element():
        """used to set the hangman elements"""
        def __init__(self, path) -> None:
            self.surf = pygame.image.load(path)
            self.surf.set_colorkey((0,0,0), RLEACCEL)
            self.rect = self.surf.get_rect()
        def show(self, position):
            screen.blit(self.surf, position)

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
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (10, 5))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])        
        
    def show(self):
        screen.blit(self.surface, (self.x, self.y))
        
    def click(self, event, counter_object):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    # dataFrame operation: changes to True in visible column if letter in word                    
                    df_word.loc[df_word["letter"]== self.letter, "visible"]= True
                    self.feedback((145,69,43))
                    counter_object.compare(self.letter)

class PlayAgain(Button):
        def feedback(self, bg="black"):
            """Change the button when you click"""
            self.size = (150,40)
            self.surface = pygame.Surface(self.size)
            self.surface.fill(bg)
            self.surface.blit(self.text, (10, 5))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

        def restart(self, event):
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.rect.collidepoint(x, y):
                        # dataFrame operation: changes to True in visible column if letter in word                    
                        init()

# make the game
pygame.init()
pygame.display.set_caption('Hangman')

# window settings
SCREENWIDTH = 800
SCREENHEIGHT = 500
screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])

#initial settings
def init():
    #random.seed(17)
    global new_word, font, hangman, alphabet_data, df_word, button_list, font_small,\
        hangman_elements, hangman_positions, replay_button
    new_word = Word()
    hangman = Counter()

    # build the hangman
    hill = hangman.Element("hangman_images/hill.png")
    wood1 = hangman.Element("hangman_images/wood1.png")
    wood2 = hangman.Element("hangman_images/wood2.png")
    rope = hangman.Element("hangman_images/rope.png")
    head = hangman.Element("hangman_images/head.png")
    body = hangman.Element("hangman_images/body.png")
    arms = hangman.Element("hangman_images/arms.png")

    # positions were found by try and error
    hangman_elements = [hill, wood1, wood2, rope, head, body, arms]
    hangman_positions = [(10,350),(50,120),(100,100),(230,150),(215,180),(165,170),(165,170)]


    font = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 30)
    # create data storage if visible or not
    
    df_word = pd.DataFrame({
        "letter": new_word.make_list(),
        "visible": [False for i in range(len(new_word.make_list()))]
        })
    df_word.loc[df_word["letter"]== " ", "visible"] = True
    
    alphabet_data = pd.read_csv("alphabet.csv")
    
    button_list = []

    for index, row in alphabet_data.iterrows():
        button = Button(str(row[2]), (row[0], row[1]), font = 30)
        button_list.append(button)
    
    replay_button = PlayAgain("Play again", (450, 100), font = 30, bg= (47,69,115))

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
                button.click(event, hangman)
            replay_button.restart(event)
         

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
        hangman_level_draw = 7 - hangman.level
        for element, position in zip(hangman_elements[:hangman_level_draw], hangman_positions[:hangman_level_draw]):
            element.show(position)


        # counter
        
        if hangman.level <= 0:
            counter_str = "Game Over"            
            replay_button.show()
        elif hangman.level >= 0 and len(df_word) == df_word["visible"].sum():
            counter_str = "Congratulations, you won!"
            replay_button.show()
        else:
            counter_str = "Tries left: {}".format(hangman.level)
        counter_img = font_small.render(counter_str, True, (100,255,255))
        screen.blit(counter_img, (20, SCREENHEIGHT-30))        

        # refresh screen
        pygame.display.flip()   

if __name__ == "__main__":
    main()

