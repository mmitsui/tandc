# ToS Clarity

**Understand what you're agreeing to — before you click "I Accept"**

ToS Clarity is a tool that crawls, analyzes, and summarizes Terms of Service and Privacy Policy documents, helping users make informed decisions about the platforms they sign up for.

---

## Vision

Every day, billions of people click "I Accept" on terms they've never read. These documents are intentionally long, complex, and filled with legal jargon. ToS Clarity changes that by providing clear, actionable summaries that answer two critical questions:

1. **What rules must I follow?** (Content policies, usage restrictions, account requirements)
2. **What am I giving up?** (Data collection, rights to content, arbitration clauses, liability waivers)

---

## Product Overview

### Primary Interface: Chrome Extension
The Chrome extension activates automatically when users visit signup pages or ToS/Privacy Policy links, providing instant summaries without leaving the page.

### Secondary Interface: Web Portal
A standalone web application for users who prefer not to install extensions, want to compare multiple services, or need shareable reports.

---

## Core Features (MVP - v1.0)

### 1. ToS Document Detection & Extraction
- Automatically detect Terms of Service and Privacy Policy pages
- Handle multiple document formats (HTML, PDF, embedded iframes)
- Support for dynamically loaded content (SPAs, lazy loading)
- Manual URL input as fallback

### 2. AI-Powered Analysis
- Extract and categorize key provisions into standardized sections
- Identify concerning clauses (broad data sharing, arbitration requirements, content ownership transfers)
- Generate plain-English summaries at multiple reading levels
- Highlight changes from previous versions (when available)

### 3. Summary Output Format
Each summary includes:

```
┌─────────────────────────────────────────────────────────────┐
│  ToS Clarity Summary: [Service Name]                        │
│  Last Updated: [Date] | Reading Time: [X min] → [Y sec]     │
├─────────────────────────────────────────────────────────────┤
│  ⚠️  ATTENTION REQUIRED (Red Flags)                         │
│  • [Critical items that users should carefully consider]    │
├─────────────────────────────────────────────────────────────┤
│  📋 RULES YOU MUST FOLLOW                                   │
│  • Content restrictions                                     │
│  • Account requirements                                     │
│  • Prohibited activities                                    │
├─────────────────────────────────────────────────────────────┤
│  🔓 WHAT YOU'RE GIVING UP                                   │
│  • Data collected                                           │
│  • How data is shared                                       │
│  • Rights to your content                                   │
│  • Legal rights waived                                      │
├─────────────────────────────────────────────────────────────┤
│  📊 CLARITY SCORE: [X/100]                                  │
│  Based on readability, fairness, and transparency           │
└─────────────────────────────────────────────────────────────┘
```

### 4. Supported Platforms (v1.0)
- YouTube (Terms of Service + Privacy Policy)
- OpenAI (Terms of Use + Privacy Policy + Usage Policies)

---

