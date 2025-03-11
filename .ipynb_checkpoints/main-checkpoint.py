import csv
import re
import random
from collections import defaultdict

class CSVReader:
    """
    
    Classe para carregar e analisar arquivos CSV.
    
    """

    def __init__(self, filename='steam.csv'):
        self.filename = filename

    def load_data(self):
        """
        
        Carrega os dados do arquivo CSV e retorna uma lista de dicionários
        
        """
        try:
            with open(self.filename, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                games = [row for row in reader]

            return games

        except FileNotFoundError as e:
            raise FileNotFoundError(f'Arquivo não encontrado: {self.filename}') from e
        except Exception as e:
            raise Exception(f'Erro ao ler o arquivo CSV: {e}') from e


class GameStats:
    """
    
    Classe responsável por calcular estatísticas dos jogos.
    
    """

    def __init__(self, games):
        """
    
        Inicializa com a lista de jogos.
        
        """
        self.games = games
 
        
    def total_games(self):
        """
        
        Retorna o total de jogos únicos.
        
        """
        unique_games = set()
        for game in self.games:
            unique_games.add(game['AppID'])
        return len(unique_games)

    def total_free_games(self):
        """
        
        Retorna o total de jogos gratuitos únicos.
        
        """
        unique_free_games = set()
        for game in self.games:
            try:
                if float(game['Price']) == 0.0:
                    unique_free_games.add(game['AppID'])
            except ValueError:
                continue  
        return len(unique_free_games)
    
    def games_per_year(self):
        """
        
        Retorna um dicionário com o total de jogos únicos lançados por ano.
        
        """
        games_year = defaultdict(set)
        for game in self.games:
            release_date = game['Release date']
            if release_date:
                year_match = re.search(r'\b(19|20)\d{2}\b', release_date)
                year = year_match.group() if year_match else 'Unknown'
            else:
                year = 'Unknown'
            games_year[year].add(game['AppID'])
        return {year: len(appids) for year, appids in games_year.items()}

    def year_most_releases(self):
        """
        
        Retorna o ano ou anos com o maior número de lançamentos de jogos.
        
        """
        games_year = self.games_per_year()
        max_releases = max(games_year.values())
        most_years = [year for year, count in games_year.items() if count == max_releases]
        return most_years if len(most_years) > 1 else most_years[0]
        
#Principal     
        
if __name__ == '__main__':
    reader = CSVReader()
    jogos = reader.load_data()
    stats = GameStats(jogos)
    
    if jogos:
        # Exibir tipos de dados e nomes das colunas
        print('Tipos de dados e nomes de cada coluna:')
        primeiro_jogo = jogos[0]
        for coluna, valor in primeiro_jogo.items():
            print(f'{coluna}: {type(valor)}')

      
    else:
        print('Nenhum dado carregado para análise.')
    
    print('\n')
    print(f'Total de jogos carregados: {stats.total_games()}')
    print(f'Total de jogos gratuitos: {stats.total_free_games()}')
    print(f"Jogos lançados por ano: {stats.games_per_year()}")
    print(f"Ano com mais lançamentos: {stats.year_most_releases()}")