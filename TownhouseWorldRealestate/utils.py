import os
import random


def phone_random(length):
    number = '0123456789'
    #alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = '09'
    for i in range(0,length-2):
        id += random.choice(number)
        #id += random.choice(alpha)
    return id
