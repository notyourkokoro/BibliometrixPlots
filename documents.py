import pandas as pd
import matplotlib.pyplot as plt
import squarify

from wordcloud import WordCloud


class Words:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

    def most_relevant_words(self, file_name: str, size: int = 10, weight: int = 10, height: int = 6, dpi: int = 300,
                            language: str = 'en'):
        localization = {
            'en': {
                'title': 'Most Relevant Words',
                'xlabel': 'Occurrences',
                'ylabel': 'Keywords'
            },
            'ru': {
                'title': 'Наиболее релевантные ключевые слова',
                'xlabel': 'Встречаются раз',
                'ylabel': 'Ключевые слова'
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='MostFreqWords')

        # сортировка данных по невозрастанию
        df.sort_values(by='Occurrences', ascending=False, inplace=True)

        # отсечение записей
        df = df.head(size).iloc[::-1]

        # Установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика
        plt.barh(df['Words'], df['Occurrences'])

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.savefig(f'{self.save_path}/most_relevant_words_{language}.png')
        plt.show()

    def word_cloud(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300):
        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='WordCloud')

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)
        # Создание словаря из данных
        word_freq = {term: freq for term, freq in zip(df['Terms'], df['Frequency'])}

        # Создание облака слов
        wordcloud = WordCloud(width=weight * 100, height=height * 100, background_color='white',
                              prefer_horizontal=1.0).generate_from_frequencies(word_freq)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        plt.savefig(f'{self.save_path}/word_cloud.png')
        plt.show()

    def treemap(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300, fontsize: int = 6,
                word_cut: int = 10, language: str = 'en'):
        localization = {
            'en': {
                'title': 'TreeMap',
            },
            'ru': {
                'title': 'Древовидная карта',
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='TreeMap')

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # подготовка данных
        labels = df.apply(
            lambda x: f'{x["Terms"][:word_cut]}{"..." if len(x["Terms"]) > 10 else ""}\n({x["Frequency"]})', axis=1)

        # построение графика
        squarify.plot(sizes=df['Frequency'], label=labels, alpha=.8, text_kwargs={'fontsize': fontsize})

        plt.title(localization[language]['title'])
        plt.axis('off')

        plt.savefig(f'{self.save_path}/treemap_{language}.png')
        plt.show()

    def words_frequency_over_time(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300,
                                  language: str = 'en'):
        localization = {
            'en': {
                'title': 'Words\' Frequency over Time',
                'xlabel': 'Year',
                'ylabel': 'Cumulate occurrences',
                'legend': 'Terms',
            },
            'ru': {
                'title': 'Частота употребления ключевых слов с течением времени',
                'xlabel': 'Год',
                'ylabel': 'Количество случаев',
                'legend': 'Слова',
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='WordFreqOverTime')

        # получение значение годов для оси y
        years = df['Year']
        df.drop('Year', axis=1, inplace=True)

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика при помощи перебора
        for column in df.columns:
            plt.plot(years, df[column], label=column)

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), title=localization[language]['legend'])
        plt.grid(True)

        plt.savefig(f'{self.save_path}/words_frequency_over_time_{language}.png')
        plt.show()

    def trend_topics(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300, language: str = 'en'):
        localization = {
            'en': {
                'title': 'Trend Topics',
                'xlabel': 'Year',
                'ylabel': 'Term',
                'legend': 'Term frequency',
            },
            'ru': {
                'title': 'Актуальность тем',
                'xlabel': 'Год',
                'ylabel': 'Слова',
                'legend': 'Частота ключевых слов',
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='TrendTopics')

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # Отрисовка отрезков
        for _, row in df.iterrows():
            plt.plot([row['year_q1'], row['year_q3']], [row['item'], row['item']], color='lightblue')

        # Добавление шариков
        legend_handles = {}
        for _, row in df.iterrows():
            scatter = plt.scatter(row['year_med'], row['item'], s=row['freq'] * 10, color='lightblue', alpha=0.5)
            if row['freq'] not in legend_handles:
                legend_handles[row['freq']] = scatter

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.grid(True)

        plt.legend(legend_handles.values(), legend_handles.keys(), title=localization[language]['legend'],
                   loc='center left', bbox_to_anchor=(1, 0.5))

        plt.savefig(f'{self.save_path}/trend_topics_{language}.png')
        plt.show()
