"""
ui/charts.py -- Plotly chart builders for the simulator.
"""
from __future__ import annotations
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import SystemConfig
from analysis.eye_diagram import compute_eye_diagram
from ui.styles import chart_tokens

CHANNEL_COLORS = [
    "#3D9DF3", "#6EA8FF", "#7BD7B0", "#F2C66D",
    "#B8A7FF", "#F0A7C1", "#8BE0D0", "#A9B4C2",
]
SCENARIO_META = {
    "no_encryption": dict(label="Without Secure",           color="#3D9DF3", dash="solid"),
    "encryption":    dict(label="With Secure + EDFA",       color="#F28A9B", dash="dash"),
    "dcf_edfa":      dict(label="With Secure + EDFA + DCF", color="#7BD7B0", dash="dashdot"),
}


def _axis_color(theme: str) -> str:
    """Return a clearly visible axis / tick colour for both themes."""
    if theme == "dark":
        return chart_tokens(theme)["text"]
    return "#0f1923"


def _grid_color(theme: str) -> str:
    """Visible grid-line colour per theme."""
    if theme == "dark":
        return chart_tokens(theme)["grid"]
    return "rgba(61, 157, 243, 0.20)"


def _line_color(theme: str) -> str:
    """Axis spine colour per theme."""
    if theme == "dark":
        return chart_tokens(theme).get("border2", _grid_color(theme))
    return "rgba(61, 157, 243, 0.28)"


def _layout(theme="dark"):
    tokens = chart_tokens(theme)
    return dict(
        template="plotly_dark" if theme == "dark" else "plotly_white",
        paper_bgcolor=tokens["chart_bg"],
        plot_bgcolor=tokens["plot_bg"],
        font=dict(
            family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
            color=_axis_color(theme),
            size=12,
        ),
        margin=dict(l=72, r=36, t=96, b=176),
        hoverlabel=dict(
            bgcolor=tokens["surface"],
            font_color=tokens["text"],
            bordercolor=tokens["cyan"],
            font_size=12,
        ),
    )


def _legend(theme="dark"):
    tokens = chart_tokens(theme)
    return dict(
        bgcolor=tokens["surface"],
        bordercolor=_line_color(theme),
        borderwidth=1,
        font=dict(color=_axis_color(theme), size=11),
        orientation="h",
        yanchor="top",
        y=-0.30,
        xanchor="center",
        x=0.5,
    )


def _title(text, theme="dark", size=14):
    return dict(
        text=text,
        font=dict(size=size, color=_axis_color(theme)),
        x=0.5,
        y=0.96,
        xref="container",
        xanchor="center",
        yanchor="top",
    )


def _xa(t, theme="dark"):
    tc = _axis_color(theme)
    return dict(
        title=dict(text=t, standoff=28, font=dict(color=tc)),
        showgrid=True, gridcolor=_grid_color(theme),
        showline=True, linecolor=_line_color(theme), linewidth=1,
        zeroline=False, ticks="outside", ticklen=4,
        tickcolor=tc, tickfont=dict(color=tc),
        automargin=True,
    )


def _ya(t, log=False, r=None, theme="dark"):
    tc = _axis_color(theme)
    d = dict(
        title=dict(text=t, font=dict(color=tc)),
        showgrid=True, gridcolor=_grid_color(theme),
        showline=True, linecolor=_line_color(theme), linewidth=1,
        zeroline=False, ticks="outside", ticklen=4,
        tickcolor=tc, tickfont=dict(color=tc),
        automargin=True,
    )
    if log: d["type"] = "log"
    if r: d["range"] = r
    return d


