import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# # Page config
#st.set_page_config(layout="wide", page_title="📱 PhonePe Pulse Visualization", page_icon="📊")
st.set_page_config(layout="wide", page_title="📱 PhonePe Pulse Dashboard", page_icon="📊")

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Dataset Explorer", "📈 Visualizations"])

# ------------------- PAGE 1: HOME -------------------
if page == "🏠 Home":

    st.image("Screenshot 2025-07-08 at 9.33.16 PM.png", use_container_width=True)

    st.title("📊 PhonePe Pulse Analysis")

    # Introduction
    st.markdown("""
    ### 📌 Introduction

    The Indian digital payments story has captured the world's imagination. From bustling metros to remote villages, mobile-first innovation and digital infrastructure have driven an unprecedented revolution. PhonePe, launched in **December 2015**, has been at the forefront of this transformation, benefiting from the **API-driven digitization** of payments championed by India's central bank and government.

    **PhonePe Pulse** is an open-data initiative offering granular, anonymized, and aggregated insights into the digital payments ecosystem — an effort to give back to developers, researchers, and the fintech community.

    ---

    ### 📊 About the Data

    This dashboard visualizes key metrics from the **PhonePe Pulse Dataset**, covering:

    - Transactions (aggregated & mapped)
    - User insights (state, district, pin-code levels)
    - Insurance adoption trends
    - Generational consumer patterns

    All data is licensed under **CDLA-Permissive-2.0** and designed for transparency, innovation, and exploration.
    """)

    # ▶️ Embed YouTube Video (centered visually by default)
    st.markdown("### 📽️ Watch the Overview")
    st.video("https://www.youtube.com/watch?v=Yy03rjSUIB8")

    # Continue with the rest of the content
    st.markdown("""
    ---

    ### 🧠 Bharatiya Consumer: A Generational Study

    India is home to a **young, dynamic population**, reshaping how the nation consumes, spends, and saves. To explore these changes, PhonePe and Dentsu collaborated on a groundbreaking report:  
    **“The Bharatiya Consumer: A Generational Study”**, uncovering deep insights into three key demographics:

    #### 👥 Gen X (1965–1980)
    - High spenders in **finance**, **agriculture**, and **healthcare**
    - Spend **56% more online**, but transact more frequently offline
    - In metros, men transact **17% more** than women

    #### 👥 Gen Y (1981–1996)
    - Dominant in **entertainment**, **commuting**, and **finance**
    - Consistent spend across town classes
    - **Non-metros** transact online the most

    #### 👥 Gen Z (1997–2012)
    - Lead in **food**, **retail**, and **hospitality**
    - Prefer frequent indulgences and experiences
    - Spend **45% more online**, but transact offline **52% more frequently**

    This multi-generational consumer landscape offers invaluable cues to businesses, startups, and policymakers aiming to serve India’s evolving digital audience.

    ---

    ### 📢 Announcements

    🌟 Data for **Q3 and Q4 of 2024** is now available and included in the dashboard visualizations.

    ---
    """)
