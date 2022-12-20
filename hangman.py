import random
import sys
import pygame

# get the words from file 
with open("new_words.txt") as file:
    word_list = []
    for line in file:
        word_list.append(line)

# extract one random word
def get_word():
    number = random.randint(0, len(word_list))
    return word_list[number]

print(type(get_word()))

# make the game
pygame.init()

