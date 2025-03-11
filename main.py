from csv_reader import CSVReader
from game_stats import GameStats

# Carregar os dados
reader = CSVReader()
jogos = reader.load_data()

# Criar a classe de estatísticas
stats = GameStats(jogos)

# Calcular a porcentagem de jogos gratuitos e pagos
percentages = stats.percentage_games()

# Calcular a relação entre preço e tempo de jogo
price_playtime_relation = stats.price_playtime()



print(f"Jogos gratuitos: {percentages['free_percentage']}%")
print(f"Jogos pagos: {percentages['paid_percentage']}%")

print('\n')
print(f"Ano com maior número de lançamento: {stats.peak_years()}")

print('\n')
print("Relação entre Preço e Tempo Mediano de Jogo:")
for category, avg_playtime in price_playtime_relation.items():
    print(f"{category}: {avg_playtime} minutos")