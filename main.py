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
    
    def percentage_games(self):
        """
        
        Retorna  as porcentagens de jogos gratuitos e pagos.
        
        """
        total_unique_games = self.total_games()
        total_free = self.total_free_games()
        total_paid = total_unique_games - total_free
    
        percent_free = (total_free / total_unique_games) * 100
        percent_paid = (total_paid / total_unique_games) * 100
    
        return {
            'free_percentage': round(percent_free, 2),
            'paid_percentage': round(percent_paid, 2)
        }
    
    
        
#Principal     
        
if __name__ == '__main__':
    reader = CSVReader()
    jogos = reader.load_data()
    stats = GameStats(jogos)
    percentages = stats.percentage_games()
    
    
    
    
    print(f"Jogos gratuitos: {percentages['free_percentage']}%")
    print(f"Jogos pagos: {percentages['paid_percentage']}%")
  