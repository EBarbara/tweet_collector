import csv

from sklearn.model_selection import train_test_split


def save(dataset, filename):
    with open(filename, 'w', encoding='utf-8') as output_file:
        field_names = ['class', 'id', 'text']
        writer = csv.DictWriter(
            output_file, delimiter=',',
            lineterminator='\n',
            fieldnames=field_names
        )
        for data in dataset:
            writer.writerow({
                'class': data[0],
                'id': data[1],
                'text': data[2]
            })


rows = []
with open('classified.csv', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    rows = list(reader)

train_data, test_data = train_test_split(rows, test_size=0.2, shuffle=True)

save(train_data, '2class_training_br.csv')
save(test_data, '2class_testing_br.csv')
