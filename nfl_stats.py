import json
import pandas as pd
from io import StringIO

from scrapper import Scrapper
import urls


OUTPUT_PATH = 'stats'

class NFLStats:
    def __init__(self, position: str):
        """The position should be one of the following:
            -passing
            -rushing
            -receiving
            -defense
            -scoring
            -special_returning
            -special_kick
            -special_punt
        if none of the above is provided, passing will be selected"""

        if position == 'passing':
            self.scrap = Scrapper(urls.qb_stats_url)
        elif position == 'rushing':
            self.scrap = Scrapper(urls.rushing_stats_url)
        elif position == 'receiving':
            self.scrap = Scrapper(urls.receiver_stats_url)
        elif position == 'defense':
            self.scrap = Scrapper(urls.defense_stats_url)
        elif position == 'scoring':
            self.scrap = Scrapper(urls.scoring_stats_url)
        elif position == 'special_returning':
            self.scrap = Scrapper(urls.special_ret_stats_url)
        elif position == 'special_kick':
            self.scrap = Scrapper(urls.special_kick_stats_url)
        elif position == 'special_punt':
            self.scrap = Scrapper(urls.special_punt_stats_url)
        else:
            self.scrap = Scrapper(urls.qb_stats_url)

        self.position = position
        rk = self.scrap.get_all_by_attribute(tag='tr', attr='data-idx')
        names = self.scrap.get_all_recursive_search(filters=[('div', 'athleteCell__flag flex items-start mr7'),
                                                             ('a', 'AnchorLink')])

        stats_header = self.scrap.get_all_recursive_search(
            filters=[('tr', 'Table__sub-header Table__TR Table__even'),
                     ('th', 'Table__TH')])

        raw_stats = self.scrap.get_all_recursive_search(
            filters=[('div', 'Table__ScrollerWrapper relative overflow-hidden'),
                     ('tbody', 'Table__TBODY'),
                     ('tr', 'Table__TR Table__TR--sm Table__even'),
                     ('td', '')])

        rk = [int(i) for i in rk]
        # We convert the stats values to numbers
        for i in range(len(raw_stats)):
            value = raw_stats[i].replace(',', '')
            if value.replace('.', '', 1).isdigit():
                raw_stats[i] = float(value)

        # We group the stats in vectors for each player
        stats_grouped = []
        for i in range(0, len(raw_stats), len(stats_header) - 2):
            if i < len(raw_stats):
                stats_grouped.append(raw_stats[i:i + len(stats_header) - 2])

        # We create the dictionary of stats, less the ranking and name
        stats = []
        for i in stats_grouped:
            stats.append(dict(zip(stats_header[2:], i)))

        # We create the dictionary of names and ranking
        aux = [i for i in zip(rk, names)]
        aux_names = []
        for i in aux:
            aux_names.append(dict(zip(stats_header[:2], i)))

        # Player stats dictionaries union
        self.qb_stats = []
        for i in range(len(aux_names)):
            self.qb_stats.append({**aux_names[i], **stats[i]})

        self.formatted_stats_dict = json.dumps(self.qb_stats, indent=4)

    def export_csv(self):
        df = pd.read_json(StringIO(self.formatted_stats_dict))
        df.to_csv(f"{OUTPUT_PATH}/{self.position}.csv", encoding='utf-8', index=False)


