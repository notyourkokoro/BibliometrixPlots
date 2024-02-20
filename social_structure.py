import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap


class SocialStructure:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

    def countries_collaboration_world_map(self, file_name: str, weight: int = 30, height: int = 10,
                                          language: str = 'en', color_map: str = 'custom'):
        localization = {
            'en': {
                'title': 'Countries\' Collaboration World Map',
            },
            'ru': {
                'title': 'Карта мира сотрудничества стран',
            },
        }

        country_dict = {
            'USA': 'United States of America',
        }

        # настройка цветовой карты
        if color_map == 'custom':
            cmap = LinearSegmentedColormap.from_list('custom_colormap', [(0, 'gray'), (1, 'lightblue')])
        else:
            cmap = colormaps[color_map]

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='CollabWorldMap')

        # получение данных о мировой карте
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        # преобразование геометрии в проекцию, пригодную для использования centroid
        world = world.to_crs('+proj=robin')

        # приведение названия стран и столбца к стандартному виду
        df['From'] = [country_dict[country] if country in country_dict else country.title() for country in df['From']]
        df['To'] = [country_dict[country] if country in country_dict else country.title() for country in df['To']]

        # получение количества коллаборация для каждой страны
        df_from = df[['From', 'Frequency']].rename(columns={'From': 'name'})
        df_to = df[['To', 'Frequency']].rename(columns={'To': 'name'})
        temp_df = pd.concat([df_from, df_to], ignore_index=True, sort=False)
        group_df = temp_df.groupby(by='name').sum()

        # добавления к мировой карте информации о продуктивности стран
        world_to_plot_df = pd.merge(world, group_df, left_on='name', right_on='name', how='outer')
        # замена всех нулевых значений продуктивности на нули
        world_to_plot_df['Frequency'] = world_to_plot_df['Frequency'].fillna(0)

        # построение графика
        world_to_plot_df.plot(column='Frequency', legend=True, cmap=cmap, figsize=(weight, height))

        # построение связей между странами
        for index, row in df.iterrows():
            from_country = row['From']
            to_country = row['To']
            from_coords = world[world['name'] == from_country].geometry.centroid.values[0]
            to_coords = world[world['name'] == to_country].geometry.centroid.values[0]
            plt.plot([from_coords.x, to_coords.x], [from_coords.y, to_coords.y], color='red', alpha=0.5)

        plt.title(localization[language]['title'])

        plt.savefig(f'{self.save_path}/countries_collaboration_world_map_{language}.png')
        plt.show()