import pandas as pd
import matplotlib.pyplot as plt


class Overview:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

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
