import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

df = pd.read_csv("/Users/pritul/Downloads/Change logs/temp.csv")

df['No. of methods changes'] = pd.to_numeric(
    df['No. of methods changes'], errors='coerce')
df['No. of classes changed'] = pd.to_numeric(
    df['No. of classes changed'], errors='coerce')
df['Time (minutes)'] = pd.to_numeric(df['Time (minutes)'], errors='coerce')


x = df[df['Phase'] == 'Actualization']['No. of methods changes'].fillna(
    0).astype(int)
y = df[df['Phase'] == 'Verification']['Time (minutes)'].fillna(0).astype(int)

# calculate Pearson correlation coefficient and p-value
corr_coef, p_value = pearsonr(x, y)

# plot scatter plot with regression line and correlation coefficient in title
sns.regplot(x=x, y=y)
plt.xlabel("No. of methods changes")
plt.ylabel("Time (minutes)")
plt.title(
    f"Scatter plot with regression line and correlation coefficient\n Actualization vs Verification phases \n (corr = {corr_coef:.2f}, p = {p_value:.2f})")
plt.show()