## Technical Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                   │
├────────────────────────────────┬────────────────────────────────────────┤
│     Chrome Extension           │           Web Portal                    │
│  ┌──────────────────────┐     │     ┌──────────────────────┐           │
│  │ Content Script       │     │     │ Next.js Frontend     │           │
│  │ (Page Detection)     │     │     │ (React + Tailwind)   │           │
│  ├──────────────────────┤     │     ├──────────────────────┤           │
│  │ Popup UI             │     │     │ URL Input            │           │
│  │ (Summary Display)    │     │     │ History Dashboard    │           │
│  ├──────────────────────┤     │     │ Compare View         │           │
│  │ Background Worker    │     │     └──────────────────────┘           │
│  │ (API Communication)  │     │                                         │
│  └──────────────────────┘     │                                         │
└────────────────────────────────┴────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           API LAYER                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Backend (Python)                      │   │
│  ├─────────────────────────────────────────────────────────────────┤   │
│  │  /api/analyze          - Submit URL for analysis                 │   │
│  │  /api/summary/{id}     - Retrieve cached summary                 │   │
│  │  /api/compare          - Compare multiple services               │   │
│  │  /api/history          - User's analysis history                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         SERVICE LAYER                                    │
├─────────────────────────┬─────────────────────────┬─────────────────────┤
│   Document Extraction   │    AI Analysis Engine   │   Caching Layer     │
│  ┌───────────────────┐ │  ┌───────────────────┐  │ ┌─────────────────┐ │
│  │ Playwright        │ │  │ Claude API        │  │ │ Redis           │ │
│  │ (Dynamic content) │ │  │ (Summarization)   │  │ │ (Rate limiting) │ │
│  ├───────────────────┤ │  ├───────────────────┤  │ ├─────────────────┤ │
│  │ BeautifulSoup     │ │  │ Prompt Templates  │  │ │ PostgreSQL      │ │
│  │ (HTML parsing)    │ │  │ (Structured out)  │  │ │ (Summaries)     │ │
│  ├───────────────────┤ │  ├───────────────────┤  │ └─────────────────┘ │
│  │ PyMuPDF           │ │  │ Diff Engine       │  │                     │
│  │ (PDF extraction)  │ │  │ (Version compare) │  │                     │
│  └───────────────────┘ │  └───────────────────┘  │                     │
└─────────────────────────┴─────────────────────────┴─────────────────────┘
```

### Tech Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Chrome Extension** | TypeScript + React | Type safety, component reuse with web portal |
| **Web Portal** | Next.js 14 (App Router) | SSR for SEO, API routes, React ecosystem |
| **Backend API** | FastAPI (Python) | Async support, automatic OpenAPI docs, Python AI ecosystem |
| **AI Provider** | Anthropic Claude API | Strong reasoning, long context window (200K tokens handles full ToS docs), structured output |
| **Web Scraping** | Playwright | Handles JavaScript-rendered content, headless browser automation |
| **HTML Parsing** | BeautifulSoup4 | Lightweight, reliable HTML/XML parsing |
| **PDF Parsing** | PyMuPDF (fitz) | Fast, accurate text extraction from PDFs |
| **Database** | PostgreSQL | Reliable, supports JSON columns for flexible summary storage |
| **Cache** | Redis | Rate limiting, session management, hot summary caching |
| **Hosting** | Vercel (frontend) + Railway/Render (backend) | Simple deployment, good free tiers |

### Data Models

```python
# Core database models

class Document(BaseModel):
    id: UUID
    url: str
    service_name: str
    document_type: Literal["tos", "privacy", "community_guidelines", "other"]
    raw_content: str
    content_hash: str  # For detecting changes
    extracted_at: datetime
    
class Summary(BaseModel):
    id: UUID
    document_id: UUID
    version: int
    
    # Structured summary sections
    red_flags: list[RedFlag]
    rules: list[Rule]
    concessions: list[Concession]
    
    # Metadata
    clarity_score: int  # 0-100
    reading_level: str  # e.g., "College", "High School"
    original_word_count: int
    summary_word_count: int
    generated_at: datetime
    model_version: str

class RedFlag(BaseModel):
    severity: Literal["critical", "warning", "info"]
    category: str  # e.g., "data_sharing", "arbitration", "content_rights"
    title: str
    explanation: str
    source_quote: str  # Original text from document

class Rule(BaseModel):
    category: str  # e.g., "content", "account", "usage"
    title: str
    description: str
    consequence: str | None  # What happens if violated

class Concession(BaseModel):
    category: str  # e.g., "data", "rights", "legal"
    title: str
    what_you_give: str
    why_they_want_it: str  # Plain English explanation
    can_opt_out: bool
    opt_out_instructions: str | None
