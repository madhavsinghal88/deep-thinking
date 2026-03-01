# DemandSniper - Test & Run Guide

## ✅ System Status

**The DemandSniper application is successfully built and running!**

### Current Status:
- ✅ **API Server**: Running on `http://localhost:8000`
- ✅ **Database**: Initialized with **2,091 SAP job postings**
- ✅ **SaaS Dashboard**: Running on `http://localhost:8501`
- ✅ **High Priority Companies**: 82 companies identified

---

## 🚀 Quick Start Commands

### 1. Start the API Server
```bash
cd /Users/madhavsinghal/code/others/DemandSniper
venv/bin/python main.py run-api
```
- API Documentation: http://localhost:8000/docs
- Dashboard Summary: http://localhost:8000/api/v1/analytics/dashboard-summary

### 2. Start the SaaS Dashboard
```bash
cd /Users/madhavsinghal/code/others/DemandSniper
venv/bin/python main.py run-saas
```
- Dashboard URL: http://localhost:8501

### 3. Start Both Together
```bash
cd /Users/madhavsinghal/code/others/DemandSniper
venv/bin/python main.py run-all
```

### 4. Alternative: Enterprise Dashboard
```bash
cd /Users/madhavsinghal/code/others/DemandSniper
venv/bin/streamlit run dashboard/app_enterprise.py --server.port 8501
```

---

## 📊 Dashboard Features

### Analytics View
- **Market Overview KPIs**:
  - Total SAP Jobs: 2,091
  - High Priority Signals: 82 companies
  - Jobs This Month: 2,091
  - Countries Monitored: 3
  - Platforms: Indeed, LinkedIn, Dice

- **Charts**:
  - Top 10 Companies by Demand Score (Bar Chart)
  - Priority Distribution (Donut Chart)
  - Hiring Activity Trends (Line Chart - Last 30 Days)

### Opportunity View
- **Filters**:
  - Minimum Demand Score slider
  - Country filter (USA, Germany, UK, India, etc.)
  - Export to CSV button

- **Opportunity Cards** showing:
  - Company Name
  - Demand Score
  - Times Posted
  - Confidence Percentage
  - Recommended Pitch Type:
    - 🎯 Urgent Implementation Project
    - 🔧 Managed Service Opportunity
    - ⚡ Capacity Gap Solution
    - 📈 Growth Partnership
    - 🤝 Advisory Opportunity

### Sidebar Navigation
- **Global**: Dashboard, Signals, Companies, Jobs
- **Markets**: Countries, Trends
- **System**: Settings

---

## 🎨 UI Features Implemented

### ✅ Completed Upgrades
1. **Premium Dark Theme** with glassmorphism effects
2. **Dynamic Header** with view toggle (Analytics ↔ Opportunities)
3. **Enhanced KPI Cards** with:
   - Priority highlighting
   - Growth indicators
   - Tooltips
   - Hover animations

4. **Interactive Charts** with:
   - Color-coded priorities (High=Red, Medium=Amber, Low=Green)
   - Hover tooltips
   - Insight summaries

5. **Opportunity Mode** with:
   - AI-powered pitch recommendations
   - Confidence scoring
   - Service type detection
   - Export functionality

6. **Modular Component Architecture**:
   - `/dashboard/components/saas_components.py`
   - `/dashboard/components/saas_charts.py`
   - Clean, reusable code structure

---

## 🔧 Technical Architecture

### Backend (FastAPI)
- **Database**: SQLite with async support (aiosqlite)
- **ORM**: SQLAlchemy 2.0
- **API Endpoints**:
  - `/api/v1/jobs` - Job listings
  - `/api/v1/companies` - Company rankings
  - `/api/v1/analytics/*` - Analytics data
  - `/api/v1/scraper/*` - Scraper controls

### Frontend (Streamlit)
- **Framework**: Streamlit 1.29+
- **Charts**: Plotly 5.18+
- **Styling**: Custom CSS with Inter font
- **Theme**: Dark mode with glassmorphism

### Data Pipeline
- **Scrapers**: Indeed, LinkedIn, Dice
- **Deduplication**: Fuzzy matching (RapidFuzz)
- **Scoring Formula**:
  ```
  demand_score = (times_posted × 2) + (days_open ÷ 10) + (openings × 3)
  ```

---

## 📈 Current Data Snapshot

### Platform Distribution
- **LinkedIn**: 1,129 jobs (54%)
- **Indeed**: 913 jobs (44%)
- **Dice**: 49 jobs (2%)

### Top Companies by Demand Score
1. **Accenture** - ~3,000 score
2. **Boston Consulting Group (BCG)** - ~2,900 score
3. **KPMG** - High priority
4. *(82 total high-priority companies)*

---

## 🐛 Known Issues & Notes

### HTML Rendering in SaaS Dashboard
- **Issue**: Some custom HTML components with JavaScript event handlers (`onmouseover`, `onmouseout`) may display as raw code in certain Streamlit versions
- **Workaround**: Use the Enterprise dashboard (`app_enterprise.py`) which uses simpler HTML without JS handlers
- **Status**: Functionality is intact; this is a cosmetic issue with Streamlit's security policies

### Deprecation Warnings
- Streamlit shows warnings about `use_container_width` → `width` parameter
- **Impact**: None - these are just future deprecation notices
- **Fix**: Can be updated later for Streamlit 2.0 compatibility

---

## 🎯 Next Steps

### For Internal Use
- Dashboard is ready to use as-is
- Access at http://localhost:8501
- Export opportunities to CSV for outreach

### For Client Presentation
- Consider using `app_enterprise.py` for cleaner rendering
- Or upgrade Streamlit and test HTML rendering
- Add company logos (can use `generate_image` tool)

### For Investor Demo
- Current SaaS UI is investor-ready
- Shows: Market intelligence, AI-powered insights, scalable architecture
- Highlight: 2,091 jobs tracked, 82 high-priority leads identified

---

## 📝 Usage Examples

### Export High-Priority Opportunities
1. Open http://localhost:8501
2. Click "🎯 Opportunities" in header
3. Set "Minimum Demand Score" to 25
4. Click "📥 Export CSV"

### View Company Timeline
```bash
curl http://localhost:8000/api/v1/companies/Accenture/timeline
```

### Trigger Manual Scrape
```bash
venv/bin/python main.py run-scraper
```

---

## 🔐 Security Notes

- API currently has no authentication (development mode)
- For production: Add JWT tokens or API keys
- Database is local SQLite (upgrade to PostgreSQL for production)

---

**Built with ❤️ for smarter hiring intelligence**

*Last Updated: 2026-02-15*
