import pandas as pd
import matplotlib.pyplot as plt


class Overview:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

    def corresponding_author_countries(self):
        localization = {
            'en': {
                'title': 'Corresponding Author\'s Countries',
                'xlabel': 'Documents (N)',
                'ylabel': 'Countries'
            },
            'ru': {
                'title': 'Ежегодная научная продукция',
                'xlabel': 'Документы (N)',
                'ylabel': 'Страны'
            },
        }

        pass

    def annual_scientific_production(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300,
                                     language: str = 'en'):
        localization = {
            'en': {
                'title': 'Annual Scientific Production',
                'xlabel': 'Year',
                'ylabel': 'Articles'
            },
            'ru': {
                'title': 'Ежегодная научная продукция',
                'xlabel': 'Год',
                'ylabel': 'Статьи'
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='AnnualSciProd')

        # Установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика
        plt.plot(df['Year'], df['Articles'])

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.savefig(f'{self.save_path}/annual_scientific_production_{language}.png')
        plt.show()

    def countries_production_over_time(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300,
                                       language: str = 'en'):
        localization = {
            'en': {
                'title': 'Countries\' Production over Time',
                'xlabel': 'Year',
                'ylabel': 'Articles',
                'legend': 'Country',
            },
            'ru': {
                'title': 'Продуктивность в странах с течением времени',
                'xlabel': 'Год',
                'ylabel': 'Статьи',
                'legend': 'Страна',
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='CountryProdOverTime')

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика при помощи фильтрации по филиалу
        for affiliation in df['Country'].unique():
            df_affiliation = df[df['Country'] == affiliation]
            plt.plot(df_affiliation['Year'], df_affiliation['Articles'], label=affiliation)

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), title=localization[language]['legend'])
        plt.grid(True)

        plt.savefig(f'{self.save_path}/affiliations_production_over_time_{language}.png')
        plt.show()
