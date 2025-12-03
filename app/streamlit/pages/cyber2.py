
'''
# Convert date column to datetime for graphs
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    col1, col2 = st.columns(2)

    # -------------------------------------------------
    # 3D SCATTER — severity, date, status
    # -------------------------------------------------
    with col1:
        st.subheader("3D Incident Visualization")

        # Plotly 3D scatter
        # px.scatter_3d() → 3D visualization with 3 axis choices
        fig = px.scatter_3d(
            df,
            x='severity',
            y='incident_type',
            z='date',
            color='status',
            title="3D Incident Overview",
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------
    # SUNBURST CHART — Incident Type → Severity → Status
    # -------------------------------------------------
    with col2:
        st.subheader("Threat Breakdown")

        # Sunburst syntax:
        # path = hierarchy order
        fig = px.sunburst(
            df,
            path=['incident_type', 'severity', 'status'],
            title="Incident Category Breakdown"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------
    # TIMELINE (Animated Scatter)
    # -------------------------------------------------
    st.subheader("📅 Incident Timeline")

    # px.scatter() with animation_frame is auto-timeline animation
    fig = px.scatter(
        df,
        x='date',
        y='severity',
        color='incident_type',
        title="Incident Evolution Over Time",
    )
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------
    # HEATMAP: Incident Count by Type × Severity
    # -------------------------------------------------
    st.subheader("🔥 Heatmap of Incidents")

    pivot = df.pivot_table(
        index='incident_type',
        columns='severity',
        values='id',
        aggfunc='count',
        fill_value=0
    )

    heat = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="Reds",
            text=pivot.values,
            texttemplate="%{text}"
        )
    )

    heat.update_layout(
        title="Incident Density Heatmap",
        height=400,
    )
    st.plotly_chart(heat, use_container_width=True)
'''