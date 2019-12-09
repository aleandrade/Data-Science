import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

jogos = pd.read_csv("spi_matches.csv")
Santos = jogos[np.logical_or(jogos['team1'] == 'Santos', jogos['team2'] == 'Santos')]
jogos_Santos = Santos[['date', 'team1', 'team2', 'score1', 'score2']]

for label, row in jogos_Santos.iterrows() :
    print(str(row["date"]) + " : " + str(row["team1"]) + " " + str(row["score1"])[0] + "x"  + str(row["score2"])[0] + " " + str(row["team2"]))
    if(row['team1'] == "Santos") :
        jogos_Santos.loc[label, "gols_santos"] = row['score1']
        jogos_Santos.loc[label, "gols_adv"] = row['score2']
    else :
        jogos_Santos.loc[label, "gols_santos"] = row['score2']
        jogos_Santos.loc[label, "gols_adv"] = row['score1']

jogos_Santos["datetimeobj"] = jogos_Santos["date"].apply(lambda x : datetime.datetime.strptime(x, "%Y-%m-%d"))

plt.plot_date(x=jogos_Santos['datetimeobj'], y=jogos_Santos['gols_santos'], xdate = True, ydate = False, color = 'blue')
plt.plot_date(x=jogos_Santos['datetimeobj'], y=jogos_Santos['gols_adv'], xdate = True, ydate = False, color = 'red')
plt.show()
plt.clf()

plt.hist(jogos_Santos['gols_santos'], bins = range(7), alpha=0.5, label='Gols Santos')
plt.hist(jogos_Santos['gols_adv'], bins = range(7), alpha=0.5, label='Gols Adv.')
plt.legend(loc='upper right')
plt.xticks(range(7))
plt.show()
plt.clf()