def plot_waveforms(result, cfg, theme="dark"):
    t=result.time_ns; dn=min(4.0,t[-1]); m=t<=dn
    panels=[
        ("(a) Input NRZ","#3D9DF3",result.nrz_signal),
        ("(b) Encrypted RC4","#F28A9B",result.encrypted_nrz),
        ("(c) Optical TX (mW)","#7BD7B0",result.optical_power_in),
        ("(d) Optical RX (mW)","#F2C66D",result.optical_power_out),
        ("(e) Photocurrent (uA)","#B8A7FF",result.photocurrent),
        ("(f) After Filter (uA)","#F0A7C1",result.filtered_signal),
    ]
    fig=make_subplots(rows=3,cols=2,subplot_titles=[p[0] for p in panels],vertical_spacing=0.20,horizontal_spacing=0.08)
    pos=[(1,1),(1,2),(2,1),(2,2),(3,1),(3,2)]
    yl=["Amplitude","Amplitude","Power (mW)","Power (mW)","Current (uA)","Current (uA)"]
    tc = _axis_color(theme)
    gc = _grid_color(theme)
    lc = _line_color(theme)
    for (title,color,data),(r,c),ylabel in zip(panels,pos,yl):
        fig.add_trace(go.Scatter(x=t[m],y=data[m],mode="lines",line=dict(color=color,width=1.2),name=title,showlegend=False,hovertemplate="t=%{x:.3f} ns<br>val=%{y:.4f}<extra></extra>"),row=r,col=c)
        an="" if (r==1 and c==1) else str((r-1)*2+c)
        fig.update_layout(**{
            f"xaxis{an}": dict(
                title=dict(text="Time (ns)", standoff=20, font=dict(color=tc)),
                gridcolor=gc, showline=True, linecolor=lc, linewidth=1,
                zeroline=False, automargin=True,
                tickcolor=tc, tickfont=dict(color=tc),
            ),
            f"yaxis{an}": dict(
                title=dict(text=ylabel, standoff=20, font=dict(color=tc)),
                gridcolor=gc, showline=True, linecolor=lc, linewidth=1,
                zeroline=False, automargin=True,
                tickcolor=tc, tickfont=dict(color=tc),
            )
        })
    fig.update_layout(**_layout(theme),height=780,title=_title(f"Signal Waveforms | {result.scenario} | L={cfg.fiber_length_km:.0f} km | Q={result.empirical_q:.2f} | BER={result.empirical_ber:.2e}", theme, 13))
    fig.update_layout(margin=dict(b=60))
    fig.update_annotations(font_color=_axis_color(theme))
    return fig


def plot_q_factor(sweeps, cfg, theme="dark"):
    distances=next(iter(sweeps.values())).distances_km; fig=go.Figure()
    for si,(sc,sw) in enumerate(sweeps.items()):
        meta=SCENARIO_META[sc]
        for i,(wl,Q) in enumerate(sw.q_per_channel.items()):
            fig.add_trace(go.Scatter(x=distances,y=Q,mode="lines",name=f"L{i+1}={wl} nm",line=dict(color=CHANNEL_COLORS[i%8],width=1.8,dash=meta["dash"]),legendgroup=f"ch{i}",showlegend=(si==0),opacity=0.9,hovertemplate=f"<b>L{i+1}={wl} nm</b><br>Scenario: {meta['label']}<br>Dist: %{{x:.1f}} km<br>Q: %{{y:.3f}}<extra></extra>"))
    fig.add_hline(y=cfg.q_threshold,line=dict(color="#F2C66D",width=1.5,dash="dot"),annotation_text=f"Q={cfg.q_threshold} (ITU)",annotation_position="top left",annotation_font=dict(color="#F2C66D",size=10))
    for x,col,lb in [(77.4,"#3D9DF3","No Enc<br>77.4 km"),(63.0,"#F28A9B","Enc<br>63 km"),(100.0,"#7BD7B0","+DCF<br>100 km")]:
        fig.add_vline(x=x,line=dict(color=col,width=1.2,dash="dashdot"),annotation_text=lb,annotation_position="top",annotation_font=dict(color=col,size=9))
    for sc,meta in SCENARIO_META.items():
        fig.add_trace(go.Scatter(x=[None],y=[None],mode="lines",name=meta["label"],line=dict(color=_axis_color(theme) if theme=="light" else "#A9B4C2",width=2,dash=meta["dash"]),legendgroup="scenarios",legendgrouptitle_text="Scenarios",showlegend=True))
    fig.update_layout(**_layout(theme),height=580,title=_title("Q-Factor vs Link Distance -- 8 WDM Channels", theme, 14),xaxis=_xa("Link Distance (km)", theme),yaxis=_ya("Q-Factor",r=[0,72], theme=theme),legend=dict(**_legend(theme),groupclick="toggleitem"))
    return fig


