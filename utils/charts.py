import plotly.express as px


# ==========================================================
# Common Theme
# ==========================================================

def apply_dark_theme(fig):

    fig.update_layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(
            color="white",
            size=13
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
        legend=dict(
            bgcolor="#0f172a",
            font=dict(color="white")
        )
    )

    return fig


# ==========================================================
# Horizontal Bar Chart
# ==========================================================

def horizontal_bar_chart(
    df,
    x,
    y,
    title,
    color,
    colorscale,
    height=450
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        color=color,
        color_continuous_scale=colorscale,
        template="plotly_dark",
        text_auto=".2s"
    )

    fig.update_layout(
        title=title,
        height=height,
        xaxis_title="",
        yaxis_title="",
        coloraxis_showscale=False
    )

    return apply_dark_theme(fig)


# ==========================================================
# Vertical Bar Chart
# ==========================================================

def vertical_bar_chart(
    df,
    x,
    y,
    title,
    color,
    colorscale,
    height=450
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        color_continuous_scale=colorscale,
        template="plotly_dark",
        text_auto=True
    )

    fig.update_layout(
        title=title,
        height=height,
        coloraxis_showscale=False
    )

    return apply_dark_theme(fig)


# ==========================================================
# Line Chart
# ==========================================================

def line_chart(
    df,
    x,
    y,
    title,
    height=450
):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        template="plotly_dark"
    )

    fig.update_layout(
        title=title,
        height=height
    )

    return apply_dark_theme(fig)


# ==========================================================
# Scatter Chart
# ==========================================================

def scatter_chart(
    df,
    x,
    y,
    size,
    color,
    title,
    colorscale="Viridis",
    height=450
):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        color_continuous_scale=colorscale,
        template="plotly_dark"
    )

    fig.update_layout(
        title=title,
        height=height,
        coloraxis_showscale=False
    )

    return apply_dark_theme(fig)


# ==========================================================
# Donut Chart
# ==========================================================

def donut_chart(
    df,
    names,
    values,
    title,
    colors,
    height=450
):

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.55,
        color=names,
        color_discrete_sequence=colors,
        template="plotly_dark"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        title=title,
        height=height
    )

    return apply_dark_theme(fig)


# ==========================================================
# Histogram
# ==========================================================

def histogram_chart(
    df,
    x,
    title,
    color="#8B5CF6",
    height=450
):

    fig = px.histogram(
        df,
        x=x,
        nbins=30,
        template="plotly_dark",
        color_discrete_sequence=[color]
    )

    fig.update_layout(
        title=title,
        height=height
    )

    return apply_dark_theme(fig)




# ==========================================================
# Treemap Chart
# ==========================================================

def treemap_chart(
    df,
    names,
    values,
    title,
    colorscale="Viridis",
    height=500
):

    fig = px.treemap(
        df,
        path=[names],
        values=values,
        color=values,
        color_continuous_scale=colorscale
    )

    fig.update_layout(
        title=title,
        height=height
    )

    return apply_dark_theme(fig)



# ==========================================================
# Box Plot
# ==========================================================

def box_plot(
    df,
    x,
    y,
    title,
    color=None,
    height=450
):

    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        template="plotly_dark"
    )

    fig.update_layout(
        title=title,
        height=height
    )

    return apply_dark_theme(fig)



# ==========================================================
# Heatmap
# ==========================================================

def heatmap_chart(
    pivot_df,
    title,
    height=500
):

    fig = px.imshow(
        pivot_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        title=title,
        height=height
    )

    return apply_dark_theme(fig)