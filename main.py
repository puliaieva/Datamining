
import pandas as pd

import nltk

from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice

OUTPUT_FOLDER = "output/"

sample = pd.read_csv("sms-spam-corpus.csv", encoding = "ISO-8859-1")
ham = sample[sample.v1 == "ham"]
spam = sample[sample.v1 == "spam"]

stop_words = nltk.corpus.stopwords.words("english")
haml =[]
spaml =[]
ham_filtered=[]
spam_filtered=[]

#убираем цифры и буквы
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

with open(OUTPUT_FOLDER+ "counts_ham.txt","w", encoding = "ISO-8859-1") as out:
    for key,val in counts_ham.items():
        out.write('{}:{}\n'.format(key,val))

with open(OUTPUT_FOLDER+ "counts_spam.txt","w", encoding = "ISO-8859-1") as out:
    for key,val in counts_spam.items():
        out.write('{}:{}\n'.format(key,val))


#график1
ham_word_lenth=[]
spam_word_lenth=[]
for word in ham_filtered:
    lenth1=len(word)
    ham_word_lenth.append(lenth1)
for word in spam_filtered:
    lenth2=len(word)
    spam_word_lenth.append(lenth2)

average_words = sum(ham_word_lenth+spam_word_lenth) / len(ham_word_lenth+spam_word_lenth)


labels1, ham_word_count = zip(*Counter(ham_word_lenth).items())
ham_word_l = np.arange(len(labels1))

labels2, spam_word_count = zip(*Counter(spam_word_lenth).items())
spam_word_l = np.arange(len(labels2))

plt.plot(ham_word_l, ham_word_count, spam_word_l, spam_word_count, average_words,0, "go")
plt.xlabel("Длинна слова")
plt.ylabel("Частота")
plt.legend(["Ham", "Spam", "Average " + str(average_words)])

#plt.savefig(OUTPUT_FOLDER + "words_frequency.png")
#plt.show()

#график2
ham_sentence_lenth=[]
spam_sentence_lenth=[]
for line in haml:
    lenth3=len(line)
    ham_sentence_lenth.append(lenth3)
for line in spaml:
    lenth4=len(line)
    spam_sentence_lenth.append(lenth4)

average_sentence = sum(ham_sentence_lenth+spam_sentence_lenth) / len(ham_sentence_lenth+spam_sentence_lenth)

labels3, ham_sentence_count = zip(*Counter(ham_sentence_lenth).items())
ham_sentence_l = np.arange(len(labels3))

labels4, spam_sentence_count = zip(*Counter(spam_sentence_lenth).items())
spam_sentence_l = np.arange(len(labels4))

plt.plot(ham_sentence_l, ham_sentence_count, spam_sentence_l, spam_sentence_count, average_sentence,0, "go")
plt.xlabel("Длинна предложения")
plt.ylabel("Частота")
plt.legend(["Ham", "Spam", "Average " + str(average_sentence)])
#plt.savefig(OUTPUT_FOLDER + "sentence_frequency.png")
#plt.show()


#sort

sort_ham=[]
sort_spam=[]

for (k,v) in counts_ham.items():
    sort_ham.append((v,k))
sort_ham=sorted(sort_ham, reverse=True)


for (k,v) in counts_spam.items():
    sort_spam.append((v,k))
sort_spam=sorted(sort_spam, reverse=True)

#график3
top20_ham=sort_ham[:20]
top20_spam=sort_spam[:20]

def plot3(top20, category, saving_name):
    x_labels = [val[1] for val in top20]
    y_labels = [val[0] for val in top20]
    plt.figure(figsize=(14, 7))
    ax = pd.Series(y_labels).plot(kind='bar')
    ax.set_xticklabels(x_labels)

    rects = ax.patches

    for rect, label in zip(rects, y_labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height, label, ha='center', va='bottom')

    plt.xlabel("Слово")
    plt.ylabel("Частота")
    plt.legend([category])
    plt.savefig(OUTPUT_FOLDER + saving_name)
    plt.show()
#plot3(top20_ham, "Ham", "top20_ham.png")
#plot3(top20_spam, "Spam", "top20_spam.png")



