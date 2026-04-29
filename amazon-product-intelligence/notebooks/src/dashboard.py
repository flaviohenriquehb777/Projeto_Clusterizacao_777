"""Standalone offline dashboard renderer."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any


def render_dashboard_html(dashboard_data: dict[str, Any]) -> str:
    """Render a standalone HTML dashboard with embedded data."""
    data_json = json.dumps(dashboard_data, ensure_ascii=False)
    data_b64 = base64.b64encode(data_json.encode("utf-8")).decode("ascii")
    favicon_href = dashboard_data.get("_meta", {}).get("favicon_href", "../reports/figures/favicon.ico")

    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Amazon Product Intelligence Dashboard</title>
  <link rel="icon" href="__FAVICON_HREF__" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  <link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/jquery.dataTables.min.css">
  <script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>
  <style>
    :root {{
      --bg: #0a0e1a;
      --card: #111827;
      --muted: #94a3b8;
      --text: #e5e7eb;
      --accent: #6366f1;
      --good: #22c55e;
      --warn: #f59e0b;
      --bad: #ef4444;
      --shadow: 0 12px 40px rgba(0,0,0,.45);
      --sidebar-width: 280px;
      --page-pad: 16px;
      --gap: 14px;
      --radius: 16px;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; overflow: hidden; }}
    body {{
      margin: 0;
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      background:
        radial-gradient(1200px 700px at 30% -10%, rgba(99,102,241,.25), transparent 60%),
        radial-gradient(900px 600px at 110% 10%, rgba(34,197,94,.18), transparent 60%),
        var(--bg);
      color: var(--text);
      overflow: hidden;
    }}
    a {{ color: #a5b4fc; text-decoration: none; }}
    .app {{
      display: grid;
      grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
      height: 100vh;
      overflow: hidden;
    }}
    .sidebar {{
      position: sticky;
      top: 0;
      height: 100vh;
      padding: 22px 18px;
      overflow: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
      background: linear-gradient(180deg, rgba(17,24,39,.92), rgba(10,14,26,.92));
      border-right: 1px solid rgba(148,163,184,.12);
    }}
    .brand {{ font-weight: 800; letter-spacing: -0.02em; font-size: 18px; margin: 0; }}
    .nav {{ display: flex; flex-direction: column; gap: 8px; }}
    .nav button {{
      display: flex; align-items: center; gap: 10px;
      background: transparent; color: var(--text);
      border: 1px solid rgba(148,163,184,.12);
      padding: 10px 12px; border-radius: 12px;
      cursor: pointer; text-align: left;
      transition: transform .15s ease, background .15s ease, border-color .15s ease;
    }}
    .nav button:hover {{ transform: translateY(-1px); border-color: rgba(99,102,241,.45); background: rgba(99,102,241,.08); }}
    .nav button.active {{ border-color: rgba(99,102,241,.85); background: rgba(99,102,241,.12); box-shadow: inset 0 0 0 1px rgba(99,102,241,.25); }}
    .icon {{ width: 22px; height: 22px; display: grid; place-items: center; border-radius: 8px; background: rgba(99,102,241,.18); flex: 0 0 auto; }}
    .main {{
      min-width: 0;
      min-height: 0;
      padding: var(--page-pad);
      display: flex;
      flex-direction: column;
      gap: var(--gap);
      height: 100vh;
      overflow: hidden;
    }}
    .topbar {{ display: flex; flex-direction: column; gap: 12px; flex: 0 0 auto; }}
    .ticker {{
      overflow: hidden;
      border-radius: 14px;
      border: 1px solid rgba(148,163,184,.12);
      background: rgba(17,24,39,.65);
      box-shadow: var(--shadow);
      min-height: 42px;
    }}
    .ticker-track {{ display: inline-block; white-space: nowrap; padding: 10px 0; animation: marquee 22s linear infinite; }}
    .ticker-item {{ display: inline-block; padding: 0 26px; color: var(--muted); }}
    @keyframes marquee {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
    .toolbar {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      align-items: end;
    }}
    .selection-chips {{
      display: flex;
      flex-wrap: nowrap;
      gap: 8px;
      align-items: center;
      min-height: 42px;
      max-width: 100%;
      overflow-x: auto;
      overflow-y: hidden;
      white-space: nowrap;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: thin;
      min-width: 0;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid rgba(148,163,184,.16);
      background: rgba(17,24,39,.55);
      color: var(--text);
      font-size: 12px;
    }}
    .chip .x {{
      border: none;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font-size: 14px;
      line-height: 1;
      padding: 0;
    }}
    .chip .x:hover {{ color: #e5e7eb; }}
    .filter-block {{ width: min(320px, 100%); }}
    .filter-label {{ font-size: 12px; margin-bottom: 6px; color: var(--muted); }}
    select {{
      width: 100%;
      border-radius: 12px;
      padding: 10px 12px;
      background: rgba(17,24,39,.65);
      color: var(--text);
      border: 1px solid rgba(148,163,184,.12);
      outline: none;
    }}
    #filterSlotTop, #filterSlotOverview, #filterSlotSegments {{ display: flex; justify-content: flex-end; }}
    .grid {{ display: grid; gap: var(--gap); min-height: 0; }}
    .kpis {{ grid-template-columns: repeat(6, minmax(0, 1fr)); }}
    .card {{
      background: rgba(17,24,39,.75);
      border: 1px solid rgba(148,163,184,.12);
      border-radius: var(--radius);
      padding: 12px;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
      gap: 8px;
      min-height: 0;
      overflow: hidden;
    }}
    .card > div[id^="chart"],
    .card > div[style*="height"],
    .card > .datatable-wrap,
    .card > #clusterCards,
    .card > #clusterOpportunity,
    .card > #qaAccordion,
    .card > #wordCloud {{
      flex: 1 1 auto;
      min-height: 0;
    }}
    .js-plotly-plot, .plot-container, .svg-container {{
      width: 100% !important;
      height: 100% !important;
      min-height: 0 !important;
      overflow: hidden !important;
    }}
    .kpi-title {{ color: var(--muted); font-size: 12px; }}
    .kpi-value {{ font-size: 22px; font-weight: 800; margin-top: 6px; letter-spacing: -0.02em; }}
    .fade {{ animation: fade .25s ease; }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .section {{
      display: none;
      flex: 1 1 auto;
      min-height: 0;
      overflow: hidden;
    }}
    .section.active {{ display: grid; gap: var(--gap); }}
    #overview.active {{ grid-template-rows: auto minmax(0, 1fr) auto; }}
    #pricing.active {{ grid-template-rows: minmax(0, 1.02fr) minmax(0, .98fr) auto; }}
    #ratings.active {{ grid-template-rows: minmax(0, 1fr) minmax(0, .92fr); }}
    #psi.active {{ grid-template-rows: minmax(0, 1.08fr) minmax(0, .92fr); }}
    #segments.active {{ grid-template-rows: minmax(0, 1fr) auto minmax(0, .9fr); }}
    #sentiment.active {{ grid-template-rows: minmax(0, 1fr) minmax(0, 1fr) minmax(140px, .56fr); }}
    #report.active, #catalog.active {{ grid-template-rows: minmax(0, 1fr); }}
    .row, .row3, .rowSegments {{ display: grid; gap: var(--gap); align-items: stretch; min-height: 0; }}
    .row {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .row3, .rowSegments {{ grid-template-columns: minmax(0, 1.18fr) minmax(320px, .82fr); }}
    .row > .card, .row3 > .card, .rowSegments > .card, .kpis > .card {{ min-height: 0; height: 100%; }}
    #overview .kpis .card {{ min-height: 88px; justify-content: center; }}
    .title {{ font-size: 16px; font-weight: 800; margin: 0; line-height: 1.2; }}
    .muted {{ color: var(--muted); font-size: 12px; line-height: 1.45; }}
    .datatable-wrap, #clusterCards, #clusterOpportunity, #qaAccordion, #wordCloud {{ overflow: auto; padding-right: 4px; }}
    #clusterOpportunity {{ white-space: normal; line-height: 1.6; }}
    .datatable-wrap table {{ width: 100%; }}
    .dataTables_wrapper {{ display: flex; flex-direction: column; min-height: 0; height: 100%; gap: 8px; }}
    .dt-toolbar {{ display: flex; justify-content: flex-end; }}
    .dt-toolbar .dataTables_filter {{ margin-left: auto; }}
    .dataTables_wrapper .dataTables_filter label {{ color: var(--muted); font-size: 12px; }}
    .dataTables_wrapper .dataTables_filter input {{
      margin-left: 8px;
      border-radius: 10px;
      border: 1px solid rgba(148,163,184,.14);
      background: rgba(10,14,26,.55);
      color: var(--text);
      padding: 7px 10px;
    }}
    .dataTables_scroll {{ display: flex; flex-direction: column; min-height: 0; flex: 1 1 auto; }}
    .dataTables_scrollHead, .dataTables_scrollBody {{ width: 100% !important; }}
    .dataTables_scrollBody {{ flex: 1 1 auto; min-height: 0; }}
    table.dataTable {{ background: rgba(17,24,39,.75); color: var(--text); border-radius: 14px; overflow: hidden; border-collapse: separate; border-spacing: 0; }}
    table.dataTable thead th {{ background: rgba(99,102,241,.10); color: var(--text); border-bottom: 1px solid rgba(148,163,184,.10); font-weight: 600; font-size: 12px; letter-spacing: 0.02em; padding: 10px 12px; }}
    table.dataTable tbody td {{ border-bottom: 1px solid rgba(148,163,184,.06); font-weight: 400; font-size: 12px; padding: 9px 12px; transition: background .15s ease; letter-spacing: 0.01em; vertical-align: top; }}
    table.dataTable tbody tr:hover td {{ background: rgba(99,102,241,.06); }}
    table.dataTable tbody tr:last-child td {{ border-bottom: none; }}
    .dt-footer {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }}
    .dataTables_wrapper .dataTables_paginate .paginate_button {{ color: var(--muted) !important; }}
    .dataTables_wrapper .dataTables_paginate .paginate_button.current {{ background: rgba(99,102,241,.18) !important; border-color: rgba(99,102,241,.3) !important; color: #e5e7eb !important; }}
    .dataTables_wrapper .dataTables_info {{ color: var(--muted); font-size: 12px; }}
    .pill {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 12px;
      border: 1px solid rgba(148,163,184,.18);
      color: var(--muted);
    }}
    .btn {{
      border-radius: 12px;
      border: 1px solid rgba(148,163,184,.12);
      background: rgba(99,102,241,.16);
      color: var(--text);
      padding: 10px 12px;
      cursor: pointer;
      transition: all .15s ease;
      white-space: nowrap;
    }}
    .btn:hover {{ background: rgba(99,102,241,.28); transform: translateY(-1px); }}
    .accordion {{ display: flex; flex-direction: column; gap: 10px; min-height: 0; }}
    .accordion details {{
      border: 1px solid rgba(148,163,184,.12);
      background: rgba(17,24,39,.65);
      border-radius: 14px;
      padding: 10px 12px;
      margin: 0;
    }}
    .accordion summary {{ cursor: pointer; font-weight: 700; }}
    .wordcloud {{ display: flex; flex-wrap: wrap; gap: 8px; align-content: flex-start; }}
    .word {{
      font-size: 13px;
      line-height: 1;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(148,163,184,.12);
      background: rgba(99,102,241,.08);
      display: inline-flex;
      align-items: center;
      white-space: nowrap;
    }}
    .img-placeholder {{ width:44px;height:44px;border-radius:10px;background:rgba(99,102,241,.12);display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:18px; }}
    #segments #clusterCards .card {{ margin-bottom: 10px; cursor: pointer; }}
    #report .card, #catalog .card {{ height: 100%; }}
    @media (max-width: 1440px) {{
      .kpis {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .row3, .rowSegments {{ grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }}
    }}
    @media (max-width: 1180px) {{
      html, body {{ overflow: auto; }}
      body {{ overflow: auto; }}
      .app {{ grid-template-columns: 1fr; height: auto; min-height: 100vh; }}
      .sidebar {{ height: auto; position: relative; }}
      .main {{ height: auto; min-height: auto; overflow: visible; }}
      .section, .section.active {{ overflow: visible; }}
      .toolbar {{ grid-template-columns: 1fr; }}
      .kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .row, .row3, .rowSegments {{ grid-template-columns: 1fr; }}
      #overview.active, #pricing.active, #ratings.active, #psi.active, #segments.active, #sentiment.active, #report.active, #catalog.active {{ grid-template-rows: none; }}
      .filter-block {{ width: 100%; max-width: none; }}
    }}
  </style>
</head>
<body>
  <script id="dashboardData" type="text/plain">__DASHBOARD_DATA_B64__</script>
  <div class="app">
    <aside class="sidebar">
      <div class="brand">Amazon Product Intelligence</div>
      <div class="nav">
        <button class="active" data-tab="overview"><span class="icon">🏠</span> Overview</button>
        <button data-tab="pricing"><span class="icon">💰</span> Pricing & Discounts</button>
        <button data-tab="ratings"><span class="icon">⭐</span> Ratings & Reviews</button>
        <button data-tab="psi"><span class="icon">🏆</span> Product Score Index</button>
        <button data-tab="segments"><span class="icon">🧩</span> Segmentação</button>
        <button data-tab="sentiment"><span class="icon">💬</span> Sentimento</button>
        <button data-tab="report"><span class="icon">📋</span> Business Report</button>
        <button data-tab="catalog"><span class="icon">📦</span> Catálogo</button>
      </div>
    </aside>

    <main class="main">
      <div class="topbar">
        <div class="ticker">
          <div class="ticker-track" id="tickerTrack"></div>
        </div>
        <div class="toolbar">
          <div class="selection-chips" id="selectionChips"></div>
          <div id="filterSlotTop">
            <div class="filter-block" id="filterBlock">
              <div class="filter-label">Global filter — Main Category</div>
              <select id="categoryFilter"></select>
            </div>
          </div>
        </div>
      </div>

      <section id="overview" class="section active fade">
        <div class="grid kpis" id="kpiGrid"></div>
        <div class="row" style="margin-top:14px">
          <div class="card">
            <div class="title">Products by Category</div>
            <div id="chartCategoryBar" style="height:380px"></div>
          </div>
          <div class="card">
            <div class="title">Data Quality Gauge</div>
            <div id="chartQualityGauge" style="height:380px"></div>
          </div>
        </div>
        <div id="filterSlotOverview" style="margin-top:14px;display:flex;justify-content:flex-end;"></div>
      </section>

      <section id="pricing" class="section fade">
        <div class="row">
          <div class="card">
            <div class="title">Price by Category (Box)</div>
            <div id="chartPriceBox" style="height:420px"></div>
          </div>
          <div class="card">
            <div class="title">Price vs Discount</div>
            <div id="chartPriceDiscount" style="height:420px"></div>
          </div>
        </div>
        <div class="row" style="margin-top:14px">
          <div class="card">
            <div class="title">Discount Distribution</div>
            <div id="chartDiscountHist" style="height:380px"></div>
          </div>
          <div class="card">
            <div class="title">Discount × Category (Heatmap)</div>
            <div id="chartDiscountHeatmap" style="height:380px"></div>
          </div>
        </div>
        <div class="card" style="margin-top:14px">
          <div class="title">Most Aggressive Category</div>
          <div class="muted" id="aggressiveCategory"></div>
          <div style="margin-top:10px"><span class="pill" id="aggressiveValue"></span></div>
        </div>
      </section>

      <section id="ratings" class="section fade">
        <div class="row">
          <div class="card">
            <div class="title">Rating vs Review Volume</div>
            <div id="chartRatingReviews" style="height:420px"></div>
          </div>
          <div class="card">
            <div class="title">Opportunity Quadrants</div>
            <div class="muted">High rating × high reviews are leaders; high rating × low reviews are hidden gems.</div>
            <div id="chartQuadrants" style="height:390px;margin-top:10px"></div>
          </div>
        </div>
        <div class="row" style="margin-top:14px">
          <div class="card">
            <div class="title">Ratings Distribution</div>
            <div id="chartRatingDist" style="height:360px"></div>
          </div>
          <div class="card">
            <div class="title">Top Leaders — Rating × Volume</div>
            <div class="muted">Clique em uma barra para filtrar por categoria.</div>
            <div id="chartLeaders" style="height:360px;margin-top:10px"></div>
          </div>
        </div>
      </section>

      <section id="psi" class="section fade">
        <div class="row">
          <div class="card">
            <div class="title">Top 20 PSI Leaderboard</div>
            <div id="chartPsiLeaderboard" style="height:520px"></div>
          </div>
          <div class="card">
            <div class="title">PSI vs Price (by Cluster)</div>
            <div id="chartPsiVsPrice" style="height:520px"></div>
          </div>
        </div>
        <div class="row" style="margin-top:14px">
          <div class="card">
            <div class="title">Average PSI by Category</div>
            <div id="chartPsiByCategory" style="height:420px"></div>
          </div>
          <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
              <div class="title">PSI Table</div>
              <button class="btn" id="exportPsiBtn">Export CSV</button>
            </div>
            <div class="datatable-wrap" style="margin-top:10px">
              <table id="psiTable" class="display"></table>
            </div>
          </div>
        </div>
      </section>

      <section id="segments" class="section fade">
        <div class="rowSegments">
          <div class="card">
            <div class="title">Clusters (PCA 2D)</div>
            <div id="chartPca" style="height:520px"></div>
          </div>
          <div class="card">
            <div class="title">Cluster Profiles</div>
            <div id="clusterCards"></div>
          </div>
        </div>
        <div id="filterSlotSegments" style="margin-top:14px;display:flex;justify-content:flex-end;"></div>
        <div class="rowSegments" style="margin-top:14px">
          <div class="card">
            <div class="title">Treemap — Cluster × Category</div>
            <div id="chartTreemap" style="height:460px"></div>
          </div>
          <div class="card">
            <div class="title">Opportunity Notes</div>
            <div class="muted" id="clusterOpportunity"></div>
          </div>
        </div>
      </section>

      <section id="sentiment" class="section fade">
        <div class="row">
          <div class="card">
            <div class="title">Overall Sentiment Gauge</div>
            <div id="chartSentimentGauge" style="height:420px"></div>
          </div>
          <div class="card">
            <div class="title">Sentiment by Category</div>
            <div id="chartSentimentByCategory" style="height:420px"></div>
          </div>
        </div>
        <div class="row" style="margin-top:14px">
          <div class="card">
            <div class="title">Sentiment vs Rating</div>
            <div id="chartSentimentVsRating" style="height:420px"></div>
          </div>
          <div class="card">
            <div class="title">Top Reviews</div>
            <div class="datatable-wrap" style="margin-top:10px">
              <table id="reviewsTable" class="display"></table>
            </div>
          </div>
        </div>
        <div class="card" style="margin-top:14px">
          <div class="title">WordCloud (CSS simulation)</div>
          <div class="muted">Top words are derived from filtered review text and scaled visually.</div>
          <div id="wordCloud" class="wordcloud" style="margin-top:10px"></div>
        </div>
      </section>

      <section id="report" class="section fade">
        <div class="card">
          <div class="title">Business Questions (20)</div>
          <div class="accordion" id="qaAccordion"></div>
        </div>
      </section>

      <section id="catalog" class="section fade">
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
            <div class="title">Product Catalog</div>
            <button class="btn" id="exportCatalogBtn">Export CSV</button>
          </div>
          <div class="datatable-wrap" style="margin-top:10px">
            <table id="catalogTable" class="display"></table>
          </div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const b64 = document.getElementById('dashboardData').textContent.trim();
    const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    const DATA = JSON.parse(new TextDecoder('utf-8').decode(bytes));
    const products = DATA.products || [];
    const reviews = DATA.reviews || [];
    const qa = DATA.qa || [];

    const fmt = (x, d=2) => {
      if (x === null || x === undefined || Number.isNaN(Number(x))) return 'n/a';
      const n = Number(x);
      return n.toLocaleString(undefined, { maximumFractionDigits: d });
    };

    function unique(arr) { return Array.from(new Set(arr)); }

    /* ── Global product name truncation ── */
    function truncateName(name, maxLen) {
      maxLen = maxLen || 45;
      if (!name) return '';
      return name.length > maxLen ? name.substring(0, maxLen) + '…' : name;
    }
    function truncName(name, max) { return truncateName(name, max); }

    /* ── Selection state (Power BI-like) ── */
    const selection = {
      clusters: new Set(),     // multi
      sentiments: new Set()    // multi: positivo/neutro/negativo
    };

    const PLOT_CONFIG = { displayModeBar:false, responsive:true };
    const TABLE_SCROLL_MIN = 220;

    function getActiveTab() {
      return document.querySelector('.section.active')?.id || 'overview';
    }

    function getTableScrollY(tableId, offset=16) {
      const table = document.getElementById(tableId);
      const wrap = table ? table.closest('.datatable-wrap') : null;
      if (!wrap) return TABLE_SCROLL_MIN + 'px';
      const h = Math.max(TABLE_SCROLL_MIN, Math.floor(wrap.getBoundingClientRect().height - offset));
      return `${h}px`;
    }

    function afterLayout(fn) {
      requestAnimationFrame(() => requestAnimationFrame(fn));
    }

    function resizeVisiblePlots() {
      const section = document.querySelector('.section.active');
      if (!section || typeof Plotly === 'undefined') return;
      section.querySelectorAll('.js-plotly-plot').forEach(node => {
        try { Plotly.Plots.resize(node); } catch (err) {}
      });
    }

    function adjustVisibleTables() {
      const tab = getActiveTab();
      if (tab === 'psi' && psiTable) psiTable.columns.adjust();
      if (tab === 'sentiment' && reviewsTable) reviewsTable.columns.adjust();
      if (tab === 'catalog' && catalogTable) catalogTable.columns.adjust();
    }

    function scheduleActiveLayoutRefresh() {
      afterLayout(() => {
        resizeVisiblePlots();
        adjustVisibleTables();
      });
    }

    function tableBaseOptions(tableId, overrides) {
      return Object.assign({
        destroy: true,
        autoWidth: false,
        deferRender: true,
        scrollX: true,
        scrollY: getTableScrollY(tableId),
        scrollCollapse: true,
        paging: true,
        lengthChange: false,
        pageLength: 8,
        dom: 't<"dt-footer"ip>'
      }, overrides || {});
    }

    window.addEventListener('resize', (() => {
      let timer = null;
      return () => {
        clearTimeout(timer);
        timer = setTimeout(scheduleActiveLayoutRefresh, 120);
      };
    })());

    /* ── Image fallback placeholder (SVG data URI) ── */
    var IMG_PLACEHOLDER = "data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2244%22 height=%2244%22 viewBox=%220 0 44 44%22%3E%3Crect width=%2244%22 height=%2244%22 rx=%2210%22 fill=%22%23111827%22/%3E%3Ctext x=%2222%22 y=%2226%22 text-anchor=%22middle%22 fill=%22%2394a3b8%22 font-size=%2218%22%3E%F0%9F%93%A6%3C/text%3E%3C/svg%3E";

    function toggleSet(s, v) {
      if (v === null || v === undefined) return;
      const key = String(v);
      if (s.has(key)) s.delete(key);
      else s.add(key);
    }

    function getFilterCategory() {
      const v = document.getElementById('categoryFilter').value;
      return v === '__ALL__' ? null : v;
    }

    function setFilterCategory(cat) {
      const sel = document.getElementById('categoryFilter');
      sel.value = (cat === null || cat === undefined) ? '__ALL__' : cat;
    }

    function toggleCategory(cat) {
      if (!cat) return;
      const cur = getFilterCategory();
      if (cur === cat) setFilterCategory(null);
      else setFilterCategory(cat);
      refreshAll();
    }

    function clearAllSelections() {
      selection.clusters.clear();
      selection.sentiments.clear();
      setFilterCategory(null);
      refreshAll();
    }

    function filteredProductsCategoryOnly() {
      const c = getFilterCategory();
      if (!c) return products;
      return products.filter(p => p.main_category === c);
    }

    function filteredProducts() {
      let arr = filteredProductsCategoryOnly();
      if (selection.clusters.size) {
        arr = arr.filter(p => selection.clusters.has(String(p.cluster)));
      }
      return arr;
    }

    function filteredReviewsCategoryOnly() {
      const c = getFilterCategory();
      if (!c) return reviews;
      return reviews.filter(r => r.main_category === c);
    }

    function filteredReviews() {
      let arr = filteredReviewsCategoryOnly();
      if (selection.sentiments.size) {
        arr = arr.filter(r => selection.sentiments.has(String(r.sentimento_label)));
      }
      return arr;
    }

    function placeFilterForTab(tab) {
      const block = document.getElementById('filterBlock');
      let slot = document.getElementById('filterSlotTop');
      if (tab === 'overview') slot = document.getElementById('filterSlotOverview') || slot;
      if (tab === 'segments') slot = document.getElementById('filterSlotSegments') || slot;
      if (block && slot && block.parentElement !== slot) slot.appendChild(block);
    }

    function renderSelectionChips() {
      const el = document.getElementById('selectionChips');
      if (!el) return;
      const chips = [];
      const c = getFilterCategory();
      if (c) chips.push({ label: `Category: ${c}`, clear: 'category' });
      if (selection.clusters.size) chips.push({ label: `Clusters: ${Array.from(selection.clusters).join(', ')}`, clear: 'clusters' });
      if (selection.sentiments.size) chips.push({ label: `Sentiment: ${Array.from(selection.sentiments).join(', ')}`, clear: 'sentiments' });
      if (!chips.length) {
        el.innerHTML = `<span class="pill">No active selections</span>`;
        return;
      }
      chips.push({ label: 'Clear selections', clear: 'all', isButton: true });
      el.innerHTML = chips.map(ch => {
        if (ch.isButton) return `<button class="btn" data-clear="all">Clear selections</button>`;
        return `<span class="chip">${ch.label}<button class="x" title="Clear" data-clear="${ch.clear}">×</button></span>`;
      }).join('');
    }

    document.getElementById('selectionChips').addEventListener('click', (e) => {
      const t = e.target;
      const action = t && t.getAttribute ? t.getAttribute('data-clear') : null;
      if (!action) return;
      if (action === 'all') return clearAllSelections();
      if (action === 'category') setFilterCategory(null);
      if (action === 'clusters') selection.clusters.clear();
      if (action === 'sentiments') selection.sentiments.clear();
      refreshAll();
    });

    function refreshAll() {
      renderSelectionChips();
      plotCategoryBar();
      plotPricing();
      plotRatings();
      plotPsi();
      plotSegments();
      plotSentiment();
      refreshCatalogTable();
      scheduleActiveLayoutRefresh();
    }

    function setTicker() {
      const k = DATA.kpis;
      const items = [
        `📦 ${fmt(k.total_products,0)} Products`,
        `⭐ Avg Rating: ${fmt(k.avg_rating,2)}`,
        `💰 Avg Discount: ${fmt(k.avg_discount,2)}%`,
        `🏆 Top Category: ${k.top_category}`,
        `💎 Best PSI: ${k.best_psi_product}`,
        `🔴 Max Discount: ${fmt(k.max_discount,2)}%`,
        `📊 ${fmt(k.total_categories,0)} Categories`,
        `🧩 ${fmt(k.n_clusters,0)} Clusters Identified`
      ];
      const doubled = items.concat(items);
      document.getElementById('tickerTrack').innerHTML = doubled.map(t => `<span class="ticker-item">${t}</span>`).join('');
    }

    function renderKpis() {
      const k = DATA.kpis;
      const cards = [
        { title: 'Total Products', value: k.total_products, tip: 'Unique products (product_id)' },
        { title: 'Avg Rating', value: k.avg_rating, tip: 'Mean of rating' },
        { title: 'Avg Discount %', value: k.avg_discount, tip: 'Mean of discount_percentage' },
        { title: 'Avg Savings (₹)', value: k.avg_savings, tip: 'Mean(actual - discounted)' },
        { title: 'Total Categories', value: k.total_categories, tip: 'Distinct main categories' },
        { title: 'Total Reviews', value: k.total_reviews, tip: 'Sum of rating_count' }
      ];
      const el = document.getElementById('kpiGrid');
      el.innerHTML = cards.map(c => `
        <div class="card" title="${c.tip}">
          <div class="kpi-title">${c.title}</div>
          <div class="kpi-value" data-kpi="${c.title}">0</div>
        </div>
      `).join('');

      const nodes = Array.from(el.querySelectorAll('.kpi-value'));
      nodes.forEach(n => {
        const t = n.getAttribute('data-kpi');
        const v = cards.find(x => x.title === t).value;
        const target = Number(v);
        const steps = 28;
        let i = 0;
        const tick = () => {
          i++;
          const cur = target * (i/steps);
          n.textContent = (t.includes('Rating') || t.includes('%')) ? fmt(cur,2) : fmt(cur,0);
          if (i < steps) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }

    function plotCategoryBar() {
      const cats = {};
      products.forEach(p => {
        const c = p.main_category || 'Unknown';
        cats[c] = (cats[c] || 0) + 1;
      });
      const entries = Object.entries(cats).sort((a,b) => b[1]-a[1]);
      const x = entries.map(e => e[0]);
      const y = entries.map(e => e[1]);
      const sel = getFilterCategory();
      const colors = x.map(c => !sel || c === sel ? 'rgba(99,102,241,.92)' : 'rgba(99,102,241,.45)');
      const opacity = x.map(c => !sel || c === sel ? 1 : 0.28);
      Plotly.newPlot('chartCategoryBar', [{
        type:'bar', x, y,
        marker:{ color: colors, opacity: opacity },
        text: y.map(v => fmt(v,0)),
        textposition: 'outside',
        cliponaxis: false,
        hovertemplate: '%{x}<br>Products=%{y}<extra></extra>'
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
        font:{color:'#e5e7eb'},
        margin:{l:40,r:10,t:10,b:90},
        uirevision: 'keep',
        clickmode: 'event+select'
      }, PLOT_CONFIG);
      const el = document.getElementById('chartCategoryBar');
      el.on('plotly_click', (ev) => {
        const cat = ev && ev.points && ev.points[0] ? ev.points[0].x : null;
        if (cat) toggleCategory(cat);
      });
      el.on('plotly_doubleclick', () => {
        setFilterCategory(null);
        refreshAll();
      });
    }

    function plotQualityGauge() {
      const critical = ['product_id','product_name','main_category','discounted_price_clean','actual_price_clean','discount_pct_clean','rating_clean','rating_count_clean'];
      const miss = (p) => critical.some(k => p[k] === null || p[k] === undefined);
      const missShare = products.length ? (products.filter(miss).length / products.length) : 0;
      const quality = Math.max(0, Math.min(100, (1 - missShare) * 100));
      Plotly.newPlot('chartQualityGauge', [{
        type: 'indicator', mode: 'gauge+number', value: quality,
        gauge: { axis: { range: [0, 100] }, bar: { color: '#6366f1' },
          steps: [
            { range: [0, 60], color: 'rgba(239,68,68,.25)' },
            { range: [60, 85], color: 'rgba(245,158,11,.20)' },
            { range: [85, 100], color: 'rgba(34,197,94,.20)' }
          ] }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'}, margin:{l:20,r:20,t:10,b:10}
      }, {displayModeBar:false});
    }

    function plotPricing() {
      const fp = filteredProducts();
      const byCat = {};
      fp.forEach(p => {
        const c = p.main_category || 'Unknown';
        if (!byCat[c]) byCat[c] = [];
        if (p.discounted_price_clean !== null) byCat[c].push(p.discounted_price_clean);
      });
      const traces = Object.entries(byCat).map(([c, vals]) => ({ type:'box', name:c, y: vals, boxpoints:'outliers' }));
      Plotly.newPlot('chartPriceBox', traces, {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:120}, yaxis:{title:'₹'},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      const priceBoxEl = document.getElementById('chartPriceBox');
      priceBoxEl.on('plotly_click', (ev) => {
        const cat = ev?.points?.[0]?.data?.name;
        if (cat) toggleCategory(cat);
      });
      priceBoxEl.on('plotly_doubleclick', () => {
        setFilterCategory(null);
        refreshAll();
      });

      const colors = fp.map(p => p.faixa_desconto || 'n/a');
      Plotly.newPlot('chartPriceDiscount', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.discounted_price_clean),
        y: fp.map(p=>p.discount_pct_clean),
        text: fp.map(p=>truncName(p.product_name)),
        marker:{ size: 9, color: colors, colorscale: 'Viridis' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'₹'}, yaxis:{title:'Discount %'},
        uirevision:'keep'
      }, PLOT_CONFIG);

      const disc = fp.map(p=>p.discount_pct_clean).filter(v=>v!==null);
      Plotly.newPlot('chartDiscountHist', [{type:'histogram', x: disc, marker:{color:'rgba(99,102,241,.85)'}}], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Discount %'}, yaxis:{title:'Count'},
        uirevision:'keep'
      }, PLOT_CONFIG);

      const discByCat = {};
      fp.forEach(p => {
        const c = p.main_category || 'Unknown';
        if (p.discount_pct_clean === null) return;
        if (!discByCat[c]) discByCat[c] = [];
        discByCat[c].push(p.discount_pct_clean);
      });
      const avg = Object.entries(discByCat).map(([c, arr]) => [c, arr.reduce((a,b)=>a+b,0)/arr.length]).sort((a,b)=>b[1]-a[1]);
      if (avg.length) {
        document.getElementById('aggressiveCategory').textContent = avg[0][0];
        document.getElementById('aggressiveValue').textContent = `Avg discount: ${fmt(avg[0][1],2)}%`;
      } else {
        document.getElementById('aggressiveCategory').textContent = 'n/a';
        document.getElementById('aggressiveValue').textContent = '';
      }

      const cats = Object.keys(discByCat).sort();
      const bands = ['low','medium','high'];
      const z = bands.map(b => cats.map(c => {
        const rows = fp.filter(p => (p.main_category||'Unknown')===c && (p.faixa_desconto||'')===b && p.rating_clean!==null);
        if (!rows.length) return null;
        const m = rows.reduce((a,r)=>a+Number(r.rating_clean),0)/rows.length;
        return m;
      }));
      Plotly.newPlot('chartDiscountHeatmap', [{
        type:'heatmap',
        x: cats,
        y: bands,
        z: z,
        colorscale: 'Viridis',
        hovertemplate: 'Category=%{x}<br>Band=%{y}<br>Avg rating=%{z:.2f}<extra></extra>'
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:70,r:10,t:10,b:120},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      document.getElementById('chartDiscountHeatmap').on('plotly_click', (ev) => {
        const cat = ev?.points?.[0]?.x;
        if (cat) toggleCategory(cat);
      });
    }

    function plotRatings() {
      const fp = filteredProducts();
      Plotly.newPlot('chartRatingReviews', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.rating_count_clean),
        y: fp.map(p=>p.rating_clean),
        text: fp.map(p=>truncName(p.product_name)),
        marker: { size: fp.map(p => Math.max(6, Math.min(30, (p.discounted_price_clean || 0)/500))), color: 'rgba(99,102,241,.85)' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Rating Count', type:'log'}, yaxis:{title:'Rating'},
        uirevision:'keep'
      }, PLOT_CONFIG);

      const r = fp.map(p=>p.rating_clean).filter(v=>v!==null);
      Plotly.newPlot('chartRatingDist', [{type:'histogram', x: r, nbinsx: 20, marker:{color:'rgba(34,197,94,.75)'}}], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Rating'}, yaxis:{title:'Count'},
        uirevision:'keep'
      }, PLOT_CONFIG);

      const ratingVals = fp.map(p=>p.rating_clean).filter(v=>v!==null).sort((a,b)=>a-b);
      const reviewsVals = fp.map(p=>p.rating_count_clean).filter(v=>v!==null).sort((a,b)=>a-b);
      const median = (arr) => arr.length ? arr[Math.floor(arr.length/2)] : 0;
      const rMed = median(ratingVals);
      const vMed = median(reviewsVals);
      Plotly.newPlot('chartQuadrants', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.rating_count_clean),
        y: fp.map(p=>p.rating_clean),
        text: fp.map(p=>truncName(p.product_name)),
        marker: { size: 8, color: 'rgba(34,197,94,.75)' }
      }], {
        shapes: [
          { type:'line', x0:vMed, x1:vMed, y0:0, y1:5, line:{color:'rgba(148,163,184,.35)', width:2, dash:'dot'} },
          { type:'line', x0:1, x1:Math.max(...reviewsVals, 10), y0:rMed, y1:rMed, line:{color:'rgba(148,163,184,.35)', width:2, dash:'dot'} }
        ],
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Rating Count', type:'log'}, yaxis:{title:'Rating', range:[0,5]},
        uirevision:'keep'
      }, PLOT_CONFIG);

      const leaders = fp
        .filter(p => p.rating_clean !== null && p.rating_count_clean !== null)
        .slice()
        .sort((a,b)=> (b.rating_clean* Math.log10(b.rating_count_clean+1)) - (a.rating_clean* Math.log10(a.rating_count_clean+1)))
        .slice(0,10);

      const score = (p) => (p.rating_clean || 0) * Math.log10((p.rating_count_clean || 0) + 1);
      const top = leaders.slice().reverse();
      Plotly.newPlot('chartLeaders', [{
        type:'bar', orientation:'h',
        y: top.map(p => truncName(p.product_name, 44)),
        x: top.map(p => score(p)),
        text: top.map(p => fmt(score(p),2)),
        textposition: 'outside',
        marker: { color: 'rgba(34,197,94,.78)' },
        customdata: top.map(p => [p.main_category]),
        hovertemplate: '%{y}<br>Leader score=%{x:.2f}<br>Category=%{customdata[0]}<extra></extra>'
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
        font:{color:'#e5e7eb', size: 11},
        margin:{l:220,r:50,t:10,b:40},
        xaxis:{title:'Leader score'}, yaxis:{automargin:true},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      const el = document.getElementById('chartLeaders');
      el.on('plotly_click', (ev) => {
        const cat = ev?.points?.[0]?.customdata?.[0];
        if (cat) toggleCategory(cat);
      });
    }

    let psiTable = null;
    function plotPsi() {
      const fp = filteredProducts().slice().sort((a,b)=> (b.PSI||0) - (a.PSI||0));
      const top = fp.slice(0, 20).reverse();
      Plotly.newPlot('chartPsiLeaderboard', [{
        type:'bar', orientation:'h',
        y: top.map(p=>truncName(p.product_name, 40)),
        x: top.map(p=>p.PSI),
        text: top.map(p=>fmt(p.PSI,1)),
        textposition: 'outside',
        marker:{color:'rgba(99,102,241,.85)', line:{width:0}}
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:220,r:50,t:10,b:40}, xaxis:{title:'PSI'},
        yaxis:{automargin:true},
        uirevision:'keep'
      }, PLOT_CONFIG);

      const fpAll = filteredProductsCategoryOnly();
      const op = fpAll.map(p => (!selection.clusters.size || selection.clusters.has(String(p.cluster))) ? 1 : 0.22);
      Plotly.newPlot('chartPsiVsPrice', [{
        type:'scatter', mode:'markers',
        x: fpAll.map(p=>p.discounted_price_clean),
        y: fpAll.map(p=>p.PSI),
        text: fpAll.map(p=>truncName(p.product_name)),
        customdata: fpAll.map(p => [String(p.cluster), p.cluster_name]),
        marker:{ size: 9, color: fpAll.map(p=>p.cluster), colorscale:'Turbo', opacity: op }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'₹'}, yaxis:{title:'PSI'},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      const psiVsPriceEl = document.getElementById('chartPsiVsPrice');
      psiVsPriceEl.on('plotly_click', (ev) => {
        const cl = ev?.points?.[0]?.customdata?.[0];
        if (cl !== null && cl !== undefined) {
          toggleSet(selection.clusters, cl);
          refreshAll();
        }
      });
      psiVsPriceEl.on('plotly_doubleclick', () => { selection.clusters.clear(); refreshAll(); });

      const byCat = {};
      fp.forEach(p => {
        const c = p.main_category || 'Unknown';
        if (p.PSI === null) return;
        if (!byCat[c]) byCat[c] = [];
        byCat[c].push(p.PSI);
      });
      const entries = Object.entries(byCat).map(([c, arr]) => [c, arr.reduce((a,b)=>a+b,0)/arr.length]).sort((a,b)=>b[1]-a[1]);
      Plotly.newPlot('chartPsiByCategory', [{
        type:'bar',
        x: entries.map(e=>e[0]),
        y: entries.map(e=>e[1]),
        marker:{color:'rgba(34,197,94,.78)'},
        text: entries.map(e=>fmt(e[1],1)),
        textposition:'outside',
        cliponaxis:false
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:120}, yaxis:{title:'Avg PSI'},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      const psiByCatEl = document.getElementById('chartPsiByCategory');
      psiByCatEl.on('plotly_click', (ev) => {
        const cat = ev?.points?.[0]?.x;
        if (cat) toggleCategory(cat);
      });

      const cols = [
        { title: 'Name', data: 'product_name' },
        { title: 'Category', data: 'main_category' },
        { title: 'PSI', data: 'PSI', render: (d) => d===null? 'n/a' : fmt(d,2) },
        { title: 'Rating', data: 'rating_clean', render: (d) => d===null? 'n/a' : fmt(d,2) },
        { title: 'Reviews', data: 'rating_count_clean', render: (d) => d===null? 'n/a' : fmt(d,0) },
        { title: 'Discount %', data: 'discount_pct_clean', render: (d) => d===null? 'n/a' : fmt(d,1) },
        { title: 'Cluster', data: 'cluster_name' }
      ];
      const tableEl = $('#psiTable');
      tableEl.empty();
      const thead = $('<thead><tr></tr></thead>');
      cols.forEach(c => thead.find('tr').append(`<th>${c.title}</th>`));
      tableEl.append(thead);
      psiTable = tableEl.DataTable(tableBaseOptions('psiTable', { data: fp, columns: cols, pageLength: 8 }));
      $('#psiTable tbody').off('click').on('click', 'tr', function() {
        const row = psiTable.row(this).data();
        if (!row) return;
        toggleSet(selection.clusters, row.cluster);
        refreshAll();
      });
    }

    function exportPsiCsv() {
      const rows = filteredProducts().slice().sort((a,b)=> (b.PSI||0) - (a.PSI||0));
      const headers = ['product_id','product_name','main_category','discounted_price_clean','discount_pct_clean','rating_clean','rating_count_clean','PSI','cluster','cluster_name'];
      const esc = (s) => {
        if (s === null || s === undefined) return '';
        const v = String(s).replace(/"/g,'""');
        return `"${v}"`;
      };
      const csv = [headers.join(',')].concat(rows.map(r => headers.map(h => esc(r[h])).join(','))).join('\\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'amazon_psi_filtered.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    function plotSegments() {
      const fpAll = filteredProductsCategoryOnly();
      const fp = filteredProducts();

      const opacity = fpAll.map(p => (!selection.clusters.size || selection.clusters.has(String(p.cluster))) ? 1 : 0.22);
      Plotly.newPlot('chartPca', [{
        type:'scatter', mode:'markers',
        x: fpAll.map(p=>p.pca_1), y: fpAll.map(p=>p.pca_2),
        text: fpAll.map(p=>truncName(p.product_name)),
        customdata: fpAll.map(p => [String(p.cluster), p.cluster_name]),
        marker:{ size: 9, color: fpAll.map(p=>p.cluster), colorscale:'Turbo', opacity: opacity }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'PCA 1'}, yaxis:{title:'PCA 2'},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      const pcaEl = document.getElementById('chartPca');
      pcaEl.on('plotly_click', (ev) => {
        const cl = ev?.points?.[0]?.customdata?.[0];
        if (cl !== null && cl !== undefined) {
          toggleSet(selection.clusters, cl);
          refreshAll();
        }
      });
      pcaEl.on('plotly_doubleclick', () => { selection.clusters.clear(); refreshAll(); });

      /* Cluster cards (respeitam apenas Category; seleção = highlight) */
      const byCluster = {};
      fpAll.forEach(p => {
        const id = p.cluster;
        if (id === null || id === undefined) return;
        if (!byCluster[id]) byCluster[id] = { n:0, name: p.cluster_name || `Cluster ${id}`, rating:0, discount:0, price:0, psi:0 };
        byCluster[id].n += 1;
        byCluster[id].rating += (p.rating_clean || 0);
        byCluster[id].discount += (p.discount_pct_clean || 0);
        byCluster[id].price += (p.discounted_price_clean || 0);
        byCluster[id].psi += (p.PSI || 0);
      });
      const cards = Object.entries(byCluster).sort((a,b)=>b[1].n-a[1].n).map(([id, c]) => {
        const n = c.n || 1;
        const selected = selection.clusters.has(String(id));
        const border = selected ? 'border-color: rgba(99,102,241,.85); box-shadow: 0 0 0 1px rgba(99,102,241,.18), var(--shadow);' : '';
        return `
          <div class="card" data-cluster-id="${id}" style="margin-bottom:10px;cursor:pointer;${border}">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="font-weight:800">${c.name}</div>
              <span class="pill">${fmt(n,0)} products</span>
            </div>
            <div class="muted" style="margin-top:8px">Avg rating: ${fmt(c.rating/n,2)} · Avg discount: ${fmt(c.discount/n,2)}% · Avg price: ₹${fmt(c.price/n,0)} · Avg PSI: ${fmt(c.psi/n,2)}</div>
          </div>
        `;
      }).join('');
      const cardsEl = document.getElementById('clusterCards');
      cardsEl.innerHTML = cards;
      cardsEl.onclick = (e) => {
        const target = e.target.closest('[data-cluster-id]');
        if (!target) return;
        toggleSet(selection.clusters, target.getAttribute('data-cluster-id'));
        refreshAll();
      };

      /* Treemap agregado: root -> clusters -> categories */
      const agg = {};
      const clusterMeta = {};
      fpAll.forEach(p => {
        const clId = String(p.cluster);
        const clName = p.cluster_name || `Cluster ${clId}`;
        clusterMeta[clId] = clName;
        const cat = p.main_category || 'Unknown';
        const k = clId + '||' + cat;
        agg[k] = (agg[k] || 0) + 1;
      });
      const clusterTotals = {};
      Object.entries(agg).forEach(([k, cnt]) => {
        const [clId] = k.split('||');
        clusterTotals[clId] = (clusterTotals[clId] || 0) + cnt;
      });
      const ids = ['root'];
      const labels = ['Amazon Products'];
      const parents = [''];
      const values = [Object.values(clusterTotals).reduce((a,b)=>a+b,0)];

      Object.entries(clusterTotals).sort((a,b)=>b[1]-a[1]).forEach(([clId, cnt]) => {
        ids.push('cluster|' + clId);
        labels.push(clusterMeta[clId] || ('Cluster ' + clId));
        parents.push('root');
        values.push(cnt);
      });
      Object.entries(agg).forEach(([k, cnt]) => {
        const [clId, cat] = k.split('||');
        ids.push('leaf|' + clId + '|' + cat);
        labels.push(cat);
        parents.push('cluster|' + clId);
        values.push(cnt);
      });

      Plotly.newPlot('chartTreemap', [{
        type: 'treemap',
        ids,
        labels,
        parents,
        values,
        branchvalues: 'total',
        textinfo: 'label+value',
        marker: { colorscale: 'Turbo', line: { width: 1, color: 'rgba(10,14,26,.8)' } }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'}, margin:{l:10,r:10,t:10,b:10},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      const tmEl = document.getElementById('chartTreemap');
      tmEl.on('plotly_click', (ev) => {
        const id = ev?.points?.[0]?.id;
        if (!id) return;
        if (id.startsWith('cluster|')) {
          toggleSet(selection.clusters, id.split('|')[1]);
          refreshAll();
          return;
        }
        if (id.startsWith('leaf|')) {
          const parts = id.split('|');
          const clId = parts[1];
          const cat = parts.slice(2).join('|');
          if (cat) toggleCategory(cat);
          toggleSet(selection.clusters, clId);
          refreshAll();
        }
      });
      tmEl.on('plotly_doubleclick', () => { selection.clusters.clear(); refreshAll(); });

      /* Opportunity notes: se houver seleção, mostrar somente selecionados; senão, top oportunidade */
      const opp = Object.entries(byCluster).map(([id,c]) => ({
        id: String(id),
        name: c.name,
        n: c.n,
        avgR: (c.rating/(c.n||1)),
        avgD: (c.discount/(c.n||1)),
        score: (c.rating/(c.n||1)) * (c.discount/(c.n||1))
      })).sort((a,b)=>b.score-a.score);
      const oppEl = document.getElementById('clusterOpportunity');
      if (!opp.length) { oppEl.textContent = 'n/a'; return; }
      const sel = selection.clusters;
      const list = sel.size ? opp.filter(o => sel.has(o.id)) : opp.slice(0, 1);
      oppEl.innerHTML = list.map(o =>
        `• <b>${o.name}</b> (${fmt(o.n,0)} produtos): rating ${fmt(o.avgR,2)} · desconto ${fmt(o.avgD,1)}%`
      ).join('<br/>');
    }

    let reviewsTable = null;
    function plotSentiment() {
      const fr = filteredReviews();
      const scores = fr.map(r => r.sentiment_score).filter(v => v !== null && v !== undefined);
      const mean = scores.length ? scores.reduce((a,b)=>a+Number(b),0)/scores.length : 0;
      const gauge = Math.max(0, Math.min(100, (mean + 1) * 50));
      Plotly.newPlot('chartSentimentGauge', [{
        type: 'indicator', mode: 'gauge+number', value: gauge,
        number: { suffix: '/100' },
        gauge: { axis: { range: [0, 100] }, bar: { color: '#22c55e' },
          steps: [
            { range: [0, 40], color: 'rgba(239,68,68,.25)' },
            { range: [40, 60], color: 'rgba(245,158,11,.20)' },
            { range: [60, 100], color: 'rgba(34,197,94,.20)' }
          ] }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'}, margin:{l:20,r:20,t:10,b:10}
      }, {displayModeBar:false});

      const byCat = {};
      fr.forEach(r => {
        const c = r.main_category || 'Unknown';
        const s = r.sentimento_label || 'n/a';
        if (!byCat[c]) byCat[c] = {positivo:0, neutro:0, negativo:0};
        if (byCat[c][s] !== undefined) byCat[c][s] += 1;
      });
      const cats = Object.keys(byCat);
      const pos = cats.map(c => byCat[c].positivo || 0);
      const neu = cats.map(c => byCat[c].neutro || 0);
      const neg = cats.map(c => byCat[c].negativo || 0);
      Plotly.newPlot('chartSentimentByCategory', [
        {type:'bar', name:'positivo', x: cats, y: pos, marker:{color:'rgba(34,197,94,.75)', opacity: (!selection.sentiments.size || selection.sentiments.has('positivo')) ? 1 : 0.25}},
        {type:'bar', name:'neutro', x: cats, y: neu, marker:{color:'rgba(148,163,184,.55)', opacity: (!selection.sentiments.size || selection.sentiments.has('neutro')) ? 1 : 0.25}},
        {type:'bar', name:'negativo', x: cats, y: neg, marker:{color:'rgba(239,68,68,.70)', opacity: (!selection.sentiments.size || selection.sentiments.has('negativo')) ? 1 : 0.25}}
      ], {
        barmode:'stack', paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:120},
        uirevision:'keep',
        clickmode:'event+select'
      }, PLOT_CONFIG);
      const sEl = document.getElementById('chartSentimentByCategory');
      sEl.on('plotly_click', (ev) => {
        const cat = ev?.points?.[0]?.x;
        const label = ev?.points?.[0]?.data?.name;
        if (cat) setFilterCategory(cat);
        if (label) toggleSet(selection.sentiments, label);
        refreshAll();
      });
      sEl.on('plotly_doubleclick', () => { selection.sentiments.clear(); refreshAll(); });

      Plotly.newPlot('chartSentimentVsRating', [{
        type:'scatter', mode:'markers',
        x: fr.map(r=>r.sentiment_score),
        y: fr.map(r=>r.rating_clean),
        text: fr.map(r=>r.review_title),
        marker:{ size: 7, color:'rgba(99,102,241,.85)' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Sentiment (compound)'}, yaxis:{title:'Rating'},
        uirevision:'keep'
      }, PLOT_CONFIG);

      const text = fr.map(r => `${r.review_title || ''} ${r.review_content || ''}`.trim()).join(' ').toLowerCase();
      const tokens = text.replace(/[^a-z\\s]/g,' ').split(/\\s+/).filter(w => w.length>=4);
      const stop = new Set(['this','that','with','have','has','from','they','them','your','very','into','were','was','are','amazon','product','good','bad','nice']);
      const freq = {};
      tokens.forEach(w => { if (stop.has(w)) return; freq[w] = (freq[w]||0)+1; });
      const top = Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0, 28);
      const max = top.length ? top[0][1] : 1;
      document.getElementById('wordCloud').innerHTML = top.map(([w,n]) => {
        const t = Math.max(0.0, Math.min(1.0, n/max));
        const opacity = (0.55 + 0.45*t).toFixed(2);
        const bg = (0.06 + 0.18*t).toFixed(2);
        return `<span class="word" style="opacity:${opacity};background:rgba(99,102,241,${bg})">${w}</span>`;
      }).join('');

      const topReviews = fr
        .filter(r => r.sentiment_score !== null && r.sentiment_score !== undefined)
        .slice()
        .sort((a,b)=> Number(b.sentiment_score) - Number(a.sentiment_score))
        .slice(0, 10)
        .concat(fr.slice().sort((a,b)=> Number(a.sentiment_score) - Number(b.sentiment_score)).slice(0, 10));

      const cols = [
        { title: 'Product', data: 'product_name' },
        { title: 'Category', data: 'main_category' },
        { title: 'Sentiment', data: 'sentiment_score', render: (d) => d===null? 'n/a' : fmt(d,3) },
        { title: 'Rating', data: 'rating_clean', render: (d) => d===null? 'n/a' : fmt(d,2) },
        { title: 'Title', data: 'review_title' }
      ];
      const tableEl = $('#reviewsTable');
      tableEl.empty();
      const thead = $('<thead><tr></tr></thead>');
      cols.forEach(c => thead.find('tr').append(`<th>${c.title}</th>`));
      tableEl.append(thead);
      reviewsTable = tableEl.DataTable(tableBaseOptions('reviewsTable', { data: topReviews, columns: cols, pageLength: 8, searching: false }));
    }

    function renderQA() {
      document.getElementById('qaAccordion').innerHTML = qa.map(x => `
        <details style="margin-bottom:10px">
          <summary>Q${x.n}. ${x.question}</summary>
          <div class="muted" style="margin-top:8px"><b style="color:#e5e7eb">Answer:</b> ${x.answer}</div>
          <div class="muted" style="margin-top:8px"><b style="color:#e5e7eb">Insight:</b> ${x.insight}</div>
          <div class="muted" style="margin-top:8px"><b style="color:#e5e7eb">Recommendation:</b> ${x.recommendation}</div>
        </details>
      `).join('');
    }

    let catalogTable = null;
    function initCatalogTable() {
      const cols = [
        { title: 'Image', data: 'img_link', render: (d) => d ? `<img src="${d}" style="width:44px;height:44px;object-fit:cover;border-radius:10px" onerror="this.onerror=null;this.src='${IMG_PLACEHOLDER}'"/>` : '<div class="img-placeholder">📦</div>' },
        { title: 'Name', data: 'product_name', render: (d, t, r) => { const n = truncName(d); return r.product_link ? `<a href="${r.product_link}" target="_blank">${n}</a>` : n; } },
        { title: 'Category', data: 'main_category' },
        { title: 'Price (₹)', data: 'discounted_price_clean', render: (d) => d===null? 'n/a' : fmt(d,0) },
        { title: 'Discount %', data: 'discount_pct_clean', render: (d) => d===null? 'n/a' : fmt(d,1) },
        { title: 'Rating', data: 'rating_clean', render: (d) => d===null? 'n/a' : fmt(d,2) },
        { title: 'PSI', data: 'PSI', render: (d) => d===null? 'n/a' : fmt(d,2) },
        { title: 'Cluster', data: 'cluster_name' }
      ];
      const tableEl = $('#catalogTable');
      tableEl.empty();
      const thead = $('<thead><tr></tr></thead>');
      cols.forEach(c => thead.find('tr').append(`<th>${c.title}</th>`));
      tableEl.append(thead);
      catalogTable = tableEl.DataTable(tableBaseOptions('catalogTable', {
        data: filteredProducts(),
        columns: cols,
        pageLength: 10,
        dom: '<"dt-toolbar"f>t<"dt-footer"ip>'
      }));
    }

    function refreshCatalogTable() {
      if (!catalogTable) return initCatalogTable();
      catalogTable.clear();
      catalogTable.rows.add(filteredProducts());
      catalogTable.draw(false);
    }

    function exportCatalogCsv() {
      const rows = filteredProducts();
      const headers = ['product_id','product_name','main_category','sub_category','discounted_price_clean','discount_pct_clean','rating_clean','rating_count_clean','PSI','cluster','cluster_name'];
      const esc = (s) => {
        if (s === null || s === undefined) return '';
        const v = String(s).replace(/"/g,'""');
        return `"${v}"`;
      };
      const csv = [headers.join(',')].concat(rows.map(r => headers.map(h => esc(r[h])).join(','))).join('\\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'amazon_products_filtered.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    function activateTab(tab) {
      const buttons = Array.from(document.querySelectorAll('.nav button'));
      buttons.forEach(x => x.classList.toggle('active', x.getAttribute('data-tab') === tab));
      Array.from(document.querySelectorAll('.section')).forEach(s => s.classList.remove('active'));
      const section = document.getElementById(tab);
      if (!section) return;
      section.classList.add('active');
      section.classList.add('fade');
      setTimeout(() => section.classList.remove('fade'), 260);
      placeFilterForTab(tab);
      scheduleActiveLayoutRefresh();
    }

    function setUpNav() {
      const buttons = Array.from(document.querySelectorAll('.nav button'));
      buttons.forEach(b => b.addEventListener('click', () => activateTab(b.getAttribute('data-tab'))));
    }

    function initFilter() {
      const categories = unique(products.map(p => p.main_category).filter(Boolean)).sort();
      const sel = document.getElementById('categoryFilter');
      sel.innerHTML = `<option value="__ALL__">All categories</option>` + categories.map(c => `<option value="${c}">${c}</option>`).join('');
      sel.addEventListener('change', () => {
        refreshAll();
      });
    }

    document.getElementById('exportCatalogBtn').addEventListener('click', exportCatalogCsv);
    document.getElementById('exportPsiBtn').addEventListener('click', exportPsiCsv);

    setTicker();
    initFilter();
    setUpNav();
    renderKpis();
    plotQualityGauge();
    renderQA();
    initCatalogTable();
    activateTab('overview');
    refreshAll();
  </script>
</body>
</html>
"""
    style_open = "<style>"
    style_close = "</style>"
    start = html.find(style_open)
    end = html.find(style_close)
    if start != -1 and end != -1 and end > start:
        css_start = start + len(style_open)
        css = html[css_start:end].replace("{{", "{").replace("}}", "}")
        html = html[:css_start] + css + html[end:]
    html = html.replace("__FAVICON_HREF__", favicon_href)
    return html.replace("__DASHBOARD_DATA_B64__", data_b64)


def write_dashboard(dashboard_data: dict[str, Any], output_path: Path) -> Path:
    """Write dashboard HTML to disk."""
    output_path.write_text(render_dashboard_html(dashboard_data), encoding="utf-8")
    return output_path