elif page == "📊 Dataset Explorer":

    file_options = {
        "Aggregated Transactions": "agg_trans.csv",
        "Aggregated Users": "agg_user.csv",
        "Aggregated Insurance": "agg_insurance.csv",
        "Mapped Transactions": "map_trans.csv",
        "Mapped Users": "map_user.csv",
        "Mapped Insurance": "map_insurance.csv",
        "Top District Transactions": "top_trans_dist.csv",
        "Top Pincode Transactions": "top_trans_pin.csv",
        "Top District Users": "top_user_dist.csv",
        "Top Pincode Users": "top_user_pin.csv",
        "Top Insurance Districts": "top_insur_district.csv",
        "Top Insurance Pincodes": "top_insur_pincode.csv"
    }

    # st.sidebar.header("📂 Dataset & Visualization")

    selection = st.sidebar.selectbox("Visit and query a Dataset ", list(file_options.keys()))
    df = file_options[selection]

    # Sidebar: Select type of visualization
    # vis_type = st.sidebar.selectbox(
    #     "Choose a Visualization", 
    #     [
    #         "Total Users by State",
    #         "Top Brand Names per State per Quarter",
    #         "Top 25 States – Transaction Amount vs. Transaction Count",
    #         "Sunburst: Transactions Year-Quarter",
    #         "State-wise App Opens vs Registered Users",
    #         "Most Efficient Districts",
    #         "Top 10 Districts by Avg Insurance Txn Value"
    #     ]
    # )


    #selection = st.sidebar.selectbox("Choose a Dataset", list(file_options.keys()))

    # Load data
    @st.cache_data
    def load_data(file):
        return pd.read_csv(file)

    df = load_data(file_options[selection])
    st.write(f"### Preview of `{selection}` Data")
    st.dataframe(df, use_container_width=True)

    # Basic filtering
    with st.expander("🔍 Filter Data"):
        filtered_df = df.copy()
        columns = st.multiselect("Select columns to filter", df.columns.tolist())

        for col in columns:
            unique_vals = filtered_df[col].unique().tolist()
            selected_vals = st.multiselect(f"Select values for {col}", unique_vals, default=unique_vals[:3])
            if selected_vals:
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

        if not filtered_df.empty:
            st.success("✅ Filtered Successfully!")
            st.dataframe(filtered_df)
        else:
            st.warning("⚠️ No data matched your filter.")
