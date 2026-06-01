"""
ui/styles/motion.py — Premium Vercel/Linear-grade motion polish.

Adds hover lifts, fade-up entrances, scroll reveals, count-up numbers,
shimmer skeletons, navbar scroll states, chart entry animations,
smooth focus rings, animated form labels, drag-state feedback,
ambient background orbs, scroll progress indicator, and subtle parallax.

Pure CSS + a lightweight IntersectionObserver / count-up JS shim.
Does NOT change colors, typography, layout, spacing, or any content.
Fully respects prefers-reduced-motion.

Usage:
    from ui.styles.motion import inject_motion
    inject_motion()   # call once, after inject_theme()
"""

from __future__ import annotations
import streamlit as st


_MOTION_CSS = r"""
<style id="swdm-motion">
/* ─────────────────────────────────────────────
   EASING & TIMING TOKENS  (motion only)
───────────────────────────────────────────── */
:root {
  --mo-ease:        cubic-bezier(.22,.61,.36,1);
  --mo-ease-out:    cubic-bezier(.16,1,.3,1);
  --mo-spring:      cubic-bezier(.34,1.56,.64,1);
  --mo-fast:        150ms;
  --mo-med:         280ms;
  --mo-slow:        480ms;
  --mo-slower:      640ms;
}

/* ─────────────────────────────────────────────
   GPU LAYER HINT  — promote animated elements
───────────────────────────────────────────── */
.metric-card, .flow-node, .workstation-panel, .panel-card,
.soft-card, .block-card, .contact-card, .theory-intro,
.simulator-intro, .summary-table-card,
[data-testid="stMetric"],
[data-testid="stButton"] > button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"],
.stDownloadButton > button,
.swdm-nav-item, a.swdm-nav-item,
.swdm-sidebar,
[data-testid="stPlotlyChart"],
[data-testid="stImage"] img {
  will-change: transform;
  transform: translateZ(0);
}

/* ─────────────────────────────────────────────
   GLOBAL TRANSITION BASELINE
───────────────────────────────────────────── */
.metric-card, .flow-node, .workstation-panel, .panel-card,
.soft-card, .block-card, .contact-card, .theory-intro,
.simulator-intro, .summary-table-card,
[data-testid="stMetric"],
[data-testid="stButton"] > button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"],
.stDownloadButton > button,
.swdm-nav-item, a.swdm-nav-item,
[data-testid="stFileUploaderDropzone"],
[data-testid="stExpander"] summary {
  transition:
    transform     var(--mo-med) var(--mo-ease-out),
    box-shadow    var(--mo-med) var(--mo-ease-out),
    border-color  var(--mo-med) var(--mo-ease-out),
    opacity       var(--mo-med) var(--mo-ease-out),
    background    var(--mo-med) var(--mo-ease-out) !important;
}

/* ─────────────────────────────────────────────
   CARD  HOVER LIFT
───────────────────────────────────────────── */
.metric-card:hover, .flow-node:hover, .panel-card:hover,
.soft-card:hover, .block-card:hover, .theory-intro:hover,
.summary-table-card:hover {
  transform: translateY(-3px) translateZ(0);
  box-shadow: 0 16px 40px -12px rgba(0,0,0,.42),
              0 4px 10px  -4px rgba(0,0,0,.22);
  border-color: var(--accent-bdr, rgba(125,220,255,.28)) !important;
}

.workstation-panel:hover, .simulator-intro:hover {
  transform: translateY(-2px) translateZ(0);
  box-shadow: 0 22px 52px -22px rgba(0,0,0,.44);
}

[data-testid="stMetric"]:hover {
  transform: translateY(-2px) translateZ(0);
  box-shadow: 0 14px 36px -10px rgba(0,0,0,.38) !important;
  border-color: var(--accent-bdr, rgba(125,220,255,.24)) !important;
}

/* ─────────────────────────────────────────────
   BUTTONS — premium micro-interactions
───────────────────────────────────────────── */
[data-testid="stButton"] > button,
.stDownloadButton > button {
  position: relative;
  overflow: hidden;
}

/* Highlight sweep on primary CTA */
[data-testid="stButton"] > button::after {
  content: "";
  position: absolute;
  top: 0; left: -100%;
  width: 60%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255,255,255,.14) 50%,
    transparent 100%
  );
  transition: left var(--mo-slow) var(--mo-ease-out);
  pointer-events: none;
}

[data-testid="stButton"] > button:hover::after {
  left: 160%;
}

[data-testid="stButton"] > button:hover,
.stDownloadButton > button:hover {
  transform: translateY(-2px) translateZ(0);
  box-shadow: 0 12px 28px -8px rgba(0,0,0,.38),
              0 0 0 1px rgba(125,220,255,.18);
}

[data-testid="stButton"] > button:active,
.stDownloadButton > button:active {
  transform: translateY(0) scale(.984) translateZ(0);
  transition-duration: 80ms !important;
}

/* ─────────────────────────────────────────────
   SIDEBAR  — blur on load / scroll
───────────────────────────────────────────── */
.swdm-sidebar {
  transition:
    backdrop-filter  var(--mo-slow) var(--mo-ease),
    box-shadow       var(--mo-med)  var(--mo-ease),
    background       var(--mo-med)  var(--mo-ease) !important;
}

/* ─────────────────────────────────────────────
   SIDEBAR NAV — left-bar active indicator
───────────────────────────────────────────── */
.swdm-nav-item { position: relative; }

.swdm-nav-item::before {
  content: "";
  position: absolute;
  left: 0; top: 18%; bottom: 18%;
  width: 2.5px;
  border-radius: 2.5px;
  background: var(--accent, #7ddcff);
  transform: scaleY(0);
  transform-origin: center;
  transition: transform var(--mo-med) var(--mo-ease-out),
              opacity   var(--mo-med) var(--mo-ease-out);
  opacity: 0;
}

.swdm-nav-item:hover::before {
  transform: scaleY(0.7);
  opacity: 0.6;
}

.swdm-nav-item.active::before {
  transform: scaleY(1);
  opacity: 1;
}

/* Smooth hover slide */
.swdm-nav-item:hover {
  transform: translateX(3px) translateZ(0);
}

.swdm-nav-item.active {
  transform: translateX(2px) translateZ(0);
}

/* ─────────────────────────────────────────────
   NAVBAR LINKS — animated underline sweep
───────────────────────────────────────────── */
.swdm-navlink, .navbar a, .swdm-nav a {
  position: relative;
}
.swdm-navlink::after, .navbar a::after, .swdm-nav a::after {
  content: "";
  position: absolute;
  left: 0; bottom: -2px;
  height: 1.5px; width: 100%;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right center;
  transition: transform var(--mo-med) var(--mo-ease-out);
}
.swdm-navlink:hover::after, .navbar a:hover::after, .swdm-nav a:hover::after {
  transform: scaleX(1);
  transform-origin: left center;
}

/* ─────────────────────────────────────────────
   NAVBAR SCROLL STATE  (scrolled class set by JS)
───────────────────────────────────────────── */
.swdm-navbar, [data-testid="stHeader"] {
  transition:
    backdrop-filter  var(--mo-med) var(--mo-ease),
    background-color var(--mo-med) var(--mo-ease),
    box-shadow       var(--mo-med) var(--mo-ease) !important;
}

html.scrolled .swdm-navbar,
html.scrolled [data-testid="stHeader"] {
  backdrop-filter: saturate(150%) blur(18px);
  -webkit-backdrop-filter: saturate(150%) blur(18px);
  box-shadow: 0 4px 20px -8px rgba(0,0,0,.32);
}

/* ─────────────────────────────────────────────
   FORM  INPUTS — smooth focus rings + label float
───────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
  transition:
    border-color  var(--mo-med) var(--mo-ease),
    box-shadow    var(--mo-med) var(--mo-ease),
    background    var(--mo-med) var(--mo-ease) !important;
}

[data-testid="stTextInput"] input:focus {
  border-color: var(--accent, #7ddcff) !important;
  box-shadow: 0 0 0 3px rgba(125,220,255,.14) !important;
  outline: none !important;
}

[data-testid="stTextInput"] input:hover {
  border-color: var(--border-strong, rgba(226,239,255,.22)) !important;
}

/* Slider track / thumb micro-interaction */
[data-testid="stSlider"] > div > div > div {
  transition: transform var(--mo-fast) var(--mo-ease) !important;
}

/* Smooth checkbox + toggle */
[data-testid="stCheckbox"] label,
[data-testid="stToggle"]   label {
  transition: color var(--mo-fast) var(--mo-ease) !important;
}

[data-testid="stToggle"] [role="switch"] {
  transition: background-color var(--mo-med) var(--mo-ease) !important;
}

/* Expander smooth open */
[data-testid="stExpander"] summary {
  transition:
    background var(--mo-med) var(--mo-ease),
    color      var(--mo-fast) var(--mo-ease) !important;
}

[data-testid="stExpander"] summary:hover {
  background: rgba(125,220,255,.07) !important;
}

/* Dropdown list elegant entrance */
[data-baseweb="popover"],
[data-baseweb="menu"] {
  animation: swdm-dropdown-in var(--mo-med) var(--mo-ease-out) both !important;
}

@keyframes swdm-dropdown-in {
  from { opacity: 0; transform: translateY(-6px) scale(.97); }
  to   { opacity: 1; transform: translateY(0)   scale(1); }
}

/* ─────────────────────────────────────────────
   FILE UPLOAD AREA
───────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {
  transition:
    transform        var(--mo-med) var(--mo-ease-out),
    border-color     var(--mo-med) var(--mo-ease),
    background-color var(--mo-med) var(--mo-ease),
    box-shadow       var(--mo-med) var(--mo-ease) !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
  border-color: var(--accent, #7ddcff) !important;
  background-color: rgba(125,220,255,.05) !important;
  box-shadow: 0 0 0 4px rgba(125,220,255,.08),
              inset 0 0 24px rgba(125,220,255,.04) !important;
}

[data-testid="stFileUploaderDropzone"][data-drag-active="true"],
[data-testid="stFileUploaderDropzone"].drag-active {
  transform: scale(1.014) translateZ(0);
  border-color: var(--accent, #7ddcff) !important;
  box-shadow: 0 0 0 6px rgba(125,220,255,.12),
              0 12px 32px rgba(125,220,255,.14) !important;
}

/* ─────────────────────────────────────────────
   TABS  — smooth indicator transition
───────────────────────────────────────────── */
.stTabs [data-baseweb="tab"] {
  transition:
    color       var(--mo-fast) var(--mo-ease),
    background  var(--mo-fast) var(--mo-ease) !important;
}

/* ─────────────────────────────────────────────
   TABLE ROWS
───────────────────────────────────────────── */
[data-testid="stTable"] tbody tr,
[data-testid="stDataFrame"] [role="row"] {
  transition: background-color var(--mo-fast) var(--mo-ease);
}
[data-testid="stTable"] tbody tr:hover {
  background-color: rgba(125,220,255,.05);
}

/* ─────────────────────────────────────────────
   IMAGES  — hover zoom + lazy-load fade-in
───────────────────────────────────────────── */
[data-testid="stImage"] img {
  transition:
    transform  var(--mo-slow)  var(--mo-ease-out),
    opacity    var(--mo-med)   var(--mo-ease-out) !important;
}

[data-testid="stImage"]:hover img {
  transform: scale(1.018) translateZ(0);
}

/* ─────────────────────────────────────────────
   CONTACT CARDS
───────────────────────────────────────────── */
.contact-card {
  transition:
    transform     var(--mo-med) var(--mo-ease-out),
    border-color  var(--mo-med) var(--mo-ease),
    box-shadow    var(--mo-med) var(--mo-ease),
    background    var(--mo-med) var(--mo-ease) !important;
}

.contact-card:hover {
  transform: translateY(-2px) translateX(1px) translateZ(0) !important;
  box-shadow: 0 12px 28px -8px rgba(0,0,0,.36) !important;
}

/* ─────────────────────────────────────────────
   THEME PILL (sidebar footer CTA)
───────────────────────────────────────────── */
.theme-pill, .sidebar-theme-pill {
  transition:
    transform   var(--mo-med) var(--mo-ease-out),
    box-shadow  var(--mo-med) var(--mo-ease-out) !important;
}
.theme-pill:hover, .sidebar-theme-pill:hover {
  transform: translateY(-1.5px) translateZ(0) !important;
}

/* ─────────────────────────────────────────────
   FADE-UP ENTRANCE KEYFRAME  (core animation)
───────────────────────────────────────────── */
@keyframes swdm-fade-up {
  from { opacity: 0; transform: translateY(14px) translateZ(0); }
  to   { opacity: 1; transform: translateY(0)    translateZ(0); }
}

@keyframes swdm-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* ─────────────────────────────────────────────
   SCROLL REVEAL  (.swdm-reveal + .is-visible)
───────────────────────────────────────────── */
.swdm-reveal {
  opacity: 0;
  transform: translateY(14px) translateZ(0);
  transition:
    opacity   var(--mo-slow)   var(--mo-ease-out),
    transform var(--mo-slow)   var(--mo-ease-out);
}
.swdm-reveal.is-visible {
  opacity: 1;
  transform: translateY(0) translateZ(0);
}

/* ─────────────────────────────────────────────
   STAGGER GRID  (tags: .swdm-stagger on parent)
───────────────────────────────────────────── */
.swdm-stagger > * {
  opacity: 0;
  transform: translateY(14px) translateZ(0);
  animation: swdm-fade-up var(--mo-slow) var(--mo-ease-out) forwards;
}
.swdm-stagger > *:nth-child(1) { animation-delay:  40ms; }
.swdm-stagger > *:nth-child(2) { animation-delay: 100ms; }
.swdm-stagger > *:nth-child(3) { animation-delay: 160ms; }
.swdm-stagger > *:nth-child(4) { animation-delay: 220ms; }
.swdm-stagger > *:nth-child(5) { animation-delay: 280ms; }
.swdm-stagger > *:nth-child(6) { animation-delay: 340ms; }
.swdm-stagger > *:nth-child(7) { animation-delay: 400ms; }
.swdm-stagger > *:nth-child(8) { animation-delay: 460ms; }

/* ─────────────────────────────────────────────
   METRIC GRID  & FLOW STRIP — auto stagger
───────────────────────────────────────────── */
.metric-grid > .metric-card,
.flow-strip  > .flow-node {
  opacity: 0;
  transform: translateY(14px) translateZ(0);
  animation: swdm-fade-up var(--mo-slow) var(--mo-ease-out) forwards;
}
.metric-grid > .metric-card:nth-child(1),
.flow-strip  > .flow-node:nth-child(1) { animation-delay:  40ms; }
.metric-grid > .metric-card:nth-child(2),
.flow-strip  > .flow-node:nth-child(2) { animation-delay: 100ms; }
.metric-grid > .metric-card:nth-child(3),
.flow-strip  > .flow-node:nth-child(3) { animation-delay: 160ms; }
.metric-grid > .metric-card:nth-child(4),
.flow-strip  > .flow-node:nth-child(4) { animation-delay: 220ms; }
.metric-grid > .metric-card:nth-child(5),
.flow-strip  > .flow-node:nth-child(5) { animation-delay: 280ms; }
.metric-grid > .metric-card:nth-child(6),
.flow-strip  > .flow-node:nth-child(6) { animation-delay: 340ms; }
.metric-grid > .metric-card:nth-child(7),
.flow-strip  > .flow-node:nth-child(7) { animation-delay: 400ms; }
.metric-grid > .metric-card:nth-child(8),
.flow-strip  > .flow-node:nth-child(8) { animation-delay: 460ms; }

/* ─────────────────────────────────────────────
   HERO & SIMULATOR INTRO  — content cascade
───────────────────────────────────────────── */
.site-hero > *,
.simulator-intro > * {
  opacity: 0;
  transform: translateY(14px) translateZ(0);
  animation: swdm-fade-up 600ms var(--mo-ease-out) forwards;
}
.site-hero > *:nth-child(1), .simulator-intro > *:nth-child(1) { animation-delay:  80ms; }
.site-hero > *:nth-child(2), .simulator-intro > *:nth-child(2) { animation-delay: 180ms; }
.site-hero > *:nth-child(3), .simulator-intro > *:nth-child(3) { animation-delay: 280ms; }
.site-hero > *:nth-child(4), .simulator-intro > *:nth-child(4) { animation-delay: 380ms; }

/* Floating hero visual */
@keyframes swdm-float {
  0%,100% { transform: translateY(0)   translateZ(0); }
  50%     { transform: translateY(-7px) translateZ(0); }
}
.hero-orbit, .publisher-art {
  animation: swdm-float 8s ease-in-out infinite;
}

/* ─────────────────────────────────────────────
   CHARTS — fade + gentle scale entrance
───────────────────────────────────────────── */
[data-testid="stPlotlyChart"],
[data-testid="stVegaLiteChart"],
.stPlotlyChart, .swdm-chart {
  opacity: 0;
  animation: swdm-chart-in 640ms var(--mo-ease-out) forwards;
  animation-delay: 80ms;
}

@keyframes swdm-chart-in {
  from { opacity: 0; transform: translateY(8px) scale(.996) translateZ(0); }
  to   { opacity: 1; transform: translateY(0)   scale(1)    translateZ(0); }
}

/* SVG line draw-in */
.swdm-chart svg path[stroke],
svg .trace path[stroke] {
  stroke-dasharray: 1200;
  stroke-dashoffset: 1200;
  animation: swdm-draw 1200ms var(--mo-ease-out) forwards;
}

@keyframes swdm-draw { to { stroke-dashoffset: 0; } }

/* ─────────────────────────────────────────────
   PAGE LOAD — Streamlit images
───────────────────────────────────────────── */
[data-testid="stImage"] img {
  animation: swdm-fade-in var(--mo-med) var(--mo-ease-out) both;
}

/* ─────────────────────────────────────────────
   RESULTS CONTAINER  — success reveal
───────────────────────────────────────────── */
.swdm-results { animation: swdm-fade-up var(--mo-slow) var(--mo-ease-out) both; }
.swdm-results > * { animation: swdm-fade-up var(--mo-slow) var(--mo-ease-out) both; }
.swdm-results > *:nth-child(2) { animation-delay: 120ms; }
.swdm-results > *:nth-child(3) { animation-delay: 220ms; }
.swdm-results > *:nth-child(4) { animation-delay: 320ms; }

/* Success / error feedback pulse */
@keyframes swdm-success-pulse {
  0%   { box-shadow: 0 0 0 0   rgba(123,215,176,.38); }
  60%  { box-shadow: 0 0 0 10px rgba(123,215,176,0); }
  100% { box-shadow: 0 0 0 0   rgba(123,215,176,0); }
}
.swdm-success {
  animation: swdm-success-pulse 700ms var(--mo-ease-out);
}

@keyframes swdm-error-pulse {
  0%   { box-shadow: 0 0 0 0   rgba(242,138,155,.38); }
  60%  { box-shadow: 0 0 0 10px rgba(242,138,155,0); }
  100% { box-shadow: 0 0 0 0   rgba(242,138,155,0); }
}
.swdm-error {
  animation: swdm-error-pulse 700ms var(--mo-ease-out);
}

/* ─────────────────────────────────────────────
   SKELETON SHIMMER
───────────────────────────────────────────── */
.swdm-skeleton {
  position: relative;
  overflow: hidden;
  background: rgba(125,220,255,.06);
  border-radius: 10px;
}
.swdm-skeleton::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent          0%,
    rgba(255,255,255,.07) 50%,
    transparent          100%
  );
  transform: translateX(-100%);
  animation: swdm-shimmer 1.5s var(--mo-ease) infinite;
}
@keyframes swdm-shimmer { to { transform: translateX(100%); } }

/* Streamlit spinner: smooth entrance */
[data-testid="stSpinner"] {
  animation: swdm-fade-up var(--mo-med) var(--mo-ease-out) both;
}

/* ─────────────────────────────────────────────
   AMBIENT BACKGROUND ORBS  (subtle, fixed)
───────────────────────────────────────────── */
#swdm-orb-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}
.swdm-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  animation: swdm-orb-drift 18s ease-in-out infinite alternate;
}
.swdm-orb-1 {
  width: 480px; height: 480px;
  top: -120px; left: -80px;
  background: radial-gradient(circle, rgba(125,220,255,.055), transparent 72%);
  animation-duration: 22s;
  animation-delay: 0s;
}
.swdm-orb-2 {
  width: 380px; height: 380px;
  top: 30%; right: -60px;
  background: radial-gradient(circle, rgba(110,168,255,.045), transparent 72%);
  animation-duration: 18s;
  animation-delay: -6s;
}
.swdm-orb-3 {
  width: 300px; height: 300px;
  bottom: -80px; left: 35%;
  background: radial-gradient(circle, rgba(123,215,176,.032), transparent 72%);
  animation-duration: 26s;
  animation-delay: -12s;
}
@keyframes swdm-orb-drift {
  0%   { transform: translate(0,  0)   scale(1)     translateZ(0); }
  33%  { transform: translate(28px, -22px) scale(1.06) translateZ(0); }
  66%  { transform: translate(-18px, 16px) scale(.95)  translateZ(0); }
  100% { transform: translate(12px, 8px)  scale(1.02) translateZ(0); }
}

/* ─────────────────────────────────────────────
   SCROLL PROGRESS INDICATOR
───────────────────────────────────────────── */
#swdm-scroll-progress {
  position: fixed;
  top: 0; left: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent, #7ddcff), var(--accent-2, #6ea8ff));
  width: 0%;
  z-index: 99999;
  transform-origin: left;
  transition: width 60ms linear;
  pointer-events: none;
  box-shadow: 0 0 8px rgba(125,220,255,.4);
}

/* ─────────────────────────────────────────────
   STMETRIC VALUE  — tabular nums for count-up
───────────────────────────────────────────── */
[data-testid="stMetricValue"], [data-countup] {
  font-variant-numeric: tabular-nums;
}

/* ─────────────────────────────────────────────
   STATUS CHIPS  — subtle entrance
───────────────────────────────────────────── */
.status-chip-row .status-chip {
  opacity: 0;
  animation: swdm-fade-up 420ms var(--mo-ease-out) forwards;
}
.status-chip-row .status-chip:nth-child(1) { animation-delay:  20ms; }
.status-chip-row .status-chip:nth-child(2) { animation-delay:  70ms; }
.status-chip-row .status-chip:nth-child(3) { animation-delay: 120ms; }
.status-chip-row .status-chip:nth-child(4) { animation-delay: 170ms; }
.status-chip-row .status-chip:nth-child(5) { animation-delay: 220ms; }
.status-chip-row .status-chip:nth-child(6) { animation-delay: 270ms; }

/* ─────────────────────────────────────────────
   SECTION / WORKSTATION PANEL entrance
───────────────────────────────────────────── */
.section-heading,
.workstation-panel,
.simulator-intro {
  opacity: 0;
  transform: translateY(14px) translateZ(0);
  animation: swdm-fade-up var(--mo-slow) var(--mo-ease-out) forwards;
  animation-delay: 60ms;
}

/* ─────────────────────────────────────────────
   BLOCK TAGS — scale entrance on hover
───────────────────────────────────────────── */
.block-tag {
  transition: transform var(--mo-fast) var(--mo-ease),
              box-shadow var(--mo-fast) var(--mo-ease) !important;
}
.block-tag:hover {
  transform: scale(1.06) translateZ(0);
}

/* ─────────────────────────────────────────────
   REDUCED MOTION  — full override
───────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration:       .001ms !important;
    animation-iteration-count: 1     !important;
    transition-duration:       .001ms !important;
  }
  .hero-orbit, .publisher-art { animation: none !important; }
  #swdm-orb-layer              { display: none !important; }
  #swdm-scroll-progress        { display: none !important; }
}
</style>
"""