def plot_ber(sweeps, cfg, theme="dark"):
    distances=next(iter(sweeps.values())).distances_km; fig=go.Figure()
    for si,(sc,sw) in enumerate(sweeps.items()):
        meta=SCENARIO_META[sc]
        for i,(wl,BER) in enumerate(sw.ber_per_channel.items()):
            bs=np.clip(np.asarray(BER,dtype=float),1e-12,1.0)
            fig.add_trace(go.Scatter(x=distances,y=bs,mode="lines",name=f"L{i+1}={wl} nm",line=dict(color=CHANNEL_COLORS[i%8],width=1.8,dash=meta["dash"]),legendgroup=f"ch{i}",showlegend=(si==0),opacity=0.9,hovertemplate=f"<b>L{i+1}={wl} nm</b><br>Scenario: {meta['label']}<br>Dist: %{{x:.1f}} km<br>BER: %{{y:.3e}}<extra></extra>"))
    fig.add_hline(y=1e-9,line=dict(color="#F2C66D",width=1.5,dash="dot"),annotation_text="BER=10^-9 (ITU)",annotation_position="top left",annotation_font=dict(color="#F2C66D",size=10))
    for x,col,lb in [(77.4,"#3D9DF3","No Enc<br>77.4 km"),(63.0,"#F28A9B","Enc<br>63 km"),(100.0,"#7BD7B0","+DCF<br>100 km")]:
        fig.add_vline(x=x,line=dict(color=col,width=1.2,dash="dashdot"),annotation_text=lb,annotation_position="top",annotation_font=dict(color=col,size=9))
    for sc,meta in SCENARIO_META.items():
        fig.add_trace(go.Scatter(x=[None],y=[None],mode="lines",name=meta["label"],line=dict(color=_axis_color(theme) if theme=="light" else "#A9B4C2",width=2,dash=meta["dash"]),legendgroup="scenarios",legendgrouptitle_text="Scenarios",showlegend=True))
    fig.update_layout(**_layout(theme),height=580,title=_title("BER vs Link Distance -- Log Scale -- 8 WDM Channels", theme, 14),xaxis=_xa("Link Distance (km)", theme),yaxis=_ya("BER",log=True, theme=theme),legend=dict(**_legend(theme),groupclick="toggleitem"))
    return fig


