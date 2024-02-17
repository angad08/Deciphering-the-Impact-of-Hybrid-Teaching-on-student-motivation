import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


hybrid_data = pd.read_excel('pages/hybrid_data.xlsx')
# Function to plot a donut chart with specified colors
def plot_donut_chart(data, column, title, ax, colors):
    sizes = data[column].value_counts(normalize=True)
    labels = sizes.index
    wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%', colors=colors,
                                      textprops={'fontsize': 12}, pctdistance=1.2)
    
    # Draw a circle at the center to turn the pie chart into a donut chart
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    ax.add_artist(centre_circle)
    
    ax.legend(wedges, labels,
              title=column,
              loc="lower right",
              bbox_to_anchor=(1, -0.1, 0.5, 1))
    
    ax.set_title(title, fontsize=16)

# Create the figure and define the grid layout
fig = plt.figure(figsize=(15, 5))
gs = GridSpec(1, 3, figure=fig)

# Define colors for the charts
colors = ['#0d6abf','#a8dbad']

# Donut Chart 1: Intrinsic motivation (%) by Like_Hybrid
ax1 = fig.add_subplot(gs[0, 0])
plot_donut_chart(hybrid_data, 'Like_Hybrid', 'Intrinsic motivation (%) by Like_Hybrid', ax1, colors)

# Donut Chart 2: Intrinsic motivation (%) by Gender
ax2 = fig.add_subplot(gs[0, 1])
plot_donut_chart(hybrid_data, 'Gender', 'Intrinsic motivation (%) by Gender', ax2, colors)

# Donut Chart 3: Intrinsic motivation (%) by Motivation_Type
ax3 = fig.add_subplot(gs[0, 2])
plot_donut_chart(hybrid_data, 'Motivation_Type', 'Intrinsic motivation (%) by Motivation Type', ax3, colors)

# Adjust layout for better spacing
plt.tight_layout()

# Display the plots in Streamlit
st.title('Latrobe Student Motivation Dashboard')
st.pyplot(fig)

#plot_stacked_barchart(hybrid_data)
def plot_stacked_barchart(df):
    # Define the combinations for the stacked bar charts
    combinations = [
        ('Campus', 'Gender'),
        ('Campus', 'Motivation_Type'),
        ('Campus', 'Mode'),
        ('Campus', 'Like_Hybrid')
    ]
    
    # Colors for the stacked bar charts
    colors = ['#d64550', '#0d6abf']

    # Create two figures for the 1x2 layout of stacked bar charts
    for i in range(0, len(combinations), 2):
        # Create the figure and define the grid layout for each pair of combinations
        fig, axs = plt.subplots(1, 2, figsize=(25, 7.5))  # Adjust the size as needed

        for j in range(2):
            if i + j < len(combinations):
                x, hue = combinations[i + j]
                # Calculate the Median Intrinsic motivation (%) by for each combination
                median_values = df.groupby([x, hue])['IM_Percentage'].median().unstack()
                # Plot with specified colors
                median_values.plot(kind='barh', stacked=True, ax=axs[j], color=colors)
                axs[j].set_title(f'Median Intrinsic motivation (%) by by {x} and {hue}')
                axs[j].set_xlabel('Median Intrinsic motivation (%) by')
                axs[j].set_ylabel(x)
                axs[j].legend(title=hue, loc='lower right')

                # Display values on the bars
                for container in axs[j].containers:
                    axs[j].bar_label(container, label_type='center', fmt='%.2f', fontsize=11)

        plt.tight_layout()
        # Display the plots in Streamlit
        st.pyplot(fig)

# Call the function to plot the stacked bar charts in the Streamlit app
plot_stacked_barchart(hybrid_data)