```

---

## Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
**Goal:** Working backend that can analyze YouTube and OpenAI ToS

- [x] **Project Setup**
  - ✅ Initialize FastAPI project with proper structure
  - ✅ Set up PostgreSQL database with SQLAlchemy
  - ✅ Configure Redis for caching
  - ✅ Set up development environment (Docker Compose)
  - ✅ Create initial Alembic migration for database schema
  - ✅ Implement comprehensive unit tests for:
    - Database models and operations
    - Redis caching operations
    - Application startup and health checks
    - API endpoints and dependencies

- [ ] **Document Extraction Service**
  - Implement Playwright-based scraper for dynamic pages
  - Add BeautifulSoup parser for static content
  - Create URL-to-content pipeline
  - Handle YouTube ToS page structure
  - Handle OpenAI ToS page structure

- [ ] **AI Analysis Engine**
  - Design prompt templates for ToS analysis
  - Implement Claude API integration
  - Create structured output parser
  - Build red flag detection system
  - Implement clarity score algorithm

- [ ] **Core API Endpoints**
  - POST `/api/analyze` - Accept URL, return job ID
  - GET `/api/summary/{id}` - Retrieve analysis results
  - Implement proper error handling and validation

### Phase 2: Chrome Extension (Weeks 3-4)
**Goal:** Functional Chrome extension with core features

- [ ] **Extension Infrastructure**
  - Set up TypeScript + React build pipeline (Vite/Webpack)
  - Create manifest.json (Manifest V3)
  - Implement background service worker
  - Set up content script injection

- [ ] **Page Detection**
  - Build ToS page detector (URL patterns, page content analysis)
  - Create floating indicator for detected pages
  - Handle edge cases (iframes, popups, SPAs)

- [ ] **Popup Interface**
  - Design summary display UI
  - Implement loading states
  - Add "Analyze This Page" manual trigger
  - Create settings panel

- [ ] **Integration**
  - Connect extension to backend API
  - Implement local caching for offline access
  - Add error handling and retry logic

### Phase 3: Web Portal (Weeks 5-6)
**Goal:** Public-facing website with core functionality

- [ ] **Next.js Application**
  - Set up Next.js 14 with App Router
  - Implement responsive design (Tailwind CSS)
  - Create landing page with value proposition
  - Build URL input interface

- [ ] **Summary Display**
  - Port summary UI from extension
  - Add shareable summary links
  - Implement print-friendly view

- [ ] **User Features**
  - Anonymous usage (no account required for basic use)
  - Optional account creation
  - Analysis history (for logged-in users)

### Phase 4: Polish & Launch Prep (Weeks 7-8)
**Goal:** Production-ready MVP

- [ ] **Quality & Performance**
  - Comprehensive error handling
  - Rate limiting implementation
  - Performance optimization (caching strategy)
  - Mobile responsiveness testing

- [ ] **Content & Trust**
  - Write documentation
  - Create "How It Works" explainer
  - Add disclaimer about AI limitations
  - Implement feedback mechanism

- [ ] **Launch Infrastructure**
  - Set up production hosting
  - Configure monitoring (error tracking, analytics)
  - Implement basic abuse prevention
  - Chrome Web Store submission

---

## Future Roadmap (Post-MVP)

### v1.1 - Expanded Coverage
- Add 20+ popular services (social media, streaming, productivity tools)
- Community-submitted URL support
- Automated periodic re-scanning for ToS changes

### v1.2 - Comparison Features
- Side-by-side service comparisons
- Category rankings (e.g., "Best privacy practices in social media")
- Historical version diffs

### v1.3 - Premium Features
- API access for developers/researchers
- Team accounts for organizations
- Custom monitoring (alerts when tracked ToS changes)
- Detailed PDF reports

### v2.0 - Platform Expansion
- Firefox extension
- Safari extension
- Mobile apps (iOS/Android)

---

## Monetization Strategy (TBD)

### Free Tier (Forever Free)
- 10 analyses per month
- Access to pre-analyzed popular services
- Basic summary view
- Chrome extension core features

### Pro Tier ($5/month or $48/year)
- Unlimited analyses
- Full analysis history
- Comparison tools
- Priority processing
- Export summaries (PDF, Markdown)
- Email alerts for ToS changes on saved services

### Team/Enterprise (Custom pricing)
- API access
- Bulk analysis
- Custom integrations
- White-label options
- Compliance reporting features

### Additional Revenue Streams
- Anonymized, aggregated insights sold to researchers/journalists
- Sponsored "transparency reports" from companies wanting to highlight fair terms

---

## Project Structure

```
tos-clarity/
├── README.md
├── docker-compose.yml
│
├── backend/
│   ├── pyproject.toml
│   ├── alembic/                    # Database migrations
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Environment config
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── analyze.py
│   │   │   │   ├── summary.py
│   │   │   │   └── compare.py
│   │   │   └── dependencies.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── scraper.py          # Document extraction
│   │   │   ├── analyzer.py         # AI analysis orchestration
│   │   │   ├── claude_client.py    # Claude API wrapper
│   │   │   └── scoring.py          # Clarity score calculation
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── database.py         # SQLAlchemy models
│   │   │   └── schemas.py          # Pydantic schemas
│   │   ├── prompts/
│   │   │   ├── analyze_tos.txt
│   │   │   ├── extract_red_flags.txt
│   │   │   └── generate_summary.txt
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── text_processing.py
│   └── tests/
│
├── extension/
│   ├── package.json
│   ├── manifest.json
│   ├── src/
│   │   ├── background/
│   │   │   └── service-worker.ts
│   │   ├── content/
│   │   │   ├── detector.ts         # ToS page detection
│   │   │   └── injector.ts         # UI injection
│   │   ├── popup/
│   │   │   ├── App.tsx
│   │   │   ├── components/
│   │   │   └── hooks/
│   │   ├── shared/
│   │   │   ├── api.ts              # Backend API client
│   │   │   ├── types.ts
│   │   │   └── storage.ts          # Chrome storage wrapper
│   │   └── styles/
│   └── public/
│       └── icons/
│
├── web/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                # Landing page
│   │   ├── analyze/
│   │   │   └── page.tsx            # URL input page
│   │   ├── summary/
│   │   │   └── [id]/
│   │   │       └── page.tsx        # Summary display
│   │   └── api/                    # API routes (proxy to backend)
│   ├── components/
│   │   ├── SummaryCard.tsx
│   │   ├── RedFlagBadge.tsx
│   │   ├── RulesList.tsx
│   │   └── ClarityScore.tsx
│   └── lib/
│       └── api.ts
│
└── shared/
    └── types/                      # Shared TypeScript types
        └── index.ts