_MOTION_JS = r"""
<script id="swdm-motion-js">
(function() {
  try {
    var doc  = (window.parent && window.parent.document) ? window.parent.document : document;
    var win  = (window.parent && window.parent.document) ? window.parent  : window;

    if (doc.__swdmMotionInit) return;
    doc.__swdmMotionInit = true;

    var prefersReduced = win.matchMedia &&
      win.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ─── Ambient orb layer ─── */
    if (!prefersReduced && !doc.getElementById('swdm-orb-layer')) {
      var orbLayer = doc.createElement('div');
      orbLayer.id = 'swdm-orb-layer';
      orbLayer.innerHTML =
        '<div class="swdm-orb swdm-orb-1"></div>' +
        '<div class="swdm-orb swdm-orb-2"></div>' +
        '<div class="swdm-orb swdm-orb-3"></div>';
      doc.body.appendChild(orbLayer);
    }

    /* ─── Scroll progress bar ─── */
    var progressBar = null;
    if (!prefersReduced) {
      progressBar = doc.createElement('div');
      progressBar.id = 'swdm-scroll-progress';
      doc.body.appendChild(progressBar);
    }

    /* ─── Scroll event: navbar state + progress bar ─── */
    var html = doc.documentElement;
    var scrollTarget = doc.querySelector('.st-key-dashboard_shell') ||
                       doc.scrollingElement || html;

    var ticking = false;
    var onScroll = function() {
      if (ticking) return;
      ticking = true;
      win.requestAnimationFrame(function() {
        var st = scrollTarget.scrollTop || 0;
        /* Navbar blur */
        if (st > 8) html.classList.add('scrolled');
        else         html.classList.remove('scrolled');

        /* Progress bar */
        if (progressBar) {
          var total = scrollTarget.scrollHeight - scrollTarget.clientHeight;
          var pct   = total > 0 ? (st / total * 100) : 0;
          progressBar.style.width = Math.min(100, pct) + '%';
        }
        ticking = false;
      });
    };

    scrollTarget.addEventListener('scroll', onScroll, { passive: true });
    doc.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ─── IntersectionObserver (scroll reveal + count-up) ─── */
    if (prefersReduced || !('IntersectionObserver' in win)) return;

    /* Scroll reveal */
    var revealIo = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          revealIo.unobserve(e.target);
        }
      });
    }, { threshold: 0.10, rootMargin: '0px 0px -36px 0px' });

    var REVEAL_SELECTORS = [
      '.section-heading', '.workstation-panel', '.panel-card',
      '.simulator-intro', '.site-hero', '.publisher-section',
      '.soft-card', '.block-card', '.theory-intro',
      '[data-testid="stExpander"]',
      '[data-testid="stDataFrame"]',
      '[data-testid="stTable"]'
    ].join(',');

    var scan = function() {
      doc.querySelectorAll(REVEAL_SELECTORS).forEach(function(el) {
        if (!el.classList.contains('swdm-reveal')) {
          el.classList.add('swdm-reveal');
          revealIo.observe(el);
        }
      });
    };
    scan();

    /* Count-up for metric values */
    var easeOut = function(t) { return 1 - Math.pow(1 - t, 3); };

    var animateCount = function(el, to, duration) {
      var isInt    = Number.isInteger(to);
      var decimals = isInt ? 0 : Math.min(3, ((to.toString().split('.')[1] || '').length));
      var start    = win.performance ? win.performance.now() : Date.now();
      var step = function(now) {
        var elapsed = (win.performance ? win.performance.now() : Date.now()) - start;
        var p   = Math.min(1, elapsed / duration);
        var val = to * easeOut(p);
        el.textContent = isInt
          ? Math.round(val).toLocaleString()
          : val.toFixed(decimals);
        if (p < 1) win.requestAnimationFrame(step);
        else el.textContent = el.dataset.swdmFinal;
      };
      win.requestAnimationFrame(step);
    };

    var countIo = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (!e.isIntersecting) return;
        var el  = e.target;
        if (el.dataset.swdmCounted) return;
        var raw = (el.textContent || '').trim();
        var m   = raw.match(/^(-?\d+(?:\.\d+)?)/);
        if (!m) { countIo.unobserve(el); return; }
        var num = parseFloat(m[1]);
        if (!isFinite(num) || Math.abs(num) > 1e9) { countIo.unobserve(el); return; }
        el.dataset.swdmFinal   = raw;
        el.dataset.swdmCounted = '1';
        animateCount(el, num, 1100);
        countIo.unobserve(el);
      });
    }, { threshold: 0.4 });

    var scanCounts = function() {
      doc.querySelectorAll('[data-testid="stMetricValue"], [data-countup]')
        .forEach(function(el) {
          if (!el.dataset.swdmCounted) countIo.observe(el);
        });
    };
    scanCounts();

    /* Very subtle mouse-parallax on hero visual (desktop only, tiny delta) */
    if (win.innerWidth > 860) {
      var heroOrbit = null;
      var onMouseMove = function(e) {
        if (!heroOrbit) heroOrbit = doc.querySelector('.hero-orbit, .publisher-art');
        if (!heroOrbit) return;
        var cx = win.innerWidth  / 2;
        var cy = win.innerHeight / 2;
        var dx = (e.clientX - cx) / cx;  /* -1 → +1 */
        var dy = (e.clientY - cy) / cy;
        heroOrbit.style.transform =
          'translate(' + (dx * 5).toFixed(1) + 'px, ' + (dy * 4).toFixed(1) + 'px) translateZ(0)';
      };
      doc.addEventListener('mousemove', onMouseMove, { passive: true });
    }

    /* Re-scan after Streamlit re-renders */
    var mo = new MutationObserver(function() { scan(); scanCounts(); });
    mo.observe(doc.body, { childList: true, subtree: true });

  } catch (err) {
    /* Fail silently — never break the app */
    if (console && console.debug) console.debug('swdm-motion init skipped', err);
  }
})();
</script>
"""


def inject_motion() -> None:
    """Inject premium motion CSS + JS. Idempotent at the DOM level."""
    st.markdown(_MOTION_CSS, unsafe_allow_html=True)
    st.markdown(_MOTION_JS,  unsafe_allow_html=True)
