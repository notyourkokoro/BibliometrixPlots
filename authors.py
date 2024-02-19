import pandas as pd
import matplotlib.pyplot as plt


class Authors:
    def __init__(self, save_path: str = 'plots'):
        self.save_path = save_path

    def most_relevant_authors(self, file_name: str, size: int = 10, weight: int = 10, height: int = 6, dpi: int = 300,
                              language: str = 'en'):
        localization = {
            'en': {
                'title': 'Most Relevant Authors',
                'xlabel': 'Articles',
                'ylabel': 'Authors'
            },
            'ru': {
                'title': 'Наиболее значимые авторы',
                'xlabel': 'Статьи',
                'ylabel': 'Авторы'
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='MostRelAuthors')

        # сортировка данных по невозрастанию
        df.sort_values(by='Articles', ascending=False, inplace=True)

        # отсечение записей
        df = df.head(size).iloc[::-1]

        # Установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # построение графика
        plt.barh(df['Authors'], df['Articles'])

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.savefig(f'{self.save_path}/most_relevant_authors_{language}.png')
        plt.show()

    def authors_production_over_time(self, file_name: str, weight: int = 10, height: int = 6, dpi: int = 300,
                                     language: str = 'en'):
        localization = {
            'en': {
                'title': 'Authors\' Production over Time',
                'xlabel': 'Year',
                'ylabel': 'Authors',
                'legend': 'Articles (N)'
            },
            'ru': {
                'title': 'Авторская продукция с течением времени',
                'xlabel': 'Год',
                'ylabel': 'Авторы',
                'legend': 'Статьи (N)',
            },
        }

        # загрузка данных
        df = pd.read_excel(file_name, sheet_name='AuthorProdOverTime')

        # установка ширины, высоты и dpi графика
        plt.figure(figsize=(weight, height), dpi=dpi)

        # словарь для хранения информации о размерах точек и соответствующих им подписей в легенде
        legend_handles = {}

        # Перебираем уникальных авторов и строим линии для каждого автора
        for author in df['Author'].unique():
            # Фильтруем данные для текущего автора
            author_data = df[df['Author'] == author]

            # Рисуем линию для текущего автора
            plt.plot(author_data['year'], [author] * len(author_data), label=author)

            for year in author_data['year'].unique():
                count = len(author_data[author_data['year'] == year])
                scatter = plt.scatter(year, author, s=50 * count, color='black', alpha=0.5)

                if count not in legend_handles:
                    # добавление точки в легенду и ее значения
                    legend_handles[count] = scatter

        plt.legend(legend_handles.values(), legend_handles.keys(), title=localization[language]['legend'],
                   loc='center left', bbox_to_anchor=(1, 0.5))

        # подпись графика и осей
        plt.title(localization[language]['title'])
        plt.xlabel(localization[language]['xlabel'])
        plt.ylabel(localization[language]['ylabel'])

        plt.savefig(f'{self.save_path}/authors_production_over_time_{language}.png')
        plt.show()

    def author_productivity_through_lotkas_law(self, file_name: str, weight: int = 10, height: int = 6,
                                               dpi: int = 300, language: str = 'en'):
        pass