```

---

## Getting Started (Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Anthropic API key

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/tos-clarity.git
cd tos-clarity

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# Backend is available at http://localhost:8000
# Web portal is available at http://localhost:3000
```

### Running Individual Components

```bash
# Backend only
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# Web portal only
cd web
npm install
npm run dev

# Extension (development build)
cd extension
npm install
npm run dev
# Load unpacked extension from extension/dist in Chrome
```

### Database Migrations

```bash
# Run migrations
cd backend
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Rollback last migration
alembic downgrade -1
```

### Running Tests

```bash
# Run all tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

---

## API Reference

### Analyze a URL

```http
POST /api/analyze
Content-Type: application/json

{
  "url": "https://www.youtube.com/static?template=terms",
  "options": {
    "include_full_text": false,
    "language": "en"
  }
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "estimated_time_seconds": 15
}
```

### Get Summary

```http
GET /api/summary/550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "service_name": "YouTube",
  "document_type": "tos",
  "analyzed_at": "2025-01-15T10:30:00Z",
  "clarity_score": 62,
  "red_flags": [
    {
      "severity": "warning",
      "category": "content_rights",
      "title": "Broad Content License",
      "explanation": "YouTube gets a worldwide license to use, reproduce, and distribute any content you upload",
      "source_quote": "you grant YouTube a worldwide, non-exclusive, royalty-free..."
    }
  ],
  "rules": [...],
  "concessions": [...],
  "metadata": {
    "original_word_count": 4521,
    "summary_word_count": 312,
    "reading_level": "College",
    "last_updated": "2024-12-01"
  }
}
```

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Priority Areas
- Adding support for new services
- Improving prompt templates for better analysis
- UI/UX improvements
- Translations

---

## Legal Disclaimer

ToS Clarity is an educational tool designed to help users understand legal documents. The summaries provided are AI-generated and should not be considered legal advice. Always consult with a qualified attorney for legal matters. We make no warranties about the accuracy or completeness of our summaries.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Inspired by [Terms of Service; Didn't Read](https://tosdr.org/)
- Built with [Claude](https://anthropic.com) by Anthropic
