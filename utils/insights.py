import streamlit as st


def render_insights(insights):

    """
    insights = [
        ("🏆 Highest Revenue","Customer 14646"),
        ("⭐ Most Orders","Customer 17841"),
        ("💰 Highest AOV","£3,420")
    ]
    """

    st.subheader("💡 Business Insights")

    cols = st.columns(len(insights))

    for col, item in zip(cols, insights):

        title, value = item

        with col:

            st.info(
                f"""
**{title}**

{value}
"""
            )