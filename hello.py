words = {}
space = '\n'
i = 0
new_new_list = []
words_list = ['охуеннен', 'и', 'пиздат', 'я', 'дегенерат']
for word_word in words_list:
    words.update({word_word: {'индекс': 1, 'tag': 'слово'}})
test = list(map(lambda x: x, words.items()))
razn = (len(test)/2) + 1
for i in range(len(test)+int(razn)):
    if i % 2 == 1:
        test.insert(i, '\n')
for i in range(len(test)):
    print(test[i])



