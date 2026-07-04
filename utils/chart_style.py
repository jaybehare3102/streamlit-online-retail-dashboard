import plotly.graph_objects as go


# ============================================
# Apply Common Dark Theme
# ============================================

def apply_dark_theme(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0f172a",

        plot_bgcolor="#1e293b",

        font=dict(
            family="Segoe UI",
            size=13,
            color="white"
        ),

        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=13,
            font_color="white"
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
    )

    return fig


# ============================================
# Standard Line Chart
# ============================================

def style_line_chart(fig):

    fig.update_traces(

        line=dict(
            color="#3b82f6",
            width=4
        ),

        marker=dict(
            size=8
        )

    )

    return apply_dark_theme(fig)


# ============================================
# Standard Bar Chart
# ============================================

def style_bar_chart(fig):

    fig.update_traces(

        marker_line_width=0,

        opacity=0.95

    )

    return apply_dark_theme(fig)


# ============================================
# Standard Scatter Chart
# ============================================

def style_scatter_chart(fig):

    fig.update_traces(

        marker=dict(
            line=dict(
                width=1,
                color="white"
            ),
            opacity=0.8
        )

    )

    return apply_dark_theme(fig)


# ============================================
# Standard Pie / Donut Chart
# ============================================

def style_pie_chart(fig):

    fig.update_traces(

        textinfo="percent+label",

        textfont_size=13

    )

    return apply_dark_theme(fig)