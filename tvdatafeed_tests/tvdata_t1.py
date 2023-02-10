from tvDatafeed import TvDatafeed, Interval

tv = TvDatafeed()

# Pra pegar o histórico de um ativo qualquer:
'''
get_hist(
        self,
        symbol: str,
        exchange: str = "NSE",
        interval: Interval = Interval.in_daily,
        n_bars: int = 10,
        fut_contract: int = None,
        extended_session: bool = False,
    ) -> pd.DataFrame:
'''
df = tv.get_hist('PETR4', 'BMFBOVESPA', n_bars=10)
df.index.min()

df = tv.get_hist('BVSPX', 'VANTAGE', n_bars=5000)
df.reset_index(inplace=True)
df.datetime.min()
# Pra procurar se um simbolo existe, pattern-matching, não precisa ser o nome exato
'''
search_symbol(self, text: str, exchange: str = '') -> [dict, dict, dict2]
RETORNA:

'''
tv.search_symbol('PETR4')