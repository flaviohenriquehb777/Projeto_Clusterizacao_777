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
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      background:
        radial-gradient(1200px 700px at 30% -10%, rgba(99,102,241,.25), transparent 60%),
        radial-gradient(900px 600px at 110% 10%, rgba(34,197,94,.18), transparent 60%),
        var(--bg);
      color: var(--text);
    }}
    a {{ color: #a5b4fc; text-decoration: none; }}
    .app {{ display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }}
    .sidebar {{
      position: sticky;
      top: 0;
      height: 100vh;
      padding: 22px 18px;
      background: linear-gradient(180deg, rgba(17,24,39,.92), rgba(10,14,26,.92));
      border-right: 1px solid rgba(148,163,184,.12);
    }}
    .brand {{ font-weight: 800; letter-spacing: -0.02em; font-size: 18px; margin-bottom: 18px; }}
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
    .nav button.active {{ border-color: rgba(99,102,241,.85); background: rgba(99,102,241,.12); }}
    .icon {{ width: 22px; height: 22px; display: grid; place-items: center; border-radius: 8px; background: rgba(99,102,241,.18); }}
    .main {{ padding: 22px; }}
    .topbar {{ display: grid; grid-template-columns: 1fr 320px; gap: 12px; align-items: center; margin-bottom: 14px; }}
    .ticker {{
      overflow: hidden;
      border-radius: 14px;
      border: 1px solid rgba(148,163,184,.12);
      background: rgba(17,24,39,.65);
      box-shadow: var(--shadow);
    }}
    .ticker-track {{ display: inline-block; white-space: nowrap; padding: 10px 0; animation: marquee 22s linear infinite; }}
    .ticker-item {{ display: inline-block; padding: 0 26px; color: var(--muted); }}
    @keyframes marquee {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
    .filter {{ display: flex; justify-content: flex-end; gap: 10px; align-items: center; }}
    select {{
      width: 100%;
      border-radius: 12px;
      padding: 10px 12px;
      background: rgba(17,24,39,.65);
      color: var(--text);
      border: 1px solid rgba(148,163,184,.12);
      outline: none;
    }}
    .grid {{ display: grid; gap: 14px; }}
    .kpis {{ grid-template-columns: repeat(6, minmax(0, 1fr)); }}
    .card {{
      background: rgba(17,24,39,.75);
      border: 1px solid rgba(148,163,184,.12);
      border-radius: 16px;
      padding: 14px;
      box-shadow: var(--shadow);
    }}
    .kpi-title {{ color: var(--muted); font-size: 12px; }}
    .kpi-value {{ font-size: 22px; font-weight: 800; margin-top: 6px; letter-spacing: -0.02em; }}
    .fade {{ animation: fade .25s ease; }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .section {{ display: none; }}
    .section.active {{ display: block; }}
    .row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    .row3 {{ display: grid; grid-template-columns: 1.2fr .8fr; gap: 14px; }}
    .title {{ font-size: 18px; font-weight: 800; margin: 6px 0 10px; }}
    .muted {{ color: var(--muted); }}
    .datatable-wrap table {{ width: 100%; }}
    table.dataTable {{ background: rgba(17,24,39,.75); color: var(--text); border-radius: 14px; overflow: hidden; }}
    table.dataTable thead th {{ background: rgba(99,102,241,.12); color: var(--text); border-bottom: 1px solid rgba(148,163,184,.12); }}
    table.dataTable tbody td {{ border-bottom: 1px solid rgba(148,163,184,.08); }}
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
    }}
    .btn:hover {{ background: rgba(99,102,241,.22); }}
    .accordion details {{
      border: 1px solid rgba(148,163,184,.12);
      background: rgba(17,24,39,.65);
      border-radius: 14px;
      padding: 10px 12px;
    }}
    .accordion summary {{ cursor: pointer; font-weight: 700; }}
    .wordcloud {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .word {{ padding: 6px 10px; border-radius: 999px; border: 1px solid rgba(148,163,184,.12); background: rgba(99,102,241,.08); }}
    @media (max-width: 1100px) {{
      .app {{ grid-template-columns: 1fr; }}
      .sidebar {{ height: auto; position: relative; }}
      .kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .row, .row3 {{ grid-template-columns: 1fr; }}
      .topbar {{ grid-template-columns: 1fr; }}
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
        <div class="filter">
          <div style="width: 100%">
            <div class="muted" style="font-size:12px;margin-bottom:6px;">Global filter — Main Category</div>
            <select id="categoryFilter"></select>
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
            <div class="title">Top 10 — Rating + Volume</div>
            <div class="datatable-wrap" style="margin-top:10px">
              <table id="leadersTable" class="display"></table>
            </div>
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
        <div class="row3">
          <div class="card">
            <div class="title">Clusters (PCA 2D)</div>
            <div id="chartPca" style="height:520px"></div>
          </div>
          <div class="card">
            <div class="title">Cluster Profiles</div>
            <div id="clusterCards"></div>
          </div>
        </div>
        <div class="row" style="margin-top:14px">
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

    function getFilterCategory() {
      const v = document.getElementById('categoryFilter').value;
      return v === '__ALL__' ? null : v;
    }

    function filteredProducts() {
      const c = getFilterCategory();
      if (!c) return products;
      return products.filter(p => p.main_category === c);
    }

    function filteredReviews() {
      const c = getFilterCategory();
      if (!c) return reviews;
      return reviews.filter(r => r.main_category === c);
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
      Plotly.newPlot('chartCategoryBar', [{type:'bar', x, y, marker:{color:'rgba(99,102,241,.85)'}}], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
        font:{color:'#e5e7eb'}, margin:{l:40,r:10,t:10,b:90}
      }, {displayModeBar:false});
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
        margin:{l:50,r:10,t:10,b:120}, yaxis:{title:'₹'}
      }, {displayModeBar:false});

      const colors = fp.map(p => p.faixa_desconto || 'n/a');
      Plotly.newPlot('chartPriceDiscount', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.discounted_price_clean),
        y: fp.map(p=>p.discount_pct_clean),
        text: fp.map(p=>p.product_name),
        marker:{ size: 9, color: colors, colorscale: 'Viridis' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'₹'}, yaxis:{title:'Discount %'}
      }, {displayModeBar:false});

      const disc = fp.map(p=>p.discount_pct_clean).filter(v=>v!==null);
      Plotly.newPlot('chartDiscountHist', [{type:'histogram', x: disc, marker:{color:'rgba(99,102,241,.85)'}}], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Discount %'}, yaxis:{title:'Count'}
      }, {displayModeBar:false});

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
        margin:{l:70,r:10,t:10,b:120}
      }, {displayModeBar:false});
    }

    let leadersTable = null;
    function plotRatings() {
      const fp = filteredProducts();
      Plotly.newPlot('chartRatingReviews', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.rating_count_clean),
        y: fp.map(p=>p.rating_clean),
        text: fp.map(p=>p.product_name),
        marker: { size: fp.map(p => Math.max(6, Math.min(30, (p.discounted_price_clean || 0)/500))), color: 'rgba(99,102,241,.85)' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Rating Count', type:'log'}, yaxis:{title:'Rating'}
      }, {displayModeBar:false});

      const r = fp.map(p=>p.rating_clean).filter(v=>v!==null);
      Plotly.newPlot('chartRatingDist', [{type:'histogram', x: r, nbinsx: 20, marker:{color:'rgba(34,197,94,.75)'}}], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Rating'}, yaxis:{title:'Count'}
      }, {displayModeBar:false});

      const ratingVals = fp.map(p=>p.rating_clean).filter(v=>v!==null).sort((a,b)=>a-b);
      const reviewsVals = fp.map(p=>p.rating_count_clean).filter(v=>v!==null).sort((a,b)=>a-b);
      const median = (arr) => arr.length ? arr[Math.floor(arr.length/2)] : 0;
      const rMed = median(ratingVals);
      const vMed = median(reviewsVals);
      Plotly.newPlot('chartQuadrants', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.rating_count_clean),
        y: fp.map(p=>p.rating_clean),
        text: fp.map(p=>p.product_name),
        marker: { size: 8, color: 'rgba(34,197,94,.75)' }
      }], {
        shapes: [
          { type:'line', x0:vMed, x1:vMed, y0:0, y1:5, line:{color:'rgba(148,163,184,.35)', width:2, dash:'dot'} },
          { type:'line', x0:1, x1:Math.max(...reviewsVals, 10), y0:rMed, y1:rMed, line:{color:'rgba(148,163,184,.35)', width:2, dash:'dot'} }
        ],
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Rating Count', type:'log'}, yaxis:{title:'Rating', range:[0,5]}
      }, {displayModeBar:false});

      const leaders = fp
        .filter(p => p.rating_clean !== null && p.rating_count_clean !== null)
        .slice()
        .sort((a,b)=> (b.rating_clean* Math.log10(b.rating_count_clean+1)) - (a.rating_clean* Math.log10(a.rating_count_clean+1)))
        .slice(0,10);

      const cols = [
        { title: 'Name', data: 'product_name' },
        { title: 'Category', data: 'main_category' },
        { title: 'Rating', data: 'rating_clean', render: (d) => d===null? 'n/a' : fmt(d,2) },
        { title: 'Reviews', data: 'rating_count_clean', render: (d) => d===null? 'n/a' : fmt(d,0) },
        { title: 'Price (₹)', data: 'discounted_price_clean', render: (d) => d===null? 'n/a' : fmt(d,0) },
        { title: 'Discount %', data: 'discount_pct_clean', render: (d) => d===null? 'n/a' : fmt(d,1) }
      ];
      const tableEl = $('#leadersTable');
      tableEl.empty();
      const thead = $('<thead><tr></tr></thead>');
      cols.forEach(c => thead.find('tr').append(`<th>${c.title}</th>`));
      tableEl.append(thead);
      leadersTable = tableEl.DataTable({ data: leaders, columns: cols, pageLength: 5, destroy: true, searching: false, lengthChange: false, info: false });
    }

    let psiTable = null;
    function plotPsi() {
      const fp = filteredProducts().slice().sort((a,b)=> (b.PSI||0) - (a.PSI||0));
      const top = fp.slice(0, 20).reverse();
      Plotly.newPlot('chartPsiLeaderboard', [{
        type:'bar', orientation:'h',
        y: top.map(p=>p.product_name),
        x: top.map(p=>p.PSI),
        marker:{color:'rgba(99,102,241,.85)'}
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:160,r:10,t:10,b:40}, xaxis:{title:'PSI'}
      }, {displayModeBar:false});

      Plotly.newPlot('chartPsiVsPrice', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.discounted_price_clean),
        y: fp.map(p=>p.PSI),
        text: fp.map(p=>p.product_name),
        marker:{ size: 9, color: fp.map(p=>p.cluster), colorscale:'Turbo' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'₹'}, yaxis:{title:'PSI'}
      }, {displayModeBar:false});

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
        marker:{color:'rgba(34,197,94,.75)'}
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:120}, yaxis:{title:'Avg PSI'}
      }, {displayModeBar:false});

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
      psiTable = tableEl.DataTable({ data: fp, columns: cols, pageLength: 10, destroy: true });
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
      const fp = filteredProducts();
      Plotly.newPlot('chartPca', [{
        type:'scatter', mode:'markers',
        x: fp.map(p=>p.pca_1), y: fp.map(p=>p.pca_2),
        text: fp.map(p=>p.product_name),
        marker:{ size: 9, color: fp.map(p=>p.cluster), colorscale:'Turbo' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'PCA 1'}, yaxis:{title:'PCA 2'}
      }, {displayModeBar:false});

      const byCluster = {};
      fp.forEach(p => {
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
        const n = c.n;
        return `
          <div class="card" style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <div style="font-weight:800">${c.name}</div>
              <span class="pill">${fmt(n,0)} products</span>
            </div>
            <div class="muted" style="margin-top:8px">Avg rating: ${fmt(c.rating/n,2)} · Avg discount: ${fmt(c.discount/n,2)}% · Avg price: ₹${fmt(c.price/n,0)} · Avg PSI: ${fmt(c.psi/n,2)}</div>
          </div>
        `;
      }).join('');
      document.getElementById('clusterCards').innerHTML = cards;

      const treemapRows = fp.map(p => ({
        cluster_name: p.cluster_name || `Cluster ${p.cluster}`,
        main_category: p.main_category || 'Unknown',
        value: 1
      }));
      Plotly.newPlot('chartTreemap', [{
        type: 'treemap',
        labels: treemapRows.map(r => r.main_category),
        parents: treemapRows.map(r => r.cluster_name),
        values: treemapRows.map(r => r.value),
        branchvalues: 'total'
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'}, margin:{l:10,r:10,t:10,b:10}
      }, {displayModeBar:false});

      const opp = Object.entries(byCluster).map(([id,c]) => ({
        id: id,
        name: c.name,
        score: (c.rating/c.n) * (c.discount/c.n)
      })).sort((a,b)=>b.score-a.score);
      document.getElementById('clusterOpportunity').textContent = opp.length
        ? `Highest opportunity score (avg rating × avg discount): ${opp[0].name}`
        : 'n/a';
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
        {type:'bar', name:'positivo', x: cats, y: pos, marker:{color:'rgba(34,197,94,.75)'}},
        {type:'bar', name:'neutro', x: cats, y: neu, marker:{color:'rgba(148,163,184,.55)'}},
        {type:'bar', name:'negativo', x: cats, y: neg, marker:{color:'rgba(239,68,68,.70)'}}
      ], {
        barmode:'stack', paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:120}
      }, {displayModeBar:false});

      Plotly.newPlot('chartSentimentVsRating', [{
        type:'scatter', mode:'markers',
        x: fr.map(r=>r.sentiment_score),
        y: fr.map(r=>r.rating_clean),
        text: fr.map(r=>r.review_title),
        marker:{ size: 7, color:'rgba(99,102,241,.85)' }
      }], {
        paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{color:'#e5e7eb'},
        margin:{l:50,r:10,t:10,b:50}, xaxis:{title:'Sentiment (compound)'}, yaxis:{title:'Rating'}
      }, {displayModeBar:false});

      const text = fr.map(r => `${r.review_title || ''} ${r.review_content || ''}`.trim()).join(' ').toLowerCase();
      const tokens = text.replace(/[^a-z\\s]/g,' ').split(/\\s+/).filter(w => w.length>=4);
      const stop = new Set(['this','that','with','have','has','from','they','them','your','very','into','were','was','are','amazon','product','good','bad','nice']);
      const freq = {};
      tokens.forEach(w => { if (stop.has(w)) return; freq[w] = (freq[w]||0)+1; });
      const top = Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0, 28);
      const max = top.length ? top[0][1] : 1;
      document.getElementById('wordCloud').innerHTML = top.map(([w,n]) => {
        const size = 12 + Math.round((n/max) * 22);
        return `<span class="word" style="font-size:${size}px">${w}</span>`;
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
      reviewsTable = tableEl.DataTable({ data: topReviews, columns: cols, pageLength: 10, destroy: true, searching: false, lengthChange: false });
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
        { title: 'Image', data: 'img_link', render: (d) => d ? `<img src="${d}" style="width:44px;height:44px;object-fit:cover;border-radius:10px"/>` : '' },
        { title: 'Name', data: 'product_name', render: (d, t, r) => r.product_link ? `<a href="${r.product_link}" target="_blank">${d}</a>` : d },
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
      catalogTable = tableEl.DataTable({ data: filteredProducts(), columns: cols, pageLength: 10, destroy: true });
    }

    function refreshCatalogTable() {
      if (!catalogTable) return initCatalogTable();
      catalogTable.clear();
      catalogTable.rows.add(filteredProducts());
      catalogTable.draw();
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

    function setUpNav() {
      const buttons = Array.from(document.querySelectorAll('.nav button'));
      buttons.forEach(b => b.addEventListener('click', () => {
        buttons.forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        const tab = b.getAttribute('data-tab');
        Array.from(document.querySelectorAll('.section')).forEach(s => s.classList.remove('active'));
        const section = document.getElementById(tab);
        section.classList.add('active');
        section.classList.add('fade');
        setTimeout(() => section.classList.remove('fade'), 260);
      }));
    }

    function initFilter() {
      const categories = unique(products.map(p => p.main_category).filter(Boolean)).sort();
      const sel = document.getElementById('categoryFilter');
      sel.innerHTML = `<option value="__ALL__">All categories</option>` + categories.map(c => `<option value="${c}">${c}</option>`).join('');
      sel.addEventListener('change', () => {
        plotPricing();
        plotRatings();
        plotPsi();
        plotSegments();
        plotSentiment();
        refreshCatalogTable();
      });
    }

    document.getElementById('exportCatalogBtn').addEventListener('click', exportCatalogCsv);
    document.getElementById('exportPsiBtn').addEventListener('click', exportPsiCsv);

    setTicker();
    initFilter();
    setUpNav();
    renderKpis();
    plotCategoryBar();
    plotQualityGauge();
    plotPricing();
    plotRatings();
    plotPsi();
    plotSegments();
    plotSentiment();
    renderQA();
    initCatalogTable();
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

