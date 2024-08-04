import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


data = pd.read_csv('UNRATE.csv', parse_dates=['DATE'])

data['UNRATE_MA3'] = data['UNRATE'].rolling(window=3).mean()

data['UNRATE_MIN12'] = data['UNRATE'].rolling(window=12).min()

data['SAHM_RULE'] = data['UNRATE_MA3'] - data['UNRATE_MIN12']

data['RECESSION_SIGNAL'] = data['SAHM_RULE'] > 0.50

plt.figure(figsize=(14, 8))
plt.plot(data['DATE'], data['SAHM_RULE'], label='Sahm Rule Indicator', color='blue')
plt.axhline(y=0.5, color='red', linestyle='--')
plt.fill_between(data['DATE'], 0, data['SAHM_RULE'], where=data['RECESSION_SIGNAL'], color='grey', alpha=0.5, label='Recession Periods')

recession_periods = data[data['RECESSION_SIGNAL']]
peaks_with_recession = recession_periods[(recession_periods['SAHM_RULE'] == recession_periods['SAHM_RULE'].rolling(window=3, center=True).max())]
for idx in peaks_with_recession.index:
    plt.annotate(f"{data.loc[idx, 'SAHM_RULE']:.2f}", 
                 (data.loc[idx, 'DATE'], data.loc[idx, 'SAHM_RULE']),
                 textcoords="offset points", 
                 xytext=(0,10), 
                 ha='center',
                 color='black')

plt.xlabel('Year')
plt.ylabel('Sahm Rule Indicator (Percentage Points)')
plt.title('Real-time Sahm Rule Recession Indicator')

plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))  
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y')) 

plt.xlim(pd.Timestamp('1948-01-01'), pd.Timestamp('2024-07-01'))

plt.xticks(rotation=45, ha='right')
plt.tight_layout()  

plt.legend()
plt.grid(True)
plt.show()