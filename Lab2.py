import csv
import re
import pandas as pd

import nltk
from tkinter.filedialog import askopenfilename
fileway = askopenfilename()
filename = fileway.split("/")

OUTPUT_FOLDER = "output/"
stop_words = nltk.corpus.stopwords.words("english")

sample = pd.read_csv(filename[-1], encoding = "ISO-8859-1")
ham = sample[sample.v1 == "ham"]
spam = sample[sample.v1 == "spam"]

haml =[]
spaml =[]
ham_filtered=[]
spam_filtered=[]

#убираем цифры и знаки
for i in ham.v2:
    haml.append("".join(c for c in i if c.isalpha() or c == " ").lower())
for i in spam.v2:
    spaml.append("".join(c for c in i if c.isalpha() or c == " ").lower())

#убираем стопслова
for line_in_ham in haml:
   l_ham = line_in_ham.split()
   for w in l_ham:
       if w not in stop_words:
           ham_filtered.append(w)

for line_in_spam in spaml:
   l_spam = line_in_spam.split()
   for w in l_spam:
       if w not in stop_words:
           spam_filtered.append(w)

#кол-во слов
counts_ham = {}
counts_spam = {}
for word in ham_filtered:
    counts_ham[word] = counts_ham.get(word, 0) + 1

for word in spam_filtered:
   counts_spam[word] = counts_spam.get(word, 0) + 1

def find_number_of_words_in_dict(word, words_dict):
   for key in words_dict:
       if key == word:
           return words_dict[key]

   return 0

overall_spam = 0
overall_ham = 0
print("enter message:")
sentence = input()
words = re.findall('[a-zA-Z]+', sentence)
filtered_words = []
for w in words:
   if w not in stop_words:
       filtered_words.append(w)

for key in counts_ham:
   overall_ham += counts_ham[key]
for key in counts_spam:
   overall_spam += counts_spam[key]

spam_probability = 1
ham_probability = 1

for word in filtered_words:
   num_in_ham = find_number_of_words_in_dict(word, counts_ham)
   num_in_spam = find_number_of_words_in_dict(word, counts_spam)

   if num_in_ham == 0:
       overall_ham += 1
   if num_in_spam == 0:
       overall_spam += 1
   spam_probability *= (num_in_spam + 1) / overall_spam
   ham_probability *= (num_in_ham + 1) / overall_ham

if spam_probability > ham_probability:
   print('spam')
else:
   print('ham')

print(float(spam_probability))
print(float(ham_probability))