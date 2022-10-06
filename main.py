import pandas
import pymorphy2


def search_by_okpd2_code(string):
    codes = data.okpd2_code

    # конвертируем полученую строку к списку
    code_okpd = string.split('.')
    result = []
    line_index = 2

    for item_checker in list(codes):
        item_checker = item_checker.split('.')
        if item_checker == code_okpd:
            result.append(line_index)
        line_index += 1

    if len(result) == 0:
        print(f"По вашему okpd2-code {string} - ничего не найдено")

    return result


def parsing_zapros(string):
    parser = pymorphy2.MorphAnalyzer(lang='ru')

    zapros_param = {'NOUN': [], 'ADJF': [], 'ELSE': []}

    for i in string.split():
        chast_rechi = parser.parse(i)[0].tag.POS
        i = parser.parse(i)[0].normal_form

        if chast_rechi == 'PRTF':
            zapros_param['ADJF'].append(i)
        elif chast_rechi != 'NOUN' and chast_rechi != 'ADJF':
            zapros_param['ELSE'].append(i)
        else:
            zapros_param[chast_rechi].append(i)

    return zapros_param


def searching_colums(zapros):
    data = pandas.read_csv('all_data_prepared', sep=',')
    result = []

    for noun in zapros['NOUN']:
        counter = 0
        for colums in list(data['noun_words']):
            try:
              for word in colums.split():
                if noun in word:
                  result.append(counter)

            except Exception:
                    pass

            counter += 1

    return result


def result_sorting(zapros, result):
    global data
    ranging_results = {}

    for i in result:
        ranging_results[int(i)] = [0, 0, 0]
        nouns = data['noun_words'][int(i)].split()
        try:
          adjectives = data['adjective_words'][int(i)].split()
        except Exception:
          pass

        try:
          for noun in zapros['NOUN']:
              if noun in nouns:
                  ranging_results[int(i)][0] += 1

          for adjective in zapros['ADJF']:
              if adjective in adjectives:
                  ranging_results[int(i)][1] += 1

        except Exception:
          pass

    for row_num, my_list in ranging_results.items():
      try:
        ranging_results[row_num][2] = ((ranging_results[row_num][0] + ranging_results[row_num][1]) / (len(data.noun_words[row_num].split()) + len(data.adjective_words[row_num].split())))

      except Exception:
        pass

    ranging_results = sorted(ranging_results.items(), key=lambda x: x[1][2], reverse=True)

    return ranging_results


def main():
    pass
