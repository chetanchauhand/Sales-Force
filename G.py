import os, textwrap, zipfile

base = "/mnt/data/citymind-ai"
os.makedirs(base + "/src", exist_ok=True)

files = {
"package.json": r'''{
  "name": "citymind-ai",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^0.468.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "recharts": "^2.15.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.0.7"
  }
}''',
"index.html": r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#07111f" />
    <meta name="description" content="CityMind AI — an interactive smart-city traffic operations simulator." />
    <title>CityMind AI | Urban Operations</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>''',
"src/main.jsx": r'''import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <React.StrictMode><App /></React.StrictMode>
);''',
"src/App.jsx": r'''import { useEffect, useMemo, useState } from "react";
import {
  Activity, AlertTriangle, ArrowDownRight, ArrowUpRight, Bell, Bot,
  CarFront, Check, ChevronDown, Clock3, CloudRain, Command, Gauge,
  GitBranch, Layers3, Lightbulb, MapPin, Pause, Play, Radio, RotateCcw,
  Settings2, ShieldCheck, Siren, SlidersHorizontal, Sparkles, TrainFront,
  TrafficCone, Zap
} from "lucide-react";
import {
  Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis
} from "recharts";

const initialJunctions = [
  { id: "J-01", name: "Central Square", road: "Civic Ave × 5th Street", status: "Optimizing", flow: 82, wait: 24, queue: 13, phase: "North / South", x: 50, y: 47 },
  { id: "J-02", name: "Riverside Gate", road: "River Road × Bridge St", status: "Normal", flow: 68, wait: 31, queue: 19, phase: "East / West", x: 73, y: 27 },
  { id: "J-03", name: "Market District", road: "Market St × Old Town Rd", status: "Congested", flow: 34, wait: 76, queue: 37, phase: "North / South", x: 28, y: 27 },
  { id: "J-04", name: "University Loop", road: "Campus Way × Oak Blvd", status: "Normal", flow: 74, wait: 28, queue: 16, phase: "East / West", x: 25, y: 68 },
  { id: "J-05", name: "South Transit", road: "Station Rd × Ring Road", status: "Incident", flow: 22, wait: 112, queue: 42, phase: "Emergency priority", x: 72, y: 69 },
  { id: "J-06", name: "Innovation Park", road: "Tech Pkwy × Cloud Ave", status: "Normal", flow: 89, wait: 18, queue: 9, phase: "North / South", x: 50, y: 18 }
];

const seedChart = [
  { time: "08:00", congestion: 68, throughput: 42 },
  { time: "08:10", congestion: 61, throughput: 49 },
  { time: "08:20", congestion: 72, throughput: 44 },
  { time: "08:30", congestion: 56, throughput: 57 },
  { time: "08:40", congestion: 49, throughput: 63 },
  { time: "08:50", congestion: 43, throughput: 69 },
  { time: "09:00", congestion: 38, throughput: 74 }
];

const events = [
  { type: "critical", title: "Slow traffic detected", detail: "South Transit · Queue exceeds 40 vehicles", time: "Just now" },
  { type: "success", title: "Signal timing improved", detail: "Central Square · Estimated wait −18%", time: "2 min ago" },
  { type: "info", title: "Emergency corridor ready", detail: "Route available from South Transit to City Hospital", time: "6 min ago" }
];

function Metric({ icon: Icon, label, value, unit, trend, tone = "cyan" }) {
  return <article className="metric panel">
    <div className={`metric-icon ${tone}`}><Icon size={18} /></div>
    <div className="metric-copy"><span>{label}</span><div className="metric-value">{value}<small>{unit}</small></div></div>
    <div className={`trend ${trend.startsWith("+") ? "up" : "down"}`}>{trend.startsWith("+") ? <ArrowUpRight size={14}/> : <ArrowDownRight size={14}/>} {trend}</div>
  </article>;
}

