import streamlit as st
import plotly.graph_objects as go
import numpy as np
from surface import compute_surface

st.set_page_config(page_title="IV Surface Dashboard", layout="wide")
st.title("Implied Volatility Surface Dashboard")
st.markdown("Computes implied volatility from live options data using Black-Scholes and numerical root-finding.")

# --- USER INPUT ---
ticker = st.text_input("Ticker Symbol", value="SPY").upper()
compute = st.button("Compute Surface")

if compute:
    with st.spinner("Fetching options and computing IV..."):
        df = compute_surface(ticker)

    if df.empty or len(df) < 5:
        st.error("Not enough options data. Try a more liquid ticker like SPY or AAPL.")
    else:
        # Filter outliers: keep IV below 200%
        df = df[df["iv"] < 2.0]

        # Show summary stats
        spot = df["spot"].iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Spot Price", f"${spot:.2f}")
        col2.metric("Options Analysed", f"{len(df)}")
        col3.metric("Expiry Dates", f"{df['expiry'].nunique()}")
        col4.metric("Mean IV", f"{df['iv'].mean():.1%}")

        # --- 3D SURFACE PLOT ---
        st.subheader("3D Volatility Surface")

        calls = df[df["option_type"] == "call"]
        puts = df[df["option_type"] == "put"]

        fig_3d = go.Figure()

        if len(calls) > 0:
            fig_3d.add_trace(go.Scatter3d(
                x=calls["strike"],
                y=calls["days_to_expiry"],
                z=calls["iv"] * 100,
                mode="markers",
                marker=dict(size=4, color=calls["iv"] * 100, colorscale="Viridis"),
                name="Calls",
                text=[f"Strike: {s}<br>Expiry: {e}<br>IV: {iv:.1%}"
                      for s, e, iv in zip(calls["strike"], calls["expiry"], calls["iv"])],
                hoverinfo="text"
            ))

        if len(puts) > 0:
            fig_3d.add_trace(go.Scatter3d(
                x=puts["strike"],
                y=puts["days_to_expiry"],
                z=puts["iv"] * 100,
                mode="markers",
                marker=dict(size=4, color=puts["iv"] * 100, colorscale="Plasma"),
                name="Puts",
                text=[f"Strike: {s}<br>Expiry: {e}<br>IV: {iv:.1%}"
                      for s, e, iv in zip(puts["strike"], puts["expiry"], puts["iv"])],
                hoverinfo="text"
            ))

        fig_3d.update_layout(
            scene=dict(
                xaxis_title="Strike Price ($)",
                yaxis_title="Days to Expiry",
                zaxis_title="Implied Volatility (%)"
            ),
            height=600,
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig_3d, use_container_width=True)

        # --- 2D SMILE PLOT ---
        st.subheader("Volatility Smile (by Expiry)")

        expiry_options = sorted(df["expiry"].unique())
        selected_expiry = st.selectbox("Select expiry date", expiry_options)

        smile_data = df[df["expiry"] == selected_expiry]

        fig_smile = go.Figure()

        smile_calls = smile_data[smile_data["option_type"] == "call"]
        smile_puts = smile_data[smile_data["option_type"] == "put"]

        if len(smile_calls) > 0:
            fig_smile.add_trace(go.Scatter(
                x=smile_calls["strike"],
                y=smile_calls["iv"] * 100,
                mode="markers+lines",
                name="Calls",
                marker=dict(size=8)
            ))

        if len(smile_puts) > 0:
            fig_smile.add_trace(go.Scatter(
                x=smile_puts["strike"],
                y=smile_puts["iv"] * 100,
                mode="markers+lines",
                name="Puts",
                marker=dict(size=8)
            ))

        fig_smile.add_vline(x=spot, line_dash="dash", line_color="gray",
                           annotation_text=f"Spot: ${spot:.0f}")

        fig_smile.update_layout(
            xaxis_title="Strike Price ($)",
            yaxis_title="Implied Volatility (%)",
            title=f"IV Smile — {ticker} — Expiry: {selected_expiry}",
            height=450
        )

        st.plotly_chart(fig_smile, use_container_width=True)