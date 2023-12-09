from nfl_stats import *

# qb_stats = NFLStats(position='passing')
# rb_stats = NFLStats(position='rushing')
wr_stats = NFLStats(position='receiving')
# defense_stats = NFLStats(position='defense')
# scoring_stats = NFLStats(position='scoring')

wr_stats.export_csv()

#print(rb_stats.formatted_stats_dict)
#print(qb_stats.formatted_stats_dict)