elif page == "📈 Visualizations":
    st.header("📈 PhonePe Data Visualizations")

    vis_type = st.selectbox(
        "Choose a Visualization", 
        [
            "Total Users by State",
            "Top Brand Names per State per Quarter",
            "Top 25 States – Transaction Amount vs. Transaction Count",
            "Sunburst: Transactions Year-Quarter",
            "State-wise App Opens vs Registered Users",
            "Most Efficient Districts",
            "Top 10 Districts by Avg Insurance Txn Value"
        ]
    )
    if vis_type == "Total Users by State":
        import pandas as pd
        import plotly.express as px

        df = pd.read_csv("agg_user.csv")

        df_state_users = df.groupby('State', as_index=False)['UserCount'].sum()

        df_state_users = df_state_users.sort_values(by='UserCount', ascending=False).head(10)

        fig = px.pie(
            df_state_users,
            names='State',
            values='UserCount',
            title='Total Users by State (Top 10)',
            hole=0.3,  
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        fig.update_traces(textinfo='percent+label', pull=[0.1] + [0] * 9)
        fig.update_layout(title_font_size=20)

        st.plotly_chart(fig)


    elif vis_type == "Top Brand Names per State per Quarter":
        import plotly.graph_objects as go

        # Page config
        st.set_page_config(layout="wide", page_title="📱 PhonePe Top Brands", page_icon="📊")
        st.title("📊 Top Brand Names per State per Quarter (Interactive Heatmap)")

        # Load the CSV
        df = pd.read_csv("agg_user.csv")

        # Ensure correct types
        df['UserCount'] = df['UserCount'].astype(int)
        df['Quarter'] = df['Quarter'].astype(str)  # If not already

        # Process the data to get top brand per State & Quarter
        df_top = (
            df.groupby(['State', 'Quarter', 'Brand'], as_index=False)['UserCount'].sum()
        )
        df_top['Rank'] = df_top.groupby(['State', 'Quarter'])['UserCount'].rank(method='first', ascending=False)
        df_top = df_top[df_top['Rank'] == 1].drop(columns='Rank')

        # Pivot for heatmap
        heat_values = df_top.pivot(index='State', columns='Quarter', values='UserCount')
        heat_labels = df_top.pivot(index='State', columns='Quarter', values='Brand')

        # Combine into a custom hover text
        hover_text = heat_labels.copy()
        for row in heat_labels.index:
            for col in heat_labels.columns:
                brand = heat_labels.loc[row, col]
                count = heat_values.loc[row, col]
                hover_text.loc[row, col] = f"Brand: {brand}<br>Users: {count:,}"

        # Plotly heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heat_values.values,
            x=heat_values.columns,
            y=heat_values.index,
            text=hover_text.values,
            hoverinfo='text',
            colorscale='YlOrRd',
            showscale=True,
            colorbar=dict(title="Total Users"),
        ))

        fig.update_layout(
            title="Top Brand per State per Quarter",
            xaxis_title="Quarter",
            yaxis_title="State",
            height=800
        )

        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "Top 25 States – Transaction Amount vs. Transaction Count":
    # Set page configuration
        import plotly.graph_objects as go
        st.set_page_config(page_title="📊 State-wise Transactions", layout="wide")
        st.title("📊 Top 25 States by Transaction Amount and Count")

        # Load CSV
        df = pd.read_csv("agg_trans.csv")

        # Aggregate by State
        df_state_trans = (
            df.groupby("State")[["Transaction_count", "Transaction_amount"]]
            .sum()
            .reset_index()
            .sort_values(by="Transaction_amount", ascending=False)
        )

        # Top 25 states
        df_top = df_state_trans.head(25)

        # Create Plotly Figure
        fig = go.Figure()

        # Bar for Transaction Amount
        fig.add_trace(
            go.Bar(
                x=df_top["State"],
                y=df_top["Transaction_amount"],
                name="Transaction Amount (₹)",
                marker_color="steelblue",
                yaxis="y1"
            )
        )

        # Line for Transaction Count
        fig.add_trace(
            go.Scatter(
                x=df_top["State"],
                y=df_top["Transaction_count"],
                name="Transaction Count",
                mode="lines+markers",
                marker=dict(color="darkorange"),
                yaxis="y2"
            )
        )

        # Update Layout with correct axis title formatting
        fig.update_layout(
            title="Top 25 States: Transaction Amount vs Count",
            xaxis=dict(title="State", tickangle=45),
            yaxis=dict(
                title=dict(text="Transaction Amount (₹)", font=dict(color="steelblue")),
                tickfont=dict(color="steelblue"),
            ),
            yaxis2=dict(
                title=dict(text="Transaction Count", font=dict(color="darkorange")),
                tickfont=dict(color="darkorange"),
                overlaying="y",
                side="right"
            ),
            legend=dict(x=0.01, y=0.99),
            margin=dict(l=40, r=40, t=60, b=100),
            height=600
        )

        # Show in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    elif vis_type == "Sunburst: Transactions Year-Quarter":
        st.set_page_config(layout="wide", page_title="📊 Transaction Sunburst", page_icon="🌞")

        st.title("📊 Transaction Amount by Year and Quarter")

        # Load CSV file
        df = pd.read_csv("agg_trans.csv")

        # Check column names to ensure consistency (you can remove or comment this after first run)
        st.write("Preview of Data:", df.head())

        # Optional: rename columns if needed
        # df.rename(columns={"transaction_count": "Transaction_count", "transaction_amount": "Transaction_amount"}, inplace=True)

        # Grouping data by Year and Quarter
        df_grouped = df.groupby(['Year', 'Quarter'], as_index=False).agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'sum'
        }).rename(columns={
            'Transaction_count': 'Total_Transaction_Count',
            'Transaction_amount': 'Total_Transaction_Amount'
        })

        # Plot sunburst chart
        fig = px.sunburst(
            df_grouped,
            path=['Year', 'Quarter'],
            values='Total_Transaction_Amount',
            color='Total_Transaction_Count',
            color_continuous_scale='Blues',
            title='🌀 Transaction Amount by Year and Quarter (Interactive)'
        )

        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "State-wise App Opens vs Registered Users":
        import plotly.graph_objects as go
        st.set_page_config(layout="wide", page_title="📊 State App Opens vs Registered Users")
        st.title("📱 State-wise App Opens vs Registered Users (Interactive)")

        df = pd.read_csv("map_user.csv")

        df_state_usage = df.groupby("State").agg({
            "Registered_users": "sum",
            "App_opens": "sum"
        }).reset_index().sort_values("App_opens", ascending=False)

        states = df_state_usage["State"]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=states,
            y=df_state_usage["App_opens"],
            name="App Opens",
            marker_color="slateblue",
            yaxis="y1"
        ))

        fig.add_trace(go.Scatter(
            x=states,
            y=df_state_usage["Registered_users"],
            name="Registered Users",
            mode="lines+markers",
            marker=dict(color="orangered"),
            yaxis="y2"
        ))

        fig.update_layout(
            title="📊 App Opens vs Registered Users by State",
            xaxis=dict(title="States", tickangle=45),
            
            yaxis=dict(
                title=dict(text="App Opens", font=dict(color="slateblue")),
                tickfont=dict(color="slateblue")
            ),
            
            yaxis2=dict(
                title=dict(text="Registered Users", font=dict(color="orangered")),
                tickfont=dict(color="orangered"),
                overlaying="y",
                side="right"
            ),
            
            legend=dict(x=0.5, y=1.15, xanchor="center", orientation="h"),
            margin=dict(t=80),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
    elif vis_type == "Most Efficient Districts":
        st.set_page_config(layout="wide", page_title="📊 Avg Transaction Value", page_icon="📈")
        st.title("📌 Top 10 Districts by Average Insurance Transaction Value")

        # Load CSV
        df = pd.read_csv("top_trans_dist.csv")

        # Grouping and calculating values
        df_grouped = df.groupby("District", as_index=False).agg({
            "Transaction_amount": "sum",
            "Transaction_count": "sum"
        })
        df_grouped = df_grouped[df_grouped["Transaction_count"] > 0]
        df_grouped["Avg_Transaction_Value"] = df_grouped["Transaction_amount"] / df_grouped["Transaction_count"]

        # Sorting and selecting top 10
        df_top10 = df_grouped.sort_values(by="Avg_Transaction_Value", ascending=False).head(10)
        df_top10 = df_top10.sort_values(by="Avg_Transaction_Value", ascending=True)  # for horizontal bar chart

        # Plot using Plotly
        fig = px.bar(
            df_top10,
            x="Avg_Transaction_Value",
            y="District",
            orientation="h",
            color="Avg_Transaction_Value",
            color_continuous_scale="Blues",
            labels={"Avg_Transaction_Value": "Avg Transaction Value (₹)"},
            title="📌 Top 10 Districts by Average Insurance Transaction Value"
        )

        fig.update_layout(
            xaxis_title="Average Transaction Value (₹)",
            yaxis_title="District",
            coloraxis_showscale=False,
            title_font_size=18
        )

        # Display plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    elif vis_type == "Top 10 Districts by Avg Insurance Txn Value":
    # Page config
        st.set_page_config(layout="wide", page_title="📊 Insurance Transaction Dashboard", page_icon="💰")
        st.title("📊 Top 10 Districts by Average Insurance Transaction Value")

        # Load CSV file
        df = pd.read_csv("map_insurance.csv")

        # Ensure zero-division is handled
        df["Avg_Transaction_Value"] = df["Transaction_amount"] / df["Transaction_count"].replace(0, pd.NA)

        # Group by District and calculate mean of average transaction value
        df_avg = df.groupby("District", as_index=False)["Avg_Transaction_Value"].mean()

        # Sort and take top 10
        df_avg_sorted = df_avg.sort_values(by="Avg_Transaction_Value", ascending=False).head(10)

        # Plotly bar chart
        fig = px.bar(
            df_avg_sorted,
            x="District",
            y="Avg_Transaction_Value",
            color="Avg_Transaction_Value",
            color_continuous_scale="Reds",
            title="Top 10 Districts by Average Insurance Transaction Value",
            labels={"Avg_Transaction_Value": "Avg Transaction Value (₹)"},
        )

        # Improve layout
        fig.update_layout(
            xaxis_tickangle=-45,
            title_font=dict(size=20, family='Arial', color='black'),
            xaxis_title="District",
            yaxis_title="Avg Transaction Value (₹)",
            plot_bgcolor="white"
        )

        # Display
        st.plotly_chart(fig, use_container_width=True)
