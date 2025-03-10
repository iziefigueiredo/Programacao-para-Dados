import csv
from collections import defaultdict
import re

class CSVReader:
    """
    
    Classe para carregar e analisar arquivos CSV.
    
    """

    def __init__(self, filename='steam.csv'):
        self.filename = filename

    def load_data(self):
        """
        
        Carrega os dados do arquivo CSV e retorna uma lista de dicionários.
       
        """
        try:
            with open(self.filename, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                games = [row for row in reader]
            return games
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Arquivo não encontrado: {self.filename}") from e
        except Exception as e:
            raise Exception(f"Erro ao ler o arquivo CSV: {e}") from e


class GameStats:
    """
    
    Classe responsável por calcular estatísticas dos jogos.
    
    """

    def __init__(self, games):
        self.games = games

    def game_counts(self):
        """
        
        Retorna o total de jogos únicos e gratuitos únicos.
        
        """
        unique_games = set()
        unique_free_games = set()

        for game in self.games:
            app_id = game['AppID']
            unique_games.add(app_id)

            try:
                if float(game.get('Price', 0)) == 0.0:
                    unique_free_games.add(app_id)
            except ValueError:
                continue

        return len(unique_games), len(unique_free_games)

    def percentage_games(self):
        """
        
        Retorna as porcentagens de jogos gratuitos e pagos.
        
        """
        total_games, total_free = self.game_counts()
        total_paid = total_games - total_free

        percent_free = (total_free / total_games) * 100
        percent_paid = (total_paid / total_games) * 100

        return {
            'free_percentage': round(percent_free, 2),
            'paid_percentage': round(percent_paid, 2)
        }
    
    def yearly_releases(self):
        """
        
        Retorna um dicionário com o total de jogos únicos lançados por ano.
        
        """
        games_year = defaultdict(int)
        seen_games = set()

        for game in self.games:
            app_id = game['AppID']
            if app_id in seen_games:
                continue

            seen_games.add(app_id)

            release_date = game.get('Release date', '').strip()
            year_match = re.search(r'\b\d{4}\b', release_date)
            year = year_match.group() if year_match else 'Unknown'

            games_year[year] += 1

        return dict(games_year)




# Principal
if __name__ == '__main__':
    reader = CSVReader()
    jogos = reader.load_data()
    stats = GameStats(jogos)

    percentages = stats.percentage_games()
    print(f"Jogos gratuitos: {percentages['free_percentage']}%")
    print(f"Jogos pagos: {percentages['paid_percentage']}%")

    print('\n')
    print(f"Jogos lançados por ano: {stats.yearly_releases()}")
   