
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()
butyavka = morph.parse('бутявка')[0]
inf = butyavka.inflect({'gent'})
print(inf)