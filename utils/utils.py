
with open("utils/words.txt",'rb') as f:
    english_dictionary = [word for word in f.read().decode().strip().split(",") if len(word) == 5]
f.close()


