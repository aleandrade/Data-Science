a=[12, 1, 1]
a.extend([13,14])
del(a[0])
print(sorted(a))
coisas = "Eu tenho uma frase. Talvez duas"
print(str(coisas.split(".")))
meu_set = set(a)
meu_set.add(2)
print(meu_set)
meu_outro_set = {1,13, 99}
print(meu_set.union(meu_outro_set))
dict = {"Santos": "3", "Palmeiras": "1"}
if "Santos" in dict:
    print("Achei!" + dict["Santos"])

for coiso in a:
    print(str(coiso) + "\n")

print(sum(a))


with open("medals.csv", "r") as medalsFile:
    content = medalsFile.readline()
    print(content)
import pandas
df=pandas.read_csv('medals.csv')
df_novo=df['NOC'].ffill().unique()
dfCountries = pandas.read_excel("C:\\Users\\ANDRAL\\Documents\\DTA_visualize\\countries.xlsx")
List = df.set_index('NOC').join(dfCountries.set_index('3 letter'))['Country name'].ffill().unique().tolist()


#novo=df['NOC'].unique()