def plot_single_scenario(sweep, cfg, theme="dark"):
    distances=sweep.distances_km; meta=SCENARIO_META.get(sweep.scenario,dict(label=sweep.scenario,color="#4DA3FF",dash="solid"))
    fig=make_subplots(rows=1,cols=2,subplot_titles=[f"Q-Factor -- {meta['label']}",f"BER -- {meta['label']}"],horizontal_spacing=0.1)
    for i,((wl,Q),(_,BER)) in enumerate(zip(sweep.q_per_channel.items(),sweep.ber_per_channel.items())):
        c=CHANNEL_COLORS[i%8]; lb=f"L{i+1}={wl} nm"; bs=np.clip(np.asarray(BER,dtype=float),1e-12,1.0)
        fig.add_trace(go.Scatter(x=distances,y=Q,mode="lines",name=lb,line=dict(color=c,width=1.8),legendgroup=f"ch{i}",hovertemplate=f"<b>{lb}</b><br>Dist: %{{x:.1f}} km<br>Q: %{{y:.3f}}<extra></extra>"),row=1,col=1)
        fig.add_trace(go.Scatter(x=distances,y=bs,mode="lines",name=lb,line=dict(color=c,width=1.8),legendgroup=f"ch{i}",showlegend=False,hovertemplate=f"<b>{lb}</b><br>Dist: %{{x:.1f}} km<br>BER: %{{y:.3e}}<extra></extra>"),row=1,col=2)
    fig.add_hline(y=cfg.q_threshold,line=dict(color="#F2C66D",width=1.2,dash="dot"),row=1,col=1)
    fig.add_hline(y=1e-9,line=dict(color="#F2C66D",width=1.2,dash="dot"),row=1,col=2)
    fig.update_layout(**_layout(theme),height=540,title=_title(f"Individual Scenario -- {meta['label']}", theme, 13),legend=_legend(theme))
    tc2 = _axis_color(theme)
    gc2 = _grid_color(theme)
    lc2 = _line_color(theme)
    fig.update_xaxes(title_text="Link Distance (km)",title_standoff=28,gridcolor=gc2,showline=True,linecolor=lc2,linewidth=1,tickcolor=tc2,tickfont=dict(color=tc2),automargin=True)
    fig.update_xaxes(title_font=dict(color=tc2), tickfont=dict(color=tc2))
    fig.update_yaxes(title_text="Q-Factor",title_font=dict(color=tc2),gridcolor=gc2,showline=True,linecolor=lc2,linewidth=1,tickcolor=tc2,tickfont=dict(color=tc2),range=[0,72],row=1,col=1)
    fig.update_yaxes(title_text="BER",title_font=dict(color=tc2),gridcolor=gc2,showline=True,linecolor=lc2,linewidth=1,tickcolor=tc2,tickfont=dict(color=tc2),type="log",dtick=3,row=1,col=2)
    fig.update_annotations(font_color=_axis_color(theme))
    return fig


def plot_eye_grid(results, cfg, theme="dark"):
    n=len(results)
    cols_meta=[
        (["#3D9DF3","#1f3a6e"],"Without Secure"),
        (["#F28A9B","#6b1010"],"With Secure + EDFA"),
        (["#7BD7B0","#1a5c1a"],"With Secure + EDFA + DCF"),
    ][:n]
    titles=[f"{r.scenario}<br><sub>Q={r.empirical_q:.1f}</sub>" for r in results]
    fig=make_subplots(rows=1,cols=n,subplot_titles=titles,horizontal_spacing=0.06)
    for ci,(res,(pal,_)) in enumerate(zip(results,cols_meta)):
        t_norm,traces,_=compute_eye_diagram(res.filtered_signal,cfg,n_traces=200)
        for ty in traces:
            fig.add_trace(go.Scattergl(x=t_norm,y=ty,mode="lines",line=dict(color=pal[0],width=0.6),opacity=0.18,showlegend=False,hoverinfo="skip"),row=1,col=ci+1)
        for xm in (0.5,1.5):
            fig.add_trace(go.Scatter(x=[xm,xm],y=[traces.min(),traces.max()],mode="lines",line=dict(color="#F28A9B",width=1.2,dash="dash"),showlegend=(ci==0 and xm==0.5),name="Sample instant",legendgroup="sample",hoverinfo="skip"),row=1,col=ci+1)
    fig.update_layout(**_layout(theme),height=520,title=_title("Eye Diagrams -- Received Signal after Bessel Filter", theme, 13),legend=_legend(theme))
    fig.update_layout(margin=dict(t=120, b=150))
    tc3 = _axis_color(theme)
    gc3 = _grid_color(theme)
    lc3 = _line_color(theme)
    fig.update_xaxes(title_text="Time (bit period)",title_font=dict(color=tc3),title_standoff=28,gridcolor=gc3,showline=True,linecolor=lc3,linewidth=1,tickcolor=tc3,tickfont=dict(color=tc3),range=[0,2],automargin=True)
    fig.update_yaxes(title_text="Normalised Amplitude",title_font=dict(color=tc3),gridcolor=gc3,showline=True,linecolor=lc3,linewidth=1,tickcolor=tc3,tickfont=dict(color=tc3))
    fig.update_annotations(font_color=_axis_color(theme))
    return fig
