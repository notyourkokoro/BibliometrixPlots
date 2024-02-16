import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Sources:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

    def most_relevant_sources(self, file_name: str, size: int = 10, weight: int = 10, height: int = 6, dpi: int = 300,
                              language: str = 'en'):
        localization = {
            'en': {
                'title': 'Most Relevant Sources',
                'xlabel': 'Articles',
                'ylabel': 'Sources'
            },
            'ru': {
                'title': 'Ежегодная научная продукция',
                'xlabel': 'Статьи',
                'ylabel': 'Источники'
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='MostRelSources')

        # сортировка данных по невозрастанию
        df.sort_values(by='Articles', ascending=True, inplace=False)

        # отсечение записей
        df = df.head(size).iloc[::-1]

        # Установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика
        plt.barh(df['Sources'], df['Articles'])

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.savefig(f'{self.save_path}/most_relevant_sources_{language}.png')
        plt.show()

    def core_sources_by_bradfords_law(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300,
                                      language: str = 'en'):
        localization = {
            'en': {
                'title': 'Core Sources by Bradford\'s Law',
                'xlabel': 'Source log (Rank)',
                'ylabel': 'Articles'
            },
            'ru': {
                'title': 'Основные источники по закону Брэдфорда',
                'xlabel': 'Ранжирование источников',
                'ylabel': 'Статьи'
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='BradfordLaw')

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # Построение графика
        plt.plot(df['cumFreq'], df['Freq'])

        # выделение данных для первой зоны
        zone_1 = df[df['Zone'] == 'Zone 1']

        # рисование прямоугольника
        rect = patches.Rectangle((zone_1['cumFreq'].min(), 0), zone_1['cumFreq'].max() - zone_1['cumFreq'].min(),
                                 zone_1['Freq'].max(), color='lightgray', alpha=0.5)
        plt.gca().add_patch(rect)

        # добавление подписей для оси x
        plt.gca().set_xticks(zone_1['cumFreq'], zone_1['SO'], rotation=90)

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.savefig(f'{self.save_path}/core_sources_by_bradfords_law_{language}.png')
        plt.show()

    def sources_production_over_time(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300,
                                     language: str = 'en'):
        localization = {
            'en': {
                'title': 'Sources\' Production over Time',
                'xlabel': 'Year',
                'ylabel': 'Cumulate occurrences'
            },
            'ru': {
                'title': 'Основные источники по закону Брэдфорда',
                'xlabel': 'Год',
                'ylabel': 'Количество случаев'
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='SourceProdOverTime')

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

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
        plt.grid(True)

        plt.savefig(f'{self.save_path}/sources_production_over_time_{language}.png')
        plt.show()
