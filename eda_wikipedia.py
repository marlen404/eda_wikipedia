import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from bs4 import BeautifulSoup

# Fetch Wikipedia page
r = requests.get('https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue')
soup = BeautifulSoup(r.text, 'html.parser')

# Find all tables on the page and extract the first relevant table
tables = soup.find_all('table', {'class': 'wikitable'})
company_table = tables[0]

# Create a Pandas DataFrame from the HTML table
df = pd.read_html(StringIO(str(company_table)))[0]

# If MultiIndex is present, use the lowest level as column names
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(1)

# Replace duplicate column names with specific names
df.columns = ['Rank', 'Name', 'Industry', 'Revenue (Million USD)', 'Profit (Million USD)',
              'Employees', 'Headquarters', 'State-owned', 'Ref.']

# Clean column names (remove footnotes & whitespace)
df.columns = df.columns.str.replace(r"\[.*\]", "", regex=True).str.strip()

# Find columns with "USD (in millions)" (there are two: revenue & profit)
usd_columns = [col for col in df.columns if 'USD' in col]

if len(usd_columns) == 2:
    df.rename(columns={'USD (in millions)': 'Revenue (Million USD)', 'USD (in millions).1': 'Profit (Million USD)'}, inplace=True)
else:
    print(f"Warning! Unexpected number of USD columns: {usd_columns}")
    exit()

# --- DATA CLEANING ---
columns_to_drop = ['Ref.', 'State-owned']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

df['Revenue (Million USD)'] = df['Revenue (Million USD)'].astype(str).str.replace(r'[\$,]', '', regex=True).astype(float)
df['Profit (Million USD)'] = df['Profit (Million USD)'].astype(str).str.replace(r'[\$,]', '', regex=True).astype(float)

# Convert millions to billions
df['Revenue (Billion USD)'] = df['Revenue (Million USD)'] / 1000
df['Profit (Billion USD)'] = df['Profit (Million USD)'] / 1000

# Remove original columns in millions
df.drop(columns=['Revenue (Million USD)', 'Profit (Million USD)'], inplace=True)

# Prevent errors due to empty Headquarters values
df['Country'] = df['Headquarters'].fillna("Unknown").apply(lambda x: x.split(',')[-1].strip())

# Clean and convert Employees column properly
df['Employees'] = (
    df['Employees']
    .astype(str)
    .str.replace(r'[^\d]', '', regex=True)
    .replace('', '0')
    .astype(float)
)

# --- ANALYSIS & STATISTICS ---
print("\nTop 8 companies by revenue:")
print(df[['Name', 'Revenue (Billion USD)']].head(8))

print("\nAverage revenue by country:")
revenue_by_country = df.groupby('Country')['Revenue (Billion USD)'].mean().sort_values(ascending=False)
print(revenue_by_country)

print("\nMost common industries:")
print(df['Industry'].dropna().value_counts())  # Avoid NaN values

# --- VISUALIZATION ---

# Bar chart: Top 10 companies by revenue
plt.figure(figsize=(12, 6))
sns.barplot(x='Revenue (Billion USD)', y='Name', data=df.head(10), palette='Blues_r')
plt.xlabel('Revenue (Billion USD)')
plt.ylabel('Company')
plt.title('Top 10 Companies by Revenue')
plt.show()

# Pie chart: Revenue distribution by industry
df.groupby('Industry')['Revenue (Billion USD)'].sum().plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8))
plt.title('Revenue Distribution by Industry')
plt.ylabel('')
plt.show()

# Histogram: Distribution of employee numbers
plt.figure(figsize=(10, 5))
sns.histplot(df['Employees'], bins=20, kde=True)
plt.xlabel('Number of Employees')
plt.ylabel('Frequency')
plt.title('Distribution of Employee Numbers')
plt.show()