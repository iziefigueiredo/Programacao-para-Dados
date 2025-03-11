import re
from collections import defaultdict

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

    def peak_years(self):
        """
        Retorna o ano ou anos com o maior número de lançamentos de jogos.
        """
        games_year = self.yearly_releases()
        max_releases = max(games_year.values())
        most_years = [year for year, count in games_year.items() if count == max_releases]

        return most_years if len(most_years) > 1 else most_years[0]

    def price_playtime(self):
        """
        Analisa a relação entre o preço dos jogos e o tempo mediano de jogo.
        Retorna um dicionário com faixas de preço e a média do tempo mediano de jogo para cada título.
        """
        price_categories = defaultdict(list)

        for game in self.games:
            try:
                price = float(game.get('Price', 0))
                playtime = float(game.get('Median playtime forever', 0))

                if price == 0:
                    price_categories["Grátis"].append(playtime)
                elif price <= 5:
                    price_categories["Até $5"].append(playtime)
                elif price <= 20:
                    price_categories["De $5 a $20"].append(playtime)
                elif price <= 50:
                    price_categories["De $20 a $50"].append(playtime)
                else:
                    price_categories["Acima de $50"].append(playtime)

            except ValueError:
                continue  

        result = {cat: round(sum(times) / len(times), 2) if times else 0 for cat, times in price_categories.items()}
        return result
