#!/usr/bin/env python
# coding: utf-8

# # Frequency Based Solver
# The first iteration of this solver is using position based letter frequencies to determine the next best guess in a game of Wordle. The idea is that the best word to guess is the word remaining that is most likely to occur based on how often certain letters appear. It is agnostic of the green, yellow, and grey letters right now, and is only using the information from filtering the database (so indirectly affecting).
# 
# From any given database, do guesses converge here? 
# 
# To-Do
# -> better metric for 'best word', need to calculate the stats on the max freq score (mean, stdev) and maybe recommend several words that are in close scor, but this is first attempt. 

# In[1]:


from utils.utils import english_dictionary
import numpy as np


# In[2]:


#initialize the dictionary as a numpy array for no reason right now other than I'm familiar with the indexing
dic=np.asarray(english_dictionary)


# In[3]:


#first let's build code that generates the statistics for our dictionary 
#initalize letters array
letters=np.asarray(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n","o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"])


# In[4]:


letter_frequency=np.zeros([5,26]) #i decided to just start with the most sophisticated method which is considering letter frequency at each position 
for i in dic:
    for j in np.arange(len(i)):
        letter_frequency[j,np.where(i[j] == letters)] +=1 
        
        


# Now that we have letter frequency by position, we need to build a probabilistic model that calculates given a database of word, what is the 'frequency score'
# 
# In other words, what words provide the MOST information? we can calculate this easily by calculating simple 'score' that is the sum of all frequencies.

# In[5]:


def word_scorer(word_list):
    scores_array=[]
    for i in word_list:
        total_score=0
        for j in np.arange(len(i)):
            letter_score=letter_frequency[j,np.where(i[j] == letters)]
            total_score=total_score+letter_score
        scores_array.append(total_score)
    best_word_index=np.argmax(scores_array)
    return word_list[best_word_index]


# In[6]:


output=word_scorer(dic)

print(f'The best word right now is {output}')


# Ta-dah! So after initalizing the two arrays letter_frequency and letters, we can easily compute the "best" word. First attempt at some intuitive solver! 
# 
# We would simply call word_scorer based on the available words (the output after filtering) 
