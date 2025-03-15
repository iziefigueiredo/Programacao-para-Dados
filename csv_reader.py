import csv

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
