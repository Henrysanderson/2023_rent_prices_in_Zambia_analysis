
# Modules to be used
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl


# Loading the dataset
df = pd.read_excel('Lsk_rent_houses_mar23.xlsx')


# ### Data Cleaning

df.head(10)

# Checking for null values
df.isnull().sum()

# Drop unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


# Total_NaN_values in the dataset
total_NaN_values = df.isna().sum().sum()
print(f'The total number of NaN values in the dataset is {total_NaN_values}')

 
# Drop rows with missing 'Area' values if they are critical
df = df.dropna(subset=['Area'])

# Fill missing 'Bedroom' values with the mode (most common number) for each area
df['Bedroom'] = df.groupby('Area')['Bedroom'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.median()))

# Fill missing 'Bathroom' values with the median number for each area
df['Bathroom'] = df.groupby('Area')['Bathroom'].transform(lambda x: x.fillna(x.median()))

# Drop 'Garage' if not needed
# df = df.drop(columns=['Garage'])

# fill 'Garage' NaNs with 0, assuming no garage if it’s reasonable
df['Garage'] = df['Garage'].fillna(0)

 
# Second layer to finish up cleaning the remaining NaN columns
df['Rent'].fillna(df['Rent'].median(), inplace=True)
df['Bedroom'].fillna(df['Bedroom'].mode()[0], inplace=True)
df['Bathroom'].fillna(df['Bathroom'].median(), inplace=True)

df['Garage'] = pd.to_numeric(df['Garage'], errors='coerce')

   
# ### Data Analysis

 
df['Area'].unique()

st.title("House Rent Analysis in Lusaka")
st.write("Visualizing various insights into rent prices across different areas in Lusaka.")

# # 1. What is the average rent for houses in each area?

 
# Calculate average rent by area
avg_rent_area = df.groupby('Area')['Rent'].mean()

# Plot the result
st.subheader("Average Rent by Area")
fig, ax = plt.subplots()
avg_rent_area.plot(kind='bar', ax=ax)
ax.set_xlabel("Area")
ax.set_ylabel("Average Rent")
st.pyplot(fig)

st.write(f'The most expensive price is about K{avg_rent_area.max()} while the least expensive is about K{avg_rent_area.min()}')

   
# # 2. How does the number of bedrooms impact the rent prices?

# Box plot for rent based on the number of bedrooms
# st.subheader("Rent Distribution by Number of Bedrooms")
# fig, ax = plt.subplots()
# sns.boxplot(x='Bedroom', y='Rent', data=df, ax=ax)
# st.pyplot(fig)

   
# # 3. Is there a correlation between the number of bathrooms and rent?

# Scatter plot to see correlation between bathrooms and rent
# st.subheader("Rent Distribution by Number of Bedrooms")
# fig, ax = plt.subplots()
# sns.boxplot(x='Bedroom', y='Rent', data=df, ax=ax)
# st.pyplot(fig)


# Calculate correlation coefficient
correlation = df['Bathroom'].corr(df['Rent'])
st.write("Correlation between Bathrooms and Rent:", correlation)

   
# # 4. Which area has the highest and lowest rent variability?

# Box plot to show rent variability in each area
# st.subheader("Rent Variability by Area")
# fig, ax = plt.subplots()
# sns.boxplot(x='Area', y='Rent', data=df, ax=ax)
# ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
# st.pyplot(fig)


# # 5. What percentage of listings offer garages, and does having a garage impact rent?

 
# Bar chart comparing average rent for houses with and without garages
st.subheader("Average Rent by Garage Availability")
avg_rent_garage = df.groupby('Garage')['Rent'].mean()
fig, ax = plt.subplots()
avg_rent_garage.plot(kind='bar', ax=ax)
ax.set_xlabel("Garage")
ax.set_ylabel("Average Rent")
st.pyplot(fig)

   
# # 6. What is the distribution of rents across different areas?

 
# Histogram to show rent distribution by area
# Rent Distribution by Area with Dynamic Button
st.subheader("Rent Distribution by Area")

# Create a dropdown selector for areas
selected_area = st.selectbox("Select an area to view rent distribution:", df['Area'].unique())

# Add a button to trigger the plot after an area is selected
if st.button("Show Rent Distribution"):
    # Filter data for the selected area
    area_rent_data = df[df['Area'] == selected_area]['Rent']
    
    # Plotting the rent distribution for the selected area
    st.write(f"Rent Distribution in {selected_area}")
    fig, ax = plt.subplots()
    area_rent_data.hist(bins=20, ax=ax)
    ax.set_xlabel("Rent")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)


   
# # 7. What is the average rent for each combination of bedrooms and bathrooms?

 
# Create a pivot table for average rent by bedrooms and bathrooms
rent_pivot = df.pivot_table(values='Rent', index='Bedroom', columns='Bathroom', aggfunc='mean')

# Heatmap to visualize average rent by bedroom and bathroom combination
# st.subheader("Rent Distribution with Outliers")
# fig, ax = plt.subplots()
# sns.boxplot(x='Rent', data=df, ax=ax)
# st.pyplot(fig)
# st.write("Median Rent:", df['Rent'].median())

   
# # 8. What is the median rent, and are there any outliers in rent prices?

 
# Box plot to identify outliers in rent values
# st.subheader("Rent Distribution with Outliers")
# fig, ax = plt.subplots()
# sns.boxplot(x='Rent', data=df, ax=ax)
# st.pyplot(fig)
# st.write("Median Rent:", df['Rent'].median())

# # Calculate median rent
# median_rent = df['Rent'].median()
# st.write("Median Rent:", median_rent)

   
# # 9. How does the presence of a garage and more than one bathroom together impact rent?

 
# Filter dataset for houses with garages and more than one bathroom
# garage_bathroom = df[(df['Garage'] > 0) & (df['Bathroom'] > 1)]

# # Box plot for rent of houses with garage and multiple bathrooms
# st.subheader("Rent for Houses with Garage and Multiple Bathrooms")
# garage_bathroom = df[(df['Garage'] > 0) & (df['Bathroom'] > 1)]
# fig, ax = plt.subplots()
# sns.boxplot(y='Rent', data=garage_bathroom, ax=ax)
# st.pyplot(fig)


   
# # 10. Are rents skewed towards higher or lower values in any area?

 
# Histogram to check for skewness in rent prices
st.subheader("Skewness of Rent Prices")
fig, ax = plt.subplots()
sns.histplot(df['Rent'], kde=True, ax=ax)
st.pyplot(fig)

selected_area = st.selectbox("Select an area for skewness calculation", df['Area'].unique())
area_rent = df[df['Area'] == selected_area]['Rent']
st.write(f"Skewness of Rent in {selected_area}:", area_rent.skew())



