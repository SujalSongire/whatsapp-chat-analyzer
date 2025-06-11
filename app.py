import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import plotly.express as px

# -------------------- Streamlit Page Config -------------------- #
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# -------------------- Sidebar -------------------- #
st.sidebar.title(" WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a chat file")

if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analyze chat for", user_list)

    if st.sidebar.button(" Show Analysis"):

        # -------------------- Top Statistics -------------------- #
        st.markdown("## Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", num_media_messages)
        col4.metric("Links Shared", num_links)

        st.divider()

        # -------------------- Monthly Timeline -------------------- #
        st.markdown("## Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', title='Monthly Activity', markers=True,
                      labels={'time': 'Month-Year', 'message': 'Messages'},
                      color_discrete_sequence=['#636EFA'])
        fig.update_layout(title_x=0.5, height=500, xaxis_tickangle=-45,
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        # -------------------- Daily Timeline -------------------- #
        st.markdown("## Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig = px.line(daily_timeline, x='only_date', y='message', title='Daily Activity', markers=True,
                      labels={'only_date': 'Date', 'message': 'Messages'},
                      color_discrete_sequence=['#00CC96'])
        fig.update_layout(title_x=0.5, height=500,
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        # -------------------- Activity Map -------------------- #
        st.markdown("## Weekly Activity")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            busy_day = busy_day.reindex(day_order).dropna()
            fig = px.bar(x=busy_day.index, y=busy_day.values,
                         labels={'x': 'Day of Week', 'y': 'Messages'},
                         color_discrete_sequence=['#EF553B'], title='Messages per Day')
            fig.update_layout(title_x=0.5, height=400,
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.monthly_timeline(selected_user, df)
            monthly_summary = busy_month.groupby("month")['message'].sum().reindex([
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]).dropna()
            fig = px.bar(x=monthly_summary.index, y=monthly_summary.values,
                         labels={'x': 'Month', 'y': 'Messages'},
                         color_discrete_sequence=['#00CC96'], title='Messages per Month')
            fig.update_layout(title_x=0.5, height=400,
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        # -------------------- Heatmap -------------------- #
        st.markdown("## Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(
            user_heatmap,
            ax=ax,
            cmap="rocket",
            linewidths=0.3,
            linecolor='gray',
            annot=True,
            fmt='.0f',
            cbar_kws={"label": "Messages"},
            square=False
        )
        ax.set_title("Weekly Activity Heatmap", fontsize=18, fontweight='bold', pad=15, color='white')
        ax.set_xlabel("Hour of Day", fontsize=14, color='white')
        ax.set_ylabel("Day of Week", fontsize=14, color='white')
        plt.xticks(rotation=45, color='white')
        plt.yticks(rotation=0, color='white')
        fig.patch.set_facecolor('#1E1E1E')
        ax.set_facecolor('#1E1E1E')
        st.pyplot(fig)

        # -------------------- Busy Users -------------------- #
        if selected_user == 'Overall':
            st.markdown("## Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            chart_col, table_col = st.columns([2, 1])
            with chart_col:
                fig = px.bar(x=x.index, y=x.values, labels={'x': 'User', 'y': 'Messages'},
                             color_discrete_sequence=['#AB63FA'], title='Top Active Users')
                fig.update_layout(xaxis_tickangle=-45, title_x=0.5)
                st.plotly_chart(fig, use_container_width=True)
            with table_col:
                st.dataframe(new_df, use_container_width=True)

        # -------------------- WordCloud -------------------- #
        st.markdown("## WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # -------------------- Most Common Words -------------------- #
        st.markdown("## Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df).head(30)
        most_common_df.columns = ['Word', 'Count']
        fig = px.bar(most_common_df, x='Count', y='Word', orientation='h',
                     color_discrete_sequence=['#FF7F0E'], title='Top 20 Words')
        fig.update_layout(height=800, title_x=0.5,
                          margin=dict(l=120), yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig, use_container_width=True)

        # -------------------- Emoji Analysis -------------------- #
        st.markdown("## Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        if not emoji_df.empty:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig = px.bar(emoji_df.head(10), x='Emoji', y='Count',
                             color_discrete_sequence=['#0097A7'], title='Top Emojis Used')
                fig.update_layout(xaxis_tickfont_size=20, title_x=0.5)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No emojis found for this user.")
