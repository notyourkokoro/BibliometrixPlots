import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

from matplotlib import colormaps


class Countries:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

    def corresponding_authors_countries(self, file_name: str, size: int = 10, weight: int = 10, height: int = 6,
                                        dpi: int = 300, language: str = 'en'):
        localization = {
            'en': {
                'title': 'Corresponding Author\'s Countries',
                'xlabel': 'Documents (N)',
                'ylabel': 'Countries',
                'legend': 'Collaboration',
            },
            'ru': {
                'title': 'Страны авторов-корреспондентов',
                'xlabel': 'Документы (N)',
                'ylabel': 'Страны',
                'legend': 'Объединения',
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='CorrAuthCountries')

        # удаление нулевых значений
        df.dropna(inplace=True)

        # сортировка данных по невозрастанию
        df.sort_values(by='Articles', ascending=True, inplace=False)

        # отсечение записей
        df = df.head(size).iloc[::-1]

        # Создаем фигуру и оси для графика
        fig, ax = plt.subplots(figsize=(weight, height), dpi=dpi)

        # Сортируем данные по столбцу Articles
        data_sorted = df.sort_values(by='Articles', ascending=True)

        # Создаем переменную для позиции y на графике
        y_pos = range(len(data_sorted))

        # Рисуем столбцы SCP
        ax.barh(y_pos, data_sorted['SCP'], color='blue', label='SCP')

        # Рисуем столбцы MCP поверх столбцов SCP
        ax.barh(y_pos, data_sorted['MCP'], color='red', left=data_sorted['SCP'], label='MCP')

        # Устанавливаем заголовок и метки осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        # Устанавливаем метки на оси y
        ax.set_yticks(y_pos)
        ax.set_yticklabels(data_sorted['Country'])

        # Добавляем легенду
        ax.legend(title=localization[language]['legend'])

        plt.savefig(f'{self.save_path}/corresponding_authors_countries_{language}.png')
        plt.show()

    def countries_scientific_production(self, file_name: str, weight: int = 30, height: int = 10, language: str = 'en',
                                        color_map: str = 'bone'):
        localization = {
            'en': {
                'title': 'Countries\' Scientific Production',
            },
            'ru': {
                'title': 'Научная продуктивность стран',
            },
        }

        country_dict = {
            'USA': 'United States of America',
        }

        # настройка цветовой карты
        cmap = colormaps[color_map]

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='CountrySciProd')

        # получение данных о мировой карте
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # приведение названия стран и столбца к стандартному виду
        df['region'] = [country_dict[country] if country in country_dict else country.title() for country in
                        df['region']]
        df.rename(columns={'region': 'name'}, inplace=True)

        # добавления к мировой карте информации о продуктивности стран
        world_to_plot_df = pd.merge(world, df, left_on='name', right_on='name', how='outer')
        # замена всех нулевых значений продуктивности на нули
        world_to_plot_df['Freq'] = world_to_plot_df['Freq'].fillna(0)

        # построение графика
        world_to_plot_df.plot(column='Freq', legend=True, cmap=cmap, figsize=(weight, height))

        # подпись графика
        plt.title(localization[language]['title'])

        plt.savefig(f'{self.save_path}/countries_scientific_production_{language}.png')
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

        plt.savefig(f'{self.save_path}/countries_production_over_time_{language}.png')
        plt.show()
