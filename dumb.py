import csv
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# file = 'tweets_cet_sp.csv'

# word_list = {}

# with open(file, encoding='utf8') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=';')
#     for row in csv_reader:
#         tokens = word_tokenize(row[1])
#         tokens = [w.lower() for w in tokens]
#         table = str.maketrans('', '', string.punctuation)
#         stripped = [w.translate(table) for w in tokens]
#         words = [word for word in stripped if word.isalpha()]
#         stop_words = stopwords.words('portuguese')
#         words = [w for w in words if w not in stop_words]
#         for word in words:
#             if word in word_list:
#                 word_list[word] = word_list[word] + 1
#             else:
#                 word_list[word] = 1
#     word_count = {k: v for k, v in sorted(word_list.items(), key=lambda item: item[1])}
#     print(word_count)

# word_count = {
#     'pista': 635, 'número': 120, 'prefeitura': 146, 'acidente': 147, 'ônibus': 149, 'carro': 149, 'via': 1057, 'retenção': 164, 'enguiçado': 194, 
#     'poda': 197, 'r': 952, 'ocupa': 751, 'procissão': 223, 'ruas': 252, 'trânsito': 854, 'praça': 265, 'local': 456, 'faixa': 839, 'estrada': 315, 
#     'centro': 793, 'av': 1702, 'altura': 505, 'trechos': 545, 'sentido': 2533, 'evento': 622, 'interditam': 702, 'obras': 781, 'avenida': 907, 
#     'interdita': 1384, 'rua': 3501, 'sentidos': 180, 'expressa': 182, 'interditado': 205, 'faixas': 210, 'monitorado': 212, 'túnel': 218, 'zc': 242, 
#     'zn': 303, 'zo': 345, 'ponte': 383, 'bairro': 401, 'zl': 446, 'zs': 762
# }

# words = word_count.keys()
# print(words)

dictionary = [
    'pista', 'número', 'prefeitura', 'acidente', 'ônibus', 'carro', 'via', 'retenção', 'enguiçado', 'poda', 'r', 'ocupa', 'procissão', 'ruas', 'trânsito', 
    'praça', 'local', 'faixa', 'estrada', 'centro', 'av', 'altura', 'trechos', 'sentido', 'evento', 'interditam', 'obras', 'avenida', 'interdita', 'rua', 
    'sentidos', 'expressa', 'interditado', 'faixas', 'monitorado', 'túnel', 'zc', 'zn', 'zo', 'ponte', 'bairro', 'zl', 'zs'
]

file = 'tweets_transito_sp.csv'
counter = {
    'class_0': 0,
    'class_1': 0
}

with open(file, encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        text = row[1]
        id = row[0]
        tokens = word_tokenize(row[1])
        tokens = [w.lower() for w in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        stop_words = stopwords.words('portuguese')
        words = [w for w in words if w not in stop_words]
        text_class = 0
        for word in words:
            if word in dictionary:
                text_class = 1

        with open('classified.csv', 'a', encoding='utf-8') as output_file:
            field_names = ['class', 'id', 'text']
            writer = csv.DictWriter(
                output_file, delimiter=',',
                lineterminator='\n',
                fieldnames=field_names
            )
            writer.writerow({
                'class': text_class,
                'id': id,
                'text': text
            })

        if text_class == 1:
            counter['class_1'] = counter['class_1'] + 1
        else:
            counter['class_0'] = counter['class_0'] + 1

print(counter)
