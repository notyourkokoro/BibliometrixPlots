import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd


class Countries:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

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
        cmap = plt.cm.get_cmap(color_map)

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

        plt.savefig(f'{self.save_path}/annual_scientific_production_{language}.png')
        plt.show()

