import json

from scrapper import Scrapper
import urls

qb_scrap = Scrapper(urls.qb_stats_url)
rk = qb_scrap.get_all_by_attribute(tag='tr', attr='data-idx')
names = qb_scrap.get_all_recursive_search(filters=[('div', 'athleteCell__flag flex items-start mr7'),
                                                   ('a', 'AnchorLink')])

qb_stats_header = qb_scrap.get_all_recursive_search(filters=[('tr', 'Table__sub-header Table__TR Table__even'),
                                                             ('th', 'Table__TH')])

raw_qb_stats = qb_scrap.get_all_recursive_search(filters=[('div', 'Table__ScrollerWrapper relative overflow-hidden'),
                                                          ('tbody', 'Table__TBODY'),
                                                          ('tr', 'Table__TR Table__TR--sm Table__even'),
                                                          ('td', '')])

rk = [int(i) for i in rk]
# We convert the stats values to numbers
for i in range(len(raw_qb_stats)):
    value = raw_qb_stats[i].replace(',', '')
    if value.replace('.', '', 1).isdigit():
        raw_qb_stats[i] = float(value)


# We group the stats in vectors for each player
stats_grouped = []
for i in range(0, len(raw_qb_stats), len(qb_stats_header) - 2):
    if i < len(raw_qb_stats):
        stats_grouped.append(raw_qb_stats[i:i + len(qb_stats_header) - 2])

# We create the dictionary of stats, less the ranking and name
stats = []
for i in stats_grouped:
    stats.append(dict(zip(qb_stats_header[2:], i)))

# We create the dictionary of names and ranking
aux = [i for i in zip(rk, names)]
aux_names = []
for i in aux:
    aux_names.append(dict(zip(qb_stats_header[:2], i)))

# Player stats dictionaries union
qb_stats = []
for i in range(len(aux_names)):
    qb_stats.append({**aux_names[i], **stats[i]})

formatted_stats_dict = json.dumps(qb_stats, indent=4)
print(formatted_stats_dict)




