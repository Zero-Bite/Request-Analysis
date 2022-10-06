from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QTableWidgetItem
from PyQt5 import uic
import pandas
from main import parsing_zapros, searching_colums, result_sorting
import sys

data = pandas.read_csv('all_data_prepared.csv', sep=',')
print(data.isna())
data = data.fillna(' ')
country_dir = pandas.read_csv('country_directory.csv', sep=';')
print(data.isna())
countries = ['Любая страна'] + list(pandas.read_csv('county_range.csv').columns)[0].split(';')


class ToDo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = uic.loadUi("zakazchik.ui", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Страница заказчика")

        for i in countries:
            self.window.country.addItem(i)

        self.window.btn_search.clicked.connect(self.search)
        self.window.btn_stat.clicked.connect(self.stat)
        self.window.btn_export.clicked.connect(self.export)

        self.window.tableWidget.setColumnCount(5)
        self.window.tableWidget.setHorizontalHeaderLabels(['Наименование', 'Страна', 'ИНН', 'окбд2', 'характеристики'])

    def search(self):
        zapros = self.window.line_input.text().strip()
        okbd_kode = self.window.kode.text().strip()
        country = self.window.country.currentText()

        c_f_i = 0

        if country != 'Любая страна':
            for p in list(country_dir.country_name):
                if p == country:
                    break
                c_f_i += 1

        print(c_f_i)

        if not any([zapros, okbd_kode]):  # не заполнено ни одно из полей
            pass

        elif not all([zapros, okbd_kode]):  # Заполнено только одно и 2ух полей
            if zapros == '':  # поиск по окбд2-коду
                pass

            else:  # поиск по запросу
                print(1)
                zapros = parsing_zapros(zapros)
                print(2)

                result = []

                for noun in zapros['NOUN']:
                    counter = 0
                    for colums in list(data['noun_words']):
                        for word in colums.split():
                            try:
                                if noun in word:
                                    result.append(counter)

                            except Exception:
                                pass

                        counter += 1

                print(result)

                ranging_results = {}  # [noun, ag]

                for i in result:
                    ranging_results[int(i)] = [0, 0, 0]
                    nouns = data['noun_words'][int(i)].split()
                    adjectives = data['adjective_words'][int(i)].split()

                    for noun in zapros['NOUN']:
                        if noun in nouns:
                            ranging_results[int(i)][0] += 1

                    for adjective in zapros['ADJF']:
                        if adjective in adjectives:
                            ranging_results[int(i)][1] += 1

                for row_num, my_list in ranging_results.items():
                    ranging_results[row_num][2] = ((ranging_results[row_num][0] + ranging_results[row_num][1]) / (
                                len(data.noun_words[row_num].split()) + len(data.adjective_words[row_num].split())))

                print(ranging_results)

                ranging_results = sorted(ranging_results.items(), key=lambda x: x[1][2], reverse=True)

                print(ranging_results)

                q = data[['product_name', 'country_code', 'inn', 'okpd2_code', 'product_characteristics', 'price']].iloc[[j[0] for j in ranging_results]]
                result_result = []
                if country != 'Любая страна':
                    print(c_f_i)
                    counter = 0
                    for p in list(q.country_code):
                        if p == c_f_i:
                            result_result.append(counter)
                        counter += 1
                    print(counter)

                    print('res ====', result_result)

                    q = data[['product_name', 'country_code', 'inn', 'okpd2_code', 'product_characteristics', 'price']].iloc[result_result]

                print(5)

                self.window.tableWidget.setRowCount(len(list(q.product_name)))

                colums_of_table = list(q.columns)

                print(colums_of_table)
                print(list(q[colums_of_table[0]]))

                for i in range(len(list(q.product_name))):
                    for j in range(5):
                        print(list(q[colums_of_table[0]])[i], sep='\t')
                        self.window.tableWidget.setItem(i, j,  QTableWidgetItem(list(q[colums_of_table[j]])[i]))

                try:
                    self.window.med.setText(str(q.price.median()))
                    self.window.mid.setText(str(q.price.mean()))
                    self.window.min.setText(str(q.price.min()))
                    self.window.max.setText(str(q.price.max()))

                except Exception:
                    self.window.med.setText('не')
                    self.window.mid.setText('удалось')
                    self.window.min.setText('подгрузить')
                    self.window.max.setText('статистику')

        else:  # Заполнены оба поля
            pass

        print('страна:', c_f_i)
        print('запрос:', zapros, okbd_kode)

    def stat(self):
        pass

    def export(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToDo()
    ex.show()
    sys.exit(app.exec_())
