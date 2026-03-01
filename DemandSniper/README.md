# DemandSniper

A configurable hiring-demand intelligence tool for detecting companies with ongoing hiring demand, signaling potential outsourcing or service opportunities.

## Features

- **Multi-Platform Scraping**: Supports Indeed, Dice, LinkedIn (extensible to others)
- **Demand Detection**: Automatically identifies reposted jobs within 60-day windows
- **Intelligent Scoring**: Configurable demand score formula based on repost frequency, days open, and number of openings
- **Priority Classification**: Auto-tags companies as High/Medium/Low priority based on demand scores
- **Streamlit Dashboard**: Interactive visualizations with filtering, charts, and manual entry
- **FastAPI Backend**: RESTful API for programmatic access
- **Notifications**: Email and webhook alerts for high-priority opportunities
- **Company Enrichment**: Profile data for better opportunity assessment
- **Export Functionality**: CSV exports for reporting and analysis

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy (async SQLite)
- **Frontend**: Streamlit, Plotly
- **Scraping**: Playwright, BeautifulSoup, httpx
- **Scheduling**: APScheduler
- **Data**: Pandas, RapidFuzz (fuzzy matching)

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd DemandSniper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (if using Playwright scrapers)
playwright install
```

### Configuration

Edit the configuration files in the `config/` directory:

**`config/search_config.yaml`** - Search parameters:
```yaml
target_country: "United States"
skill_keywords:
  - "Python"
  - "FastAPI"
  - "React"
job_title_keywords:
  - "Software Engineer"
  - "Backend Developer"
platforms:
  - "indeed"
  - "dice"
  - "linkedin"
search_frequency: "daily"
```

**`config/scoring_config.yaml`** - Scoring and notifications:
```yaml
demand_score_formula:
  times_posted_weight: 2
  days_open_divisor: 10
  openings_weight: 3

priority_thresholds:
  high: 25
  medium: 10

notifications:
  enabled: true
  webhook:
    url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Running the Application

```bash
# Option 1: Start everything (API + Dashboard)
python main.py run-all

# Option 2: Start components separately
# Terminal 1 - API Server:
python main.py run-api

# Terminal 2 - Dashboard:
python main.py run-dashboard

# Terminal 3 - Manual Scrape:
python main.py run-scraper
```

### Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

## Project Structure

```
DemandSniper/
├── config/                 # Configuration files
│   ├── search_config.yaml
│   ├── scoring_config.yaml
│   └── settings.py
├── scraper/               # Scraping framework
│   ├── base.py           # Abstract scraper class
│   ├── indeed.py
│   ├── dice.py
│   ├── linkedin.py
│   ├── scheduler.py      # APScheduler integration
│   └── utils.py
├── database/              # Database layer
│   ├── models.py         # SQLAlchemy models
│   ├── crud.py           # CRUD operations
│   └── connection.py
├── api/                   # FastAPI backend
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│       ├── jobs.py
│       ├── companies.py
│       ├── analytics.py
│       ├── config.py
│       └── scraper.py
├── dashboard/             # Streamlit dashboard
│   ├── app.py
│   └── components/
│       ├── filters.py
│       ├── charts.py
│       ├── tables.py
│       └── forms.py
├── utils/                 # Utilities
│   ├── demand_scoring.py
│   ├── deduplication.py
│   ├── notifications.py
│   ├── enrichment.py
│   └── export.py
├── main.py               # Entry point
├── requirements.txt
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/jobs` | GET | List jobs with filters |
| `/api/v1/jobs` | POST | Create new job |
| `/api/v1/jobs/{id}` | GET | Get job details |
| `/api/v1/companies` | GET | List companies by demand |
| `/api/v1/companies/{name}` | GET | Company details |
| `/api/v1/companies/{name}/timeline` | GET | Company event timeline |
| `/api/v1/analytics/top-companies` | GET | Top companies by demand |
| `/api/v1/analytics/hiring-trends` | GET | Hiring trends over time |
| `/api/v1/analytics/export/jobs` | GET | Export jobs to CSV |
| `/api/v1/scraper/run` | POST | Trigger manual scrape |
| `/api/v1/scraper/status` | GET | Get scraper status |
| `/api/v1/config/search` | GET/PUT | Search configuration |
| `/api/v1/config/scoring` | GET/PUT | Scoring configuration |

## Demand Score Formula

The demand score is calculated as:

```
demand_score = (times_posted × times_posted_weight)
              + (days_open ÷ days_open_divisor)
              + (number_of_openings × openings_weight)
```

**Default Values:**
- `times_posted_weight`: 2
- `days_open_divisor`: 10
- `openings_weight`: 3

**Priority Thresholds:**
- High: > 25
- Medium: 10-25
- Low: < 10

## Scaling for Production

### Database
- **Current**: SQLite (single-file, good for development)
- **Production**: PostgreSQL with asyncpg
- **Migration**: Use Alembic for schema migrations

### Caching
- Add Redis for caching frequently accessed data
- Cache company profiles and demand score calculations

### Task Queue
- Replace APScheduler with Celery + Redis/RabbitMQ
- Distribute scraping across multiple workers
- Handle rate limiting more gracefully

### Deployment
- **Docker**: Containerize the application
- **Orchestration**: Kubernetes for scaling
- **Reverse Proxy**: Nginx for API and dashboard
- **Monitoring**: Prometheus + Grafana

### Security
- Add API authentication (JWT or API keys)
- Rate limiting on endpoints
- Input validation and sanitization
- HTTPS in production

## Environment Variables

Create a `.env` file:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///data/demandsniper.db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Email Notifications (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=alerts@demandsniper.com

# External APIs (optional)
CLEARBIT_API_KEY=your-clearbit-api-key
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Roadmap

- [ ] Real-time scraping with WebSocket updates
- [ ] Machine learning for demand prediction
- [ ] Integration with CRM systems (Salesforce, HubSpot)
- [ ] Multi-country support with location mapping
- [ ] Mobile app for on-the-go monitoring
- [ ] Advanced analytics and forecasting
- [ ] API rate limiting and quotas
- [ ] SaaS deployment templates

---

Built with ❤️ for smarter hiring intelligence.
