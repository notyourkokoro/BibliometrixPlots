import pandas as pd
import matplotlib.pyplot as plt


class Affiliations:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

    def most_relevant_affiliations(self, file_name: str, size: int = 10, weight: int = 10, height: int = 6, dpi: int = 300,
                                   language: str = 'en'):
        localization = {
            'en': {
                'title': 'Most Relevant Affiliations',
                'xlabel': 'Articles',
                'ylabel': 'Affiliations'
            },
            'ru': {
                'title': 'Наиболее релевантные филиалы',
                'xlabel': 'Статьи',
                'ylabel': 'Принадлежность'
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='MostRelAffiliations')

        # сортировка данных по невозрастанию
        df.sort_values(by='Articles', ascending=True, inplace=False)

        # отсечение записей
        df = df.head(size).iloc[::-1]

        # Установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика
        plt.barh(df['Affiliation'], df['Articles'])

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.savefig(f'{self.save_path}/most_relevant_affiliations_{language}.png')
        plt.show()

    def affiliations_production_over_time(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300,
                                          language: str = 'en'):
        localization = {
            'en': {
                'title': 'Affiliations\' Production over Time',
                'xlabel': 'Year',
                'ylabel': 'Articles',
                'legend': 'Affiliation',
            },
            'ru': {
                'title': 'Продуктивность аффилиации с течением времени',
                'xlabel': 'Год',
                'ylabel': 'Статьи',
                'legend': 'Филиалы',
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='AffOverTime')

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика при помощи фильтрации по филиалу
        for affiliation in df['Affiliation'].unique():
            df_affiliation = df[df['Affiliation'] == affiliation]
            plt.plot(df_affiliation['Year'], df_affiliation['Articles'], label=affiliation)

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), title=localization[language]['legend'])
        plt.grid(True)

        plt.savefig(f'{self.save_path}/affiliations_production_over_time_{language}.png')
        plt.show()
