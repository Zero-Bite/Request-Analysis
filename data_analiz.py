import pandas
import pymorphy2

ABC = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
       'w', 'x', 'y', 'z', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
       'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё', '1', '2', '3', '4', '5', '6', '7',
       '8', '9', '0']
ABC_up = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
          'W', 'X', 'Y', 'Z', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
          'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'Ё']


def parsing_data():
    global data
    counter_of_lines = 0  # индексирование строк
    morhy = pymorphy2.MorphAnalyzer()

    data['noun_words'] = ' '
    data['adjective_words'] = ' '
    data['another_words'] = ' '

    for item in list(data.product_name):
        root_of_noun = ''
        root_of_adjf_and_prtf = ''
        root_of_else = ''
        for element in item.split():
            new_elem = element
            element = ''
            for i in new_elem:
                if i in ABC or i in ABC_up:
                    element += i

            if not element in ['для', 'на', 'с', 'без', 'к', 'и']:
                element = morhy.parse(element)[0]

                if element.tag.POS == 'NOUN':
                    # существительное дропаем в колонку с существиетельными как новую строку
                    root_of_noun += element.normal_form + ' '
                elif element.tag.POS == 'ADJF' or element.tag.POS == 'PRTF':
                    # прилагательное в колонку с прилагательными
                    root_of_adjf_and_prtf += element.normal_form + ' '
                else:
                    root_of_else += element.normal_form + ' '
        data.noun_words[counter_of_lines] = root_of_noun
        data.adjective_words[counter_of_lines] = root_of_adjf_and_prtf
        data.another_words[counter_of_lines] = root_of_else

        counter_of_lines += 1


def county_range(data_list):  # ранжирует страны по упомянаемсти в данных
    my_lib = {}
    for i in list(data_list):
        try:
            for j in i.split('|'):
                if j not in my_lib:
                    my_lib[j] = 0
                my_lib[j] += 1

        except Exception:
            pass

    return [i[0] for i in sorted(my_lib.items(), key=lambda x: x[1], reverse=True)]  # list id стран в порядке убывания



data1 = pandas.read_csv('Контракты 44ФЗ.csv', sep=';')
data2 = pandas.read_csv('Справочник пром производства.csv', sep=';')
data3 = pandas.read_csv('Ценовые предложения поставщиков.csv', sep=';')

data = pandas.concat([data1, data2, data3])

data.to_csv('all_data_prepared')
