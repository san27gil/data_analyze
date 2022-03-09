import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the csv file:
df = pd.read_csv('/survey_results_public.csv', index_col=0, thousands='.')

###### INSPECT THE TABLE AND UNDERSTAD THE DATA ######
# We know this is a survey so let's see the answer of one person
# We can do this by searching by row
print(df.loc[2])

# More options to explore the data
print(df.info())
print(df.shape)
print(df.columns)
print(df.head())
print(df.tail())

###### CLEANING THE DATA ######
# Clean all duplicates
df = df.drop_duplicates(inplace=True)

# Drop rows that are completely empty
 df = df.dropna(how='all')

# How many null values do we have in each column?
print(df.isnull().any())

# Percentage of null values in each column
print(df.isnull().sum()/df.shape[0])

# Another way to see null values
print(sns.heatmap(df.isnull(), yticklabels=False))

# Clear all columns that have more than a specific percentage of null values
limit = len(df)*0.55
df = df.dropna(thresh=limit, axis=1, inplace=True)

# Clear unuseful columns for the queries we are looking for
to_drop = ['Age1stCode', 'OrgSize', 'MiscTechHaveWorkedWith', 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 
 'NEWCollabToolsWantToWorkWith', 'NEWOtherComms', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth', 
 'SurveyLength', 'SurveyEase']
df = df.drop(to_drop, inplace=True, axis=1)

# Improve data types. There are columns with numbers as an object so we change it to float
print(df.dtypes)

df['YearsCode'] =  df['YearsCode'].apply(pd.to_numeric, errors='coerce')
df['YearsCodePro'] =  df['YearsCodePro'].apply(pd.to_numeric, errors='coerce')

# See the outliers
plt.boxplot(df['CompTotal'], vert=False)
print(plt.show())

# Drop the outliers
Q1 = df['CompTotal'].quantile(0.25)
Q3 = df['CompTotal'].quantile(0.75)
IQR = Q3 - Q1

lower_limit = (Q1 - 1.5 * IQR)
upper_limit = (Q3 + 1.5 * IQR)
df = df[(df['CompTotal'] >= lower_limit) & (df['CompTotal'] <= upper_limit)]

# Fill the null values for each column with its mean
df.YearsCode.fillna(df.YearsCode.median(), inplace=True)
df.YearsCodePro.fillna(df.YearsCodePro.median(), inplace=True)
df.CompTotal.fillna(df.CompTotal.median(), inplace=True)
df.ConvertedCompYearly.fillna(df.ConvertedCompYearly.median(), inplace=True)

# See everything works
print(df.isnull().sum()/df.shape[0])

# See how many answers are for each column and improve some
print(df.nunique())

# Improve Country column
print(df.Country.unique())

df = df['Country'].replace(['United Kingdom of Great Britain and Northern Ireland', 'Russian Federation', 'Hong Kong (S.A.R.)', 
 'Venezuela, Bolivarian Republic of...', 'Congo, Republic of the...', 'United States of America'], 
 ['UK', 'Russia', 'Hong Kong', 'Venezuela', 'Congo', 'USA'], inplace=True)

# Make sure
print(df.groupby('Country').size()[0:50])

# Improve EdLevel column
print(df.groupby('EdLevel').size())

df = df['EdLevel'].replace(['Associate degree (A.A., A.S., etc.)', 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)', 
 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)', 'Other doctoral degree (Ph.D., Ed.D., etc.)', 
 'Professional degree (JD, MD, etc.)', 'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)'], 
 ['Associate degree', 'Bachelor’s degree', 'Master’s degree','Other doctoral degree', 'Professional degree', 'Secondary school'], inplace=True)

