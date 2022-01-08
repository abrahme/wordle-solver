# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:48:54 2022

@author: Ajay

Solver Code
"""
from utils.utils import english_dictionary
import numpy as np
letters=np.asarray(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n","o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"])


def freq_generator(word_list):
    letter_frequencies=np.zeros([5,26]) #initialize
    for i in word_list:
        for j in np.arange(len(i)):
            letter_frequencies[j,np.where(i[j] == letters)] +=1 
    return letter_frequencies
        
    
def word_scorer(word_list, letter_frequencies):
    scores_array=[]
    for i in word_list:
        total_score=0
        for j in np.arange(len(i)):
            letter_score=letter_frequencies[j,np.where(i[j] == letters)]
            total_score=total_score+letter_score
        scores_array.append(total_score)
    best_word_index=np.argmax(scores_array)
    return word_list[best_word_index]