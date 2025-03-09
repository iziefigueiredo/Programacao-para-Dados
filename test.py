import random
import csv


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
        except csv.Error as e:
            raise csv.Error(f'Erro ao processar o arquivo CSV: {e}') from e
        except Exception as e:
            raise Exception(f'Erro inesperado ao ler o arquivo CSV: {e}') from e


class Sampler:
    """
    
    Classe para criar uma amostra aleatória com seed para facilitar a reprodutibilidade
    
    """

    def __init__(self, data, seed=42):
        self.data = data
        self.seed = seed

    def create_sample(self, sample_size=20, output_file='amostra.csv'):
        random.seed(self.seed)
        sample_size = min(sample_size, len(self.data))

        if sample_size == 0:
            raise ValueError('Nenhum dado disponível para criar uma amostra.')

        try:
            amostra = random.sample(self.data, sample_size)

            with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.data[0].keys())
                writer.writeheader()
                writer.writerows(amostra)

            print('Amostra criada com sucesso.')

        except PermissionError as e:
            raise PermissionError(f'Permissão negada ao salvar o arquivo: {output_file}') from e
        except csv.Error as e:
            raise csv.Error(f'Erro ao escrever no arquivo CSV: {e}') from e
        except Exception as e:
            raise Exception(f'Erro inesperado ao criar a amostra: {e}') from e
            
            
#Principal 

if __name__ == '__main__':
    reader = CSVReader()
    data = reader.load_data()

    sampler = Sampler(data)
    sampler.create_sample()