function MapView({ junctions, selected, onSelect, emergency, weather }) {
  return <div className="map-stage">
    <div className="map-grid" />
    <svg className="roads" viewBox="0 0 100 100" preserveAspectRatio="none" aria-label="Schematic city traffic map">
      <path className="road-main" d="M -5 48 L 105 48 M 49 -5 L 49 105 M 10 18 L 90 82 M 8 84 L 92 16 M 0 72 L 100 30 M 19 0 L 80 100" />
      <path className="road-center" d="M -5 48 L 105 48 M 49 -5 L 49 105 M 10 18 L 90 82 M 8 84 L 92 16 M 0 72 L 100 30 M 19 0 L 80 100" />
      <path className="route-line" d={emergency ? "M 72 69 Q 65 56 50 47 Q 42 37 28 27" : "M 25 68 Q 39 59 50 47 Q 64 39 73 27"} />
      {Array.from({ length: 14 }, (_, i) => <circle key={i} cx={(i * 19 + 8) % 100} cy={(i * 29 + 11) % 100} r=".35" fill="#547080" opacity=".6" />)}
      {junctions.map(j => <g key={j.id} transform={`translate(${j.x} ${j.y})`} onClick={() => onSelect(j.id)} className="map-node">
        <circle r={selected === j.id ? 4.1 : 3.1} className={`node-halo ${j.status.toLowerCase()}`} />
        <circle r="1.05" className="node-core" />
        <text x="0" y="-5.1" textAnchor="middle" className="node-label">{j.id}</text>
      </g>)}
    </svg>
    <div className="map-compass"><span>N</span><div className="compass-arrow">▲</div></div>
    <div className="map-legend">
      <span><i className="legend-dot normal" /> Normal</span>
      <span><i className="legend-dot warning" /> Congested</span>
      <span><i className="legend-dot critical" /> Incident</span>
    </div>
    <div className="map-weather"><CloudRain size={14}/> {weather ? "Rain · 8 mm/h" : "Clear · 22°C"} <span>·</span> Live simulation</div>
    <div className="map-scale">SCHEMATIC NETWORK · NOT A REAL CITY MAP</div>
  </div>;
}

export default function App() {
  const [running, setRunning] = useState(true);
  const [autoSignals, setAutoSignals] = useState(true);
  const [emergency, setEmergency] = useState(false);
  const [weather, setWeather] = useState(false);
  const [selectedId, setSelectedId] = useState("J-01");
  const [junctions, setJunctions] = useState(initialJunctions);
  const [chart, setChart] = useState(seedChart);
  const [activeNav, setActiveNav] = useState("Overview");
  const [toast, setToast] = useState("");
  const [clock, setClock] = useState(new Date());
  const [showSettings, setShowSettings] = useState(false);
  const [greenTime, setGreenTime] = useState(32);
  const [showAllEvents, setShowAllEvents] = useState(false);

  const selected = junctions.find(j => j.id === selectedId) || junctions[0];
  const avgWait = Math.round(junctions.reduce((sum, j) => sum + j.wait, 0) / junctions.length);
  const congestion = Math.round(junctions.reduce((sum, j) => sum + (100 - j.flow), 0) / junctions.length);
  const incidentCount = junctions.filter(j => j.status === "Incident" || j.status === "Congested").length;

  useEffect(() => {
    const timer = setInterval(() => setClock(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (!running) return;
    const timer = setInterval(() => {
      setJunctions(old => old.map(j => {
        if (!autoSignals) return j;
        const flow = Math.max(18, Math.min(97, j.flow + Math.round((Math.random() - 0.44) * (weather ? 12 : 8))));
        const wait = Math.max(12, Math.min(130, j.wait + Math.round((Math.random() - 0.58) * (weather ? 12 : 9))));
        const queue = Math.max(3, Math.min(48, j.queue + Math.round((Math.random() - 0.55) * 5)));
        let status = flow < 30 || wait > 95 ? "Incident" : flow < 48 || wait > 65 ? "Congested" : flow > 78 ? "Optimizing" : "Normal";
        if (j.id === "J-05" && emergency) status = "Priority";
        return { ...j, flow, wait, queue, status };
      }));
      setChart(old => {
        const last = old[old.length - 1];
        const next = {
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          congestion: Math.max(18, Math.min(90, Math.round(last.congestion + (Math.random() - 0.58) * 12 + (weather ? 3 : 0)))),
          throughput: Math.max(25, Math.min(95, Math.round(last.throughput + (Math.random() - 0.4) * 10 - (weather ? 4 : 0))))
        };
        return [...old.slice(-6), next];
      });
    }, 3200);
    return () => clearInterval(timer);
  }, [running, autoSignals, emergency, weather]);

  const notify = (message) => {
    setToast(message);
    setTimeout(() => setToast(""), 3000);
  };

  const navItems = [
    { name: "Overview", icon: Layers3 },
    { name: "Traffic network", icon: GitBranch },
    { name: "Incidents", icon: Siren },
    { name: "AI insights", icon: Sparkles }
  ];

  const runOptimization = () => {
    setJunctions(old => old.map(j => ({
      ...j,
      flow: Math.min(98, j.flow + (j.status === "Incident" ? 5 : 9)),
      wait: Math.max(12, j.wait - (j.status === "Incident" ? 12 : 8)),
      queue: Math.max(3, j.queue - 3),
      status: j.id === "J-05" && emergency ? "Priority" : "Optimizing"
    })));
    notify("Signal plan recalculated for 6 intersections");
  };

  const resetSimulation = () => {
    setJunctions(initialJunctions);
    setChart(seedChart);
    setEmergency(false);
    setWeather(false);
    setRunning(true);
    notify("Simulation reset to baseline");
  };

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark"><Activity size={22}/></div>
        <div><strong>citymind<span>AI</span></strong><small>URBAN INTELLIGENCE</small></div>
      </div>
      <div className="workspace-switch"><div className="workspace-icon">N</div><div><strong>Northstar City</strong><small>Simulation workspace</small></div><ChevronDown size={15}/></div>
      <div className="nav-label">OPERATIONS</div>
      <nav>{navItems.map(({name, icon: Icon}) => <button key={name} className={`nav-item ${activeNav === name ? "active" : ""}`} onClick={() => {setActiveNav(name); if (name === "Incidents") setShowAllEvents(true); else setShowAllEvents(false);}}><Icon size={17}/>{name}{name === "Incidents" && <span className="nav-count">{incidentCount}</span>}</button>)}</nav>
      <div className="nav-label systems-label">CITY SYSTEMS</div>
      <button className="nav-item" onClick={() => notify("Public transit module is on the roadmap.")}><TrainFront size={17}/>Public transit <span className="soon">SOON</span></button>
      <button className="nav-item" onClick={() => {setWeather(!weather); notify(weather ? "Weather impact disabled" : "Rain impact enabled");}}><CloudRain size={17}/>Weather impact <span className={`toggle-mini ${weather ? "on" : ""}`}/></button>
      <button className="nav-item" onClick={() => {setEmergency(!emergency); notify(emergency ? "Emergency priority disabled" : "Emergency corridor activated");}}><Siren size={17}/>Emergency response <span className={`toggle-mini ${emergency ? "on" : ""}`}/></button>
      <div className="sidebar-bottom">
        <div className="system-status"><span className="pulse-dot"/><div><strong>Simulation engine</strong><small>{running ? "Running normally" : "Paused by operator"}</small></div></div>
        <button className="profile" onClick={() => setShowSettings(!showSettings)}><div className="avatar">CC</div><div><strong>City Operator</strong><small>Administrator</small></div><Settings2 size={16}/></button>
      </div>
    </aside>

    <main className="main">
      <header className="topbar">
        <div className="breadcrumbs"><span>Northstar City</span><span className="crumb-slash">/</span><strong>{activeNav}</strong><span className="environment-pill">DEMO ENVIRONMENT</span></div>
        <div className="top-actions">
          <div className="live-indicator"><span className="pulse-dot"/>{running ? "SIMULATION LIVE" : "SIMULATION PAUSED"}</div>
          <div className="clock"><Clock3 size={15}/>{clock.toLocaleTimeString([], {hour:"2-digit", minute:"2-digit", second:"2-digit"})}</div>
          <button className="icon-button" aria-label="Notifications" onClick={() => setShowAllEvents(!showAllEvents)}><Bell size={17}/><i/></button>
          <button className="operator-avatar" onClick={() => setShowSettings(!showSettings)}>CC</button>
        </div>
      </header>

      <section className="page-heading">
        <div><div className="eyebrow"><span className="eyebrow-line"/> INTELLIGENT MOBILITY PLATFORM</div><h1>{activeNav === "Overview" ? "City operations, in sync." : activeNav}</h1><p>One connected view of your city. Decisions made smarter, streets made safer.</p></div>
        <div className="heading-actions">
          <button className="btn secondary" onClick={resetSimulation}><RotateCcw size={15}/> Reset</button>
          <button className="btn secondary" onClick={() => setRunning(!running)}>{running ? <Pause size={15}/> : <Play size={15}/>} {running ? "Pause simulation" : "Resume simulation"}</button>
          <button className="btn primary" onClick={runOptimization}><Sparkles size={15}/> Optimize signals</button>
        </div>
      </section>

      <section className="metrics-grid">
        <Metric icon={CarFront} label="Vehicles monitored" value="12,840" unit="" trend="+8.2%" tone="cyan"/>
        <Metric icon={Gauge} label="Network flow" value={`${Math.round(junctions.reduce((s,j)=>s+j.flow,0)/junctions.length)}%`} unit="" trend="+5.4%" tone="green"/>
        <Metric icon={Clock3} label="Avg. wait time" value={avgWait} unit=" sec" trend="-12.6%" tone="purple"/>
        <Metric icon={AlertTriangle} label="Active hotspots" value={incidentCount} unit="" trend={incidentCount > 2 ? "+1" : "-2"} tone="orange"/>
      </section>

      <section className="content-grid">
        <article className="panel network-panel">
          <div className="panel-header">
            <div><div className="panel-title"><span className="tiny-status"/><h2>City traffic network</h2></div><p>Intersection intelligence · Northstar district</p></div>
            <div className="panel-header-actions"><span className="mini-tag"><Radio size={12}/> LIVE DATA SIMULATION</span><button className="icon-button subtle" onClick={() => notify("Map layers refreshed")}><Layers3 size={16}/></button></div>
          </div>
          <MapView junctions={junctions} selected={selectedId} onSelect={setSelectedId} emergency={emergency} weather={weather}/>
          <div className="network-footer"><div><span className="footer-dot green-dot"/> 6 intersections connected <span className="footer-divider"/> <span className="footer-dot cyan-dot"/> 24 signal groups</div><button className="text-button" onClick={() => setActiveNav("Traffic network")}>Explore network <ArrowUpRight size={14}/></button></div>
        </article>

        <article className="panel junction-panel">
          <div className="panel-header"><div><div className="panel-title"><h2>Intersection status</h2></div><p>Live operational health</p></div><button className="text-button" onClick={() => setActiveNav("Traffic network")}>View all <ArrowUpRight size={14}/></button></div>
          <div className="junction-list">
            {junctions.map(j => <button key={j.id} onClick={() => setSelectedId(j.id)} className={`junction-row ${selectedId === j.id ? "selected" : ""}`}>
              <span className={`junction-indicator ${j.status.toLowerCase()}`}><TrafficCone size={16}/></span>
              <span className="junction-name"><strong>{j.name}</strong><small>{j.id} · {j.road}</small></span>
              <span className="junction-stat"><strong>{j.wait}s</strong><small>avg wait</small></span>
              <span className={`status-pill ${j.status.toLowerCase()}`}>{j.status}</span>
            </button>)}
          </div>
          <div className="selected-detail">
            <div className="selected-detail-head"><div><span className="eyebrow">SELECTED INTERSECTION</span><h3>{selected.name}</h3></div><span className="detail-id">{selected.id}</span></div>
            <div className="detail-stats"><div><small>Traffic flow</small><strong>{selected.flow}%</strong><div className="progress"><i style={{width:`${selected.flow}%`}}/></div></div><div><small>Queue length</small><strong>{selected.queue} <em>vehicles</em></strong><div className="progress orange"><i style={{width:`${Math.min(100, selected.queue*2)}%`}}/></div></div></div>
            <div className="phase-row"><span><Radio size={13}/> Active signal phase</span><strong>{selected.phase}</strong></div>
            <button className="btn full secondary" onClick={runOptimization}><Sparkles size={14}/> Recalculate this junction</button>
          </div>
        </article>
      </section>

      <section className="bottom-grid">
        <article className="panel chart-panel">
          <div className="panel-header"><div><div className="panel-title"><h2>Network performance</h2><span className="period-pill">LAST 70 MIN</span></div><p>Congestion index vs. vehicle throughput</p></div><button className="icon-button subtle" onClick={() => notify("Chart uses simulated demo metrics")}><Settings2 size={16}/></button></div>
          <div className="chart-legend"><span><i className="legend-line blue"/> Congestion index</span><span><i className="legend-line green-line"/> Throughput</span></div>
          <div className="chart-wrap"><ResponsiveContainer width="100%" height="100%"><AreaChart data={chart} margin={{top:8,right:10,left:-20,bottom:0}}><defs><linearGradient id="blueFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#4c9fff" stopOpacity={0.23}/><stop offset="100%" stopColor="#4c9fff" stopOpacity={0}/></linearGradient><linearGradient id="greenFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#35d6a1" stopOpacity={0.14}/><stop offset="100%" stopColor="#35d6a1" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#1d2b3c" strokeDasharray="3 5" vertical={false}/><XAxis dataKey="time" tick={{fill:"#73859b",fontSize:10}} axisLine={false} tickLine={false}/><YAxis tick={{fill:"#73859b",fontSize:10}} axisLine={false} tickLine={false}/><Tooltip contentStyle={{background:"#101d2b",border:"1px solid #27384b",borderRadius:10,color:"#e9f1fb"}}/><Area type="monotone" dataKey="congestion" name="Congestion" stroke="#5aa8ff" strokeWidth={2} fill="url(#blueFill)"/><Area type="monotone" dataKey="throughput" name="Throughput" stroke="#35d6a1" strokeWidth={2} fill="url(#greenFill)"/></AreaChart></ResponsiveContainer></div>
          <div className="chart-summary"><div><span className="summary-dot blue-dot"/> Current congestion <strong>{chart[chart.length-1].congestion}/100</strong></div><div><span className="summary-dot green-dot"/> Throughput index <strong>{chart[chart.length-1].throughput}/100</strong></div></div>
        </article>

        <article className="panel insights-panel">
          <div className="panel-header"><div><div className="panel-title"><Sparkles size={17} className="ai-spark"/><h2>CityMind recommendations</h2></div><p>Actionable insights from the demo engine</p></div><span className="ai-chip">AI LAYER</span></div>
          <div className="insight-card priority"><div className="insight-icon"><Zap size={16}/></div><div><div className="insight-top"><strong>{emergency ? "Emergency corridor active" : "Rebalance South Transit"}</strong><span className="priority-label">HIGH IMPACT</span></div><p>{emergency ? "Signal priority is enabled for the simulated emergency route." : "Extend the northbound green phase by 12 seconds to reduce the current queue."}</p><button className="text-button" onClick={() => {setEmergency(true); runOptimization();}}>Apply recommendation <ArrowUpRight size={13}/></button></div></div>
          <div className="insight-card"><div className="insight-icon green"><ShieldCheck size={16}/></div><div><div className="insight-top"><strong>Protect school-zone flow</strong><span className="confidence">92% confidence</span></div><p>Keep pedestrian crossing windows unchanged during peak traffic.</p><button className="text-button" onClick={() => notify("School-zone policy added to demo queue")}>Review policy <ArrowUpRight size={13}/></button></div></div>
          <div className="insight-note"><Bot size={16}/><span>Recommendations are generated from a <strong>local demo simulation</strong>, not real sensors or a trained AI model.</span></div>
        </article>
      </section>

      <section className="panel events-panel">
        <div className="panel-header"><div><div className="panel-title"><h2>Recent events</h2><span className="event-count">{events.length}</span></div><p>Signals and incidents across your network</p></div><button className="text-button" onClick={() => setShowAllEvents(!showAllEvents)}>{showAllEvents ? "Show less" : "View event log"} <ArrowUpRight size={14}/></button></div>
        <div className="events-list">{(showAllEvents ? [...events, {type:"info",title:"Weather model updated",detail:"Rain scenario available for all intersections",time:"12 min ago"}, {type:"success",title:"Network connection verified",detail:"All six simulated intersections responding",time:"18 min ago"}] : events).map((e,i)=><div className="event-row" key={i}><span className={`event-icon ${e.type}`}>{e.type==="critical"?<AlertTriangle size={15}/>:e.type==="success"?<Check size={15}/>:<Activity size={15}/>}</span><div className="event-copy"><strong>{e.title}</strong><span>{e.detail}</span></div><time>{e.time}</time></div>)}</div>
      </section>

      <footer className="app-footer"><span>© 2026 CityMind AI <span className="footer-divider"/> Urban operations prototype</span><span><span className="pulse-dot"/> All systems nominal <span className="footer-divider"/> Build 0.1.0</span></footer>
    </main>

    {showSettings && <div className="settings-popover panel"><div className="panel-title"><Settings2 size={17}/><h2>Simulation settings</h2></div><p>Adjust the local demo model.</p><label className="setting-line"><span>Adaptive signal timing</span><button className={`switch ${autoSignals ? "on" : ""}`} onClick={() => setAutoSignals(!autoSignals)}><i/></button></label><label className="setting-line"><span>Target green phase</span><strong>{greenTime}s</strong></label><input type="range" min="15" max="60" value={greenTime} onChange={e=>setGreenTime(Number(e.target.value))}/><button className="btn primary full" onClick={()=>{setShowSettings(false);notify(`Demo green phase set to ${greenTime}s`)}}>Save settings</button></div>}
    {toast && <div className="toast"><Check size={16}/>{toast}</div>}
  </div>;
}''',
"src/styles.css": r'''@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{font-family:'DM Sans',sans-serif;color:#e8eff8;background:#07111f;font-synthesis:none;text-rendering:optimizeLegibility;font-smooth:always;--bg:#07111f;--panel:#0c1725;--line:#1b2a3b;--muted:#8090a4;--cyan:#63b7ff;--green:#37d7a1;--orange:#ffb56b}
*{box-sizing:border-box}body{margin:0;min-width:320px;background:radial-gradient(ellipse at 70% -20%,#122b44 0,transparent 45%),#07111f}button{font:inherit;cursor:pointer;color:inherit}.app-shell{min-height:100vh}.sidebar{width:246px;position:fixed;inset:0 auto 0 0;background:#091421;border-right:1px solid #1a2939;padding:25px 15px 14px;display:flex;flex-direction:column;z-index:5}.brand{display:flex;align-items:center;gap:11px;padding:0 10px 28px}.brand-mark{width:39px;height:39px;display:grid;place-items:center;color:#081522;background:linear-gradient(135deg,#7ad7ff,#46a5ff);border-radius:12px;box-shadow:0 0 25px #3b9dff26}.brand strong{display:block;font:800 20px Manrope;letter-spacing:-.8px}.brand strong span{color:#63b7ff}.brand small{display:block;color:#6e8094;font:500 8px 'DM Mono';letter-spacing:1.3px;margin-top:2px}.workspace-switch{display:flex;align-items:center;gap:9px;background:#101e2d;border:1px solid #203144;padding:10px;border-radius:10px;margin-bottom:30px}.workspace-icon{width:28px;height:28px;border-radius:8px;display:grid;place-items:center;background:#214e62;color:#a8e4ff;font-weight:800}.workspace-switch div:nth-child(2){flex:1;min-width:0}.workspace-switch strong,.profile strong{display:block;font-size:11px}.workspace-switch small,.profile small{display:block;color:#8292a6;font-size:10px;margin-top:3px}.workspace-switch>svg{color:#778ba1}.nav-label{font:500 9px 'DM Mono';letter-spacing:1.4px;color:#63778d;padding:0 11px;margin-bottom:9px}.sidebar nav{display:grid;gap:4px}.nav-item{width:100%;border:1px solid transparent;background:transparent;color:#92a2b5;border-radius:8px;display:flex;align-items:center;gap:12px;padding:11px 12px;text-align:left;font-size:12px;transition:.18s}.nav-item:hover{background:#112235;color:#eaf4ff}.nav-item.active{background:linear-gradient(90deg,#17354b,#12273a);border-color:#23445d;color:#bce7ff;box-shadow:inset 2px 0 #64c4ff}.nav-count{margin-left:auto;border-radius:5px;background:#4d2b27;color:#ffb7a0;font:11px 'DM Mono';padding:3px 6px}.systems-label{margin-top:30px}.soon{margin-left:auto;font:9px 'DM Mono';color:#6c7d91}.toggle-mini{margin-left:auto;width:23px;height:13px;border-radius:20px;background:#263547;position:relative}.toggle-mini:after{content:'';position:absolute;left:2px;top:2px;width:9px;height:9px;background:#8596a9;border-radius:50%;transition:.2s}.toggle-mini.on{background:#1d775e}.toggle-mini.on:after{left:12px;background:#8af1cc}.sidebar-bottom{margin-top:auto}.system-status{display:flex;align-items:center;gap:10px;padding:14px 10px;border-top:1px solid #1a2939;border-bottom:1px solid #1a2939;margin-bottom:13px}.system-status strong{display:block;font-size:10px}.system-status small{display:block;font-size:10px;color:#8192a5;margin-top:4px}.pulse-dot{display:inline-block;width:7px;height:7px;background:#35d6a1;border-radius:50%;box-shadow:0 0 0 4px #35d6a117;flex-shrink:0}.profile{display:flex;align-items:center;gap:9px;width:100%;background:none;border:0;text-align:left;padding:5px 7px}.profile>div:nth-child(2){flex:1}.avatar,.operator-avatar{display:grid;place-items:center;width:31px;height:31px;border-radius:50%;background:#24445b;color:#bce8ff;font-size:10px;font-weight:700;border:1px solid #3d6883}.profile>svg{color:#73879d}.main{margin-left:246px;padding:0 31px 22px;max-width:1900px}.topbar{height:67px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #18283a}.breadcrumbs,.top-actions{display:flex;align-items:center;gap:12px;font-size:11px;color:#8b9db1}.breadcrumbs strong{color:#e4edf8;font-weight:600}.crumb-slash{color:#41536a}.environment-pill,.mini-tag,.period-pill{font:9px 'DM Mono';letter-spacing:.5px;color:#89a0b7;background:#142235;border:1px solid #24364b;border-radius:5px;padding:5px 7px}.environment-pill{margin-left:7px;color:#80caff;background:#102a3b;border-color:#1e435a}.top-actions{gap:18px}.live-indicator{font:9px 'DM Mono';color:#6fe0b5;display:flex;align-items:center;gap:8px}.live-indicator .pulse-dot{width:6px;height:6px}.clock{display:flex;align-items:center;gap:6px;font:10px 'DM Mono';color:#a2b1c2}.icon-button{position:relative;border:1px solid #26364a;background:#0e1b2a;color:#9caec1;width:33px;height:33px;border-radius:8px;display:grid;place-items:center}.icon-button i{position:absolute;width:5px;height:5px;background:#ff8c76;border-radius:50%;right:7px;top:6px}.icon-button.subtle{width:30px;height:30px;background:transparent;border-color:#243348}.operator-avatar{cursor:pointer}.page-heading{display:flex;justify-content:space-between;align-items:flex-end;padding:28px 0 23px;gap:20px}.eyebrow{display:flex;align-items:center;gap:8px;font:9px 'DM Mono';letter-spacing:1.4px;color:#79bde9}.eyebrow-line{width:19px;height:1px;background:#4aa9e9}.page-heading h1{font:700 clamp(25px,2.5vw,34px) Manrope;letter-spacing:-1.4px;margin:10px 0 6px;color:#f2f7ff}.page-heading p,.panel-header p{margin:0;color:#8394a9;font-size:11px}.heading-actions{display:flex;gap:8px;flex-wrap:wrap}.btn{border:1px solid #293b50;background:#122235;border-radius:7px;padding:10px 12px;font-size:10px;font-weight:600;display:inline-flex;align-items:center;justify-content:center;gap:7px;white-space:nowrap;transition:.18s}.btn:hover{filter:brightness(1.15);transform:translateY(-1px)}.btn.secondary{background:#101d2c;color:#bac9d9}.btn.primary{background:linear-gradient(120deg,#54b6fa,#3e94e7);color:#071522;border-color:#67bcf7;box-shadow:0 5px 20px #319ce522}.btn.full{width:100%;margin-top:13px}.metrics-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin-bottom:16px}.panel,.metric{background:linear-gradient(145deg,#0e1a29,#0b1623);border:1px solid #1c2c3f;border-radius:11px;box-shadow:0 8px 25px #0000000b}.metric{display:flex;align-items:center;gap:12px;padding:16px;min-width:0;position:relative;overflow:hidden}.metric:after{content:'';position:absolute;right:-30px;top:-45px;width:90px;height:90px;border-radius:50%;background:#ffffff04}.metric-icon{width:36px;height:36px;display:grid;place-items:center;border-radius:9px;flex-shrink:0}.metric-icon.cyan{background:#12334b;color:#69c5ff}.metric-icon.green{background:#12382f;color:#4fe0ae}.metric-icon.purple{background:#2b2345;color:#b9a2ff}.metric-icon.orange{background:#3b2b20;color:#ffb66c}.metric-copy{min-width:0;flex:1}.metric-copy>span{font-size:10px;color:#8798ac;white-space:nowrap}.metric-value{font:700 24px Manrope;letter-spacing:-.8px;margin-top:3px;color:#edf5ff}.metric-value small{font:500 11px 'DM Sans';letter-spacing:0;color:#91a1b3}.trend{display:flex;align-items:center;gap:2px;font:10px 'DM Mono';white-space:nowrap}.trend.down{color:#5fe0ad}.trend.up{color:#ffab92}.content-grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(350px,1fr);gap:15px;margin-bottom:15px}.panel-header{padding:17px 18px 14px;display:flex;justify-content:space-between;align-items:flex-start;gap:10px}.panel-title{display:flex;align-items:center;gap:9px}.panel-title h2{font:650 13px Manrope;letter-spacing:-.2px;margin:0;color:#e8f1fc}.panel-header p{margin-top:6px;font-size:10px}.tiny-status{width:7px;height:7px;background:#4fc6a0;border-radius:50%;box-shadow:0 0 0 4px #4fc6a015}.panel-header-actions{display:flex;align-items:center;gap:9px}.mini-tag{display:flex;align-items:center;gap:5px;font-size:8px;color:#67d6b1;background:#103025;border-color:#205240;white-space:nowrap}.map-stage{height:342px;position:relative;overflow:hidden;background-color:#0a1c2a;background-image:linear-gradient(#19304465 1px,transparent 1px),linear-gradient(90deg,#19304465 1px,transparent 1px);background-size:25px 25px;border-top:1px solid #182a3c;border-bottom:1px solid #182a3c}.map-grid{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,#102b3a88,transparent 65%)}.roads{position:absolute;inset:0;width:100%;height:100%;overflow:visible}.road-main{fill:none;stroke:#263a4b;stroke-width:4.8;stroke-linecap:round}.road-center{fill:none;stroke:#718393;stroke-width:.25;stroke-dasharray:1.2 1.5;opacity:.55}.route-line{fill:none;stroke:#4bb8f4;stroke-width:.6;stroke-dasharray:1.5 1;filter:drop-shadow(0 0 2px #4bb8f4);opacity:.85}.map-node{cursor:pointer}.node-halo{fill:#4fe0b0;fill-opacity:.16;stroke:#4fe0b0;stroke-width:.45;transition:r .2s}.node-halo.congested{fill:#ffb25f;stroke:#ffb25f}.node-halo.incident{fill:#ff7f78;stroke:#ff7f78}.node-halo.priority{fill:#61b9ff;stroke:#61b9ff}.node-halo.optimizing{fill:#64c3ff;stroke:#64c3ff}.node-core{fill:#c9f8ed;stroke:#102d3b;stroke-width:.5}.node-label{fill:#d6e7f5;font:2.7px 'DM Mono';paint-order:stroke;stroke:#071522;stroke-width:.7px}.map-compass{position:absolute;right:17px;top:15px;display:flex;flex-direction:column;align-items:center;color:#91a9bd;font:9px 'DM Mono';gap:2px}.compass-arrow{color:#62c6ff;font-size:16px}.map-legend{position:absolute;left:15px;top:15px;display:flex;gap:10px;background:#091725d9;border:1px solid #26384b;border-radius:6px;padding:8px 9px;font-size:9px;color:#9aadc0}.map-legend span{display:flex;align-items:center;gap:5px}.legend-dot{width:6px;height:6px;border-radius:50%;display:inline-block}.legend-dot.normal{background:#4fe0b0}.legend-dot.warning{background:#ffb25f}.legend-dot.critical{background:#ff7f78}.map-weather{position:absolute;right:15px;bottom:15px;background:#091725dd;border:1px solid #26384b;border-radius:6px;padding:8px 9px;display:flex;align-items:center;gap:7px;font-size:9px;color:#a8bbcd}.map-weather svg{color:#70c8ff}.map-scale{position:absolute;left:15px;bottom:16px;font:8px 'DM Mono';color:#5d7890;letter-spacing:.5px}.network-footer{display:flex;justify-content:space-between;align-items:center;padding:12px 17px;color:#8fa1b4;font-size:9px;gap:10px}.network-footer>div{display:flex;align-items:center;gap:7px;flex-wrap:wrap}.footer-dot{width:6px;height:6px;border-radius:50%;display:inline-block}.green-dot{background:#43d7a2}.cyan-dot{background:#58b8ff}.footer-divider{width:1px;height:12px;background:#2b3c4e;display:inline-block;margin:0 5px;vertical-align:middle}.text-button{display:inline-flex;align-items:center;gap:5px;background:transparent;border:0;padding:0;color:#73c6ff;font-size:10px;font-weight:600;white-space:nowrap}.text-button:hover{color:#b3e5ff}.junction-panel{overflow:hidden}.junction-list{padding:0 9px}.junction-row{width:100%;display:flex;align-items:center;gap:9px;text-align:left;padding:10px 8px;background:transparent;border:1px solid transparent;border-radius:7px;transition:.15s}.junction-row:hover,.junction-row.selected{background:#142538;border-color:#263c51}.junction-indicator{width:28px;height:28px;border-radius:7px;background:#13382f;color:#58dfad;display:grid;place-items:center;flex-shrink:0}.junction-indicator.congested{background:#3c2d1e;color:#ffb866}.junction-indicator.incident{background:#422725;color:#ff8b83}.junction-indicator.optimizing{background:#14324a;color:#67c4ff}.junction-indicator.priority{background:#173858;color:#7ac8ff}.junction-name{flex:1;min-width:0}.junction-name strong{display:block;font-size:10px;font-weight:600;color:#dce7f3}.junction-name small{display:block;margin-top:4px;font-size:8px;color:#7c90a5;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:155px}.junction-stat{text-align:right;min-width:38px}.junction-stat strong{display:block;font:11px 'DM Mono';color:#dce9f5}.junction-stat small{display:block;font-size:8px;color:#758ba0;margin-top:3px}.status-pill{font-size:8px;padding:4px 6px;border-radius:4px;background:#18382f;color:#6ce0b5;white-space:nowrap}.status-pill.congested{background:#3c2d1e;color:#ffbe78}.status-pill.incident{background:#422725;color:#ff9991}.status-pill.optimizing{background:#14334b;color:#7bcaff}.status-pill.priority{background:#173858;color:#7ac8ff}.selected-detail{border-top:1px solid #1d2d40;margin-top:8px;padding:14px 17px 16px;background:#0b1623}.selected-detail-head{display:flex;justify-content:space-between;align-items:flex-start}.selected-detail-head .eyebrow{font-size:8px;color:#7c91a8;letter-spacing:1px}.selected-detail h3{font:650 14px Manrope;margin:5px 0 0}.detail-id{font:10px 'DM Mono';color:#79c6ff;border:1px solid #24445b;background:#102a3d;padding:4px 6px;border-radius:4px}.detail-stats{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:17px}.detail-stats small{display:block;font-size:9px;color:#8598ac}.detail-stats strong{display:block;font:650 17px Manrope;margin:5px 0 8px}.detail-stats em{font:9px 'DM Sans';color:#8295a9;font-style:normal}.progress{height:4px;background:#1c2c3d;border-radius:5px;overflow:hidden}.progress i{display:block;height:100%;background:#4fb5ff;border-radius:5px;transition:width .4s}.progress.orange i{background:#ffb66b}.phase-row{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:15px;font-size:9px;color:#8296aa}.phase-row span{display:flex;align-items:center;gap:6px}.phase-row svg{color:#5abaff}.phase-row strong{font-weight:500;color:#b8c9d8}.bottom-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(350px,1fr);gap:15px;margin-bottom:15px}.period-pill{font-size:8px;padding:4px 6px}.chart-legend{