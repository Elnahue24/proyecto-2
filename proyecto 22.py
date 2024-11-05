#pregunta 1

import pandas as pd
import numpy as np

# Cargar y procesar `Energy Indicators`
energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38, usecols="C:F", names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
energy.replace('...', np.NaN, inplace=True)
energy['Energy Supply'] *= 1000000  # Convertir de petajulios a gigajulios

# Cambiar nombres de países y limpiar nombres con paréntesis
energy['Country'] = energy['Country'].replace({
    "Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"
}).str.replace(r"\s*\(.*\)", "", regex=True)

# Cargar y procesar `world_bank`
gdp = pd.read_csv('world_bank.csv', skiprows=4)
gdp.rename(columns={"Country Name": "Country"}, inplace=True)
gdp['Country'] = gdp['Country'].replace({
    "Korea, Rep.": "South Korea",
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"
})

# Cargar y procesar `scimagojr`
scimagojr = pd.read_excel('scimagojr-3.xlsx')

# Unir los tres DataFrames
merged_df = pd.merge(pd.merge(scimagojr, energy, on="Country"), gdp[['Country'] + [str(year) for year in range(2006, 2016)]], on="Country")
top15_df = merged_df.nsmallest(15, 'Rank').set_index('Country')
print(top15_df)

#pregunta 2

def calcular_perdidas(scimagojr, energy, gdp):
    intersect_df = pd.merge(pd.merge(scimagojr, energy, on="Country", how="outer"), gdp[['Country']], on="Country", how="outer")
    return len(intersect_df) - len(merged_df)

calcular_perdidas(scimagojr, energy, gdp)

#pregunta 3

avgGDP = top15_df[[str(year) for year in range(2006, 2016)]].mean(axis=1).sort_values(ascending=False)
print(avgGDP)

#pregunta 4

sexto_pais = avgGDP.index[5]
gdp_change = top15_df.loc[sexto_pais, '2015'] - top15_df.loc[sexto_pais, '2006']
print(gdp_change)


#pregunta 5

mean_energy_per_capita = top15_df['Energy Supply per Capita'].mean()
print(mean_energy_per_capita)


#pregunta 6

max_renewable_country = top15_df['% Renewable'].idxmax()
max_renewable_value = top15_df['% Renewable'].max()
print((max_renewable_country, max_renewable_value))


#pregunta 7

top15_df['Citation Ratio'] = top15_df['Self-citations'] / top15_df['Citations']
max_citation_ratio_country = top15_df['Citation Ratio'].idxmax()
max_citation_ratio_value = top15_df['Citation Ratio'].max()
print((max_citation_ratio_country, max_citation_ratio_value))


#pregunta 8

top15_df['Estimated Population'] = top15_df['Energy Supply'] / top15_df['Energy Supply per Capita']
third_most_populous_country = top15_df['Estimated Population'].sort_values(ascending=False).index[2]
print(third_most_populous_country)


#pregunta 9

top15_df['Citable docs per Capita'] = top15_df['Citable documents'] / top15_df['Estimated Population']
correlation = top15_df['Citable docs per Capita'].corr(top15_df['Energy Supply per Capita'])
print(correlation)


#pregunta 10

top15_df['HighRenew'] = (top15_df['% Renewable'] >= top15_df['% Renewable'].median()).astype(int)
print(top15_df['HighRenew'])


#pregunta 11

continent_dict = {
    'China': 'Asia', 'United States': 'North America', 'Japan': 'Asia', 'United Kingdom': 'Europe', 'Russian Federation': 'Europe',
    'Canada': 'North America', 'Germany': 'Europe', 'India': 'Asia', 'France': 'Europe', 'South Korea': 'Asia',
    'Italy': 'Europe', 'Spain': 'Europe', 'Iran': 'Asia', 'Australia': 'Australia', 'Brazil': 'South America'
}
top15_df['Continent'] = top15_df.index.to_series().map(continent_dict)
continent_stats = top15_df.groupby('Continent')['Estimated Population'].agg(['size', 'sum', 'mean', 'std'])
print(continent_stats)

