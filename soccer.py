import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split 
import math
import seaborn as sns

jogos = pd.read_csv("spi_matches.csv")
Santos = jogos[np.logical_or(jogos['team1'] == 'Santos', jogos['team2'] == 'Santos')]
jogos_Santos = Santos[['date', 'team1', 'team2', 'score1', 'score2', 'prob1', 'prob2', 'importance1', 'importance2', 'spi1', 'spi2']]

for label, row in jogos_Santos.iterrows() :
    print(str(row["date"]) + " : " + str(row["team1"]) + " " + str(row["score1"])[0] + "x"  + str(row["score2"])[0] + " " + str(row["team2"]))
    if(row['team1'] == "Santos") :
        jogos_Santos.loc[label, "gols_santos"] = row['score1']
        jogos_Santos.loc[label, "gols_adv"] = row['score2']
        jogos_Santos.loc[label, "local"] = 0.0
        jogos_Santos.loc[label, "prob_Santos"] = row['prob1']
        jogos_Santos.loc[label, "spi_Santos"] = row['spi1']
        if(math.isnan(row['importance1'])) :
            jogos_Santos.loc[label, "importance_Santos"] = 25.0
        else : 
            jogos_Santos.loc[label, "importance_Santos"] = row['importance1']
    else :
        jogos_Santos.loc[label, "gols_santos"] = row['score2']
        jogos_Santos.loc[label, "gols_adv"] = row['score1']
        jogos_Santos.loc[label, "local"] = 1.0
        jogos_Santos.loc[label, "prob_Santos"] = row['prob2']
        jogos_Santos.loc[label, "spi_Santos"] = row['spi2']
        if(math.isnan(row['importance2'])) :
            jogos_Santos.loc[label, "importance_Santos"] = 25.0
        else : 
            jogos_Santos.loc[label, "importance_Santos"] = row['importance2']

jogos_Santos["datetimeobj"] = jogos_Santos["date"].apply(lambda x : datetime.datetime.strptime(x, "%Y-%m-%d"))

plt.plot_date(x=jogos_Santos['datetimeobj'], y=jogos_Santos['gols_santos'], xdate = True, ydate = False, color = 'blue')
plt.plot_date(x=jogos_Santos['datetimeobj'], y=jogos_Santos['gols_adv'], xdate = True, ydate = False, color = 'red')
#plt.show()
plt.clf()

plt.hist(jogos_Santos['gols_santos'], bins = range(7), alpha=0.5, label='Gols Santos')
plt.hist(jogos_Santos['gols_adv'], bins = range(7), alpha=0.5, label='Gols Adv.')
plt.legend(loc='upper right')
plt.xticks(range(7))
#plt.show()
plt.clf()

#Treinando kNeighbors para prever numero de gols
Santos_predict = jogos_Santos[['gols_santos','prob_Santos', 'importance_Santos', 'spi_Santos', 'local']]

ax = sns.heatmap(Santos_predict.corr(), square=True, cmap='RdYlGn')
plt.show()

X = Santos_predict.drop('gols_santos', axis=1).values
y = Santos_predict['gols_santos'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=4)
knn.fit(X_test,y_test)
print(knn.predict(X_test))
print(knn.score(X_test, y_test))
