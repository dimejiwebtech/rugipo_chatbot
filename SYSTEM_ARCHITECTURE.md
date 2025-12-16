# System Architecture - Visual Overview

## Directory Structure (After Implementation)

```
rugipo_chatbot/
├── knowledge/                          # Core data management app
│   ├── management/                     # Django management commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── export_qa.py           # Export DB to JSON
│   │       └── scrape_rugipo.py       # Scrape & update DB
│   │
│   ├── migrations/                     # Database migrations
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_engineeringqa_category.py
│   │
│   ├── __init__.py
│   ├── admin.py                        # ✨ Django admin (add/edit Q&A)
│   ├── apps.py                         # ✨ Scheduler initialization
│   ├── models.py                       # EngineeringQA model
│   ├── signals.py                      # ✨ Auto-export on save
│   ├── urls.py                         # ✨ API endpoints
│   ├── views.py                        # ✨ API handlers
│   ├── scraper.py                      # ✨ Web scraper
│   ├── scheduler.py                    # ✨ Task scheduler
│   ├── utils.py                        # ✨ Export utility
│   └── tests.py
│
├── config/
│   ├── settings.py                     # ✨ Scheduler & JSON config
│   ├── urls.py                         # ✨ Added knowledge URLs
│   ├── wsgi.py
│   └── asgi.py
│
├── chatbot/                            # Chat API
│   ├── services/
│   │   └── openai_service.py          # Loads JSON & uses scraped data
│   ├── models.py                       # Chat sessions & messages
│   ├── views.py                        # Chat endpoints
│   └── urls.py
│
├── data/
│   └── engineering_qa.json             # ✨ Auto-updated from DB
│
├── IMPLEMENTATION_SUMMARY.md           # ✨ This implementation
├── DATA_MANAGEMENT_GUIDE.md            # ✨ Full documentation
├── QUICK_REFERENCE.md                  # ✨ Quick start guide
├── README.md                           # Main project README
├── manage.py
└── db.sqlite3                          # Database

✨ = NEW or MODIFIED during implementation
```

---

## Data Flow Diagram

### Workflow 1: Manual Admin Entry (Development)

```
┌──────────────────┐
│  Django Admin UI │
│ /admin/          │
└────────┬─────────┘
         │ Add/Edit Q&A
         ↓
    ┌─────────┐
    │Database │ (SQLite)
    │ Q&A    │
    └────┬────┘
         │ Signal: post_save
         ↓
  ┌─────────────────┐
  │  export_qa()    │
  │  (utils.py)     │
  └────┬────────────┘
       │
       ↓
┌──────────────────────┐
│engineering_qa.json   │
│(auto-updated)        │
└────┬─────────────────┘
     │
     ↓ (chatbot reads on startup)
┌──────────────────┐
│ OpenAI Service   │
│ (Knowledge base) │
└──────────────────┘
```

### Workflow 2: Website Scraping

```
┌──────────────────┐
│ RUGIPO Website   │
│ /engineering     │
│ /about/staff     │
│ /faq             │
└────────┬─────────┘
         │
         ↓ (HTTP requests)
  ┌──────────────────┐
  │  RUGIPOScraper   │
  │  (scraper.py)    │
  │  - Parse HTML    │
  │  - Extract data  │
  │  - Categorize    │
  └────────┬─────────┘
           │
           ↓
       ┌──────────┐
       │Database  │ Smart merging:
       │  Q&A     │ - Add new
       │          │ - Update changed
       └────┬─────┘ - Avoid dupes
            │
            ↓ Signal: post_save
     ┌────────────────┐
     │  Auto-export   │
     │  to JSON       │
     └────────────────┘
```

### Workflow 3: Scheduled Automatic Scraping

```
┌──────────────────┐
│ App Startup      │
│ (Django init)    │
└────────┬─────────┘
         │
         ↓
   ┌──────────────┐
   │Scheduler     │ Only if:
   │initialized   │ START_SCHEDULER=true
   │(scheduler.py)│
   └────────┬─────┘
            │
            ↓ (Daily at 2 AM)
   ┌──────────────────────┐
   │ scheduled_scrape()   │
   │ - Run scraper        │
   │ - Update DB          │
   │ - Auto-export JSON   │
   │ - Log results        │
   └─────────────────────┘
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    RUGIPO CHATBOT SYSTEM                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERACTIONS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Admin Staff         ChatBot Users      API Consumers           │
│  ├─ /admin/         ├─ Website         ├─ External apps       │
│  └─ Add Q&A         └─ /chat/          └─ Monitoring tools    │
│                                                                 │
└──────────────────┬──────────────────────┬──────────────────────┘
                   │                      │
            ┌──────▼──────┐         ┌─────▼───────┐
            │ Django Admin│         │  Chat API   │
            │  Interface  │         │  (chatbot/) │
            └──────┬──────┘         └─────┬───────┘
                   │                      │
        ┌──────────▼──────────────────────▼──────────┐
        │         Django Models / Database           │
        │                                             │
        │  ┌─────────────────────────────────────┐   │
        │  │  EngineeringQA                      │   │
        │  │  - category                         │   │
        │  │  - question                         │   │
        │  │  - answer                           │   │
        │  │  - keywords                         │   │
        │  │  - is_active                        │   │
        │  └─────────────────────────────────────┘   │
        │                                             │
        │  ┌─────────────────────────────────────┐   │
        │  │  ChatSession / ChatMessage          │   │
        │  │  (conversation history)             │   │
        │  └─────────────────────────────────────┘   │
        │                                             │
        └────────────────┬──────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼──────┐  ┌──────▼──────┐  ┌────▼────────┐
   │  Signals  │  │  Scheduler  │  │  Scraper    │
   │ (Post-save)  (Background)  │  (Web fetch)  │
   └────┬──────┘  └──────┬──────┘  └────┬────────┘
        │                │              │
        └────────────────┼──────────────┘
                         │
                    ┌────▼───────┐
                    │   Export   │
                    │  Utility   │
                    │(utils.py)  │
                    └────┬───────┘
                         │
                    ┌────▼──────────────┐
                    │engineering_qa.json│
                    │  (Data File)       │
                    └────┬──────────────┘
                         │
                    ┌────▼─────────────┐
                    │  OpenAI Service  │
                    │ (Loads on init)  │
                    └──────────────────┘
```

---

## API Endpoints

### Management APIs (Admin Only)

```
POST /api/knowledge/scrape/
├─ Authentication: Login required
├─ Body: {} (empty)
└─ Response:
   {
     "success": true,
     "message": "Scraping completed successfully",
     "result": {
       "added": 5,
       "updated": 2,
       "total": 7
     }
   }

POST /api/knowledge/export/
├─ Authentication: Login required
├─ Body: {} (empty)
└─ Response:
   {
     "success": true,
     "message": "Exported to ...",
     "path": "/absolute/path/to/engineering_qa.json"
   }
```

---

## Database Schema

### EngineeringQA Model

```sql
CREATE TABLE knowledge_engineeringqa (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    keywords VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW
)

Categories:
- 'abet' → Agricultural and Bio-Environmental Engineering Technology
- 'cet'  → Civil Engineering Technology
- 'cte'  → Computer Engineering Technology
- 'eeet' → Electrical/Electronics Engineering Technology
- 'met'  → Mechanical Engineering Technology
```

---

## Configuration

### Environment Variables (.env)

```
# Optional: Enable automatic daily scraping at 2 AM
START_SCHEDULER=false
```

### Django Settings (config/settings.py)

```python
# JSON file location
KNOWLEDGE_BASE_JSON_PATH = BASE_DIR / 'data' / 'engineering_qa.json'

# Enable/disable scheduler
START_SCHEDULER = os.getenv('START_SCHEDULER', 'False').lower() == 'true'
```

---

## Execution Flow

### When Server Starts

```
1. Django initializes
2. knowledge.apps.KnowledgeConfig.ready() called
3. Signals imported
4. If START_SCHEDULER=true:
   └─ Scheduler starts
   └─ Jobs registered
   └─ Scraper scheduled for 2 AM daily
5. Server ready for requests
```

### When Admin Saves Q&A

```
1. Admin form submitted
2. Model saved to DB
3. Signal: post_save triggered
4. export_on_save() executes
5. export_engineering_qa_to_json() called
6. JSON file updated
7. Response sent to admin
```

### When Manual Scrape Triggered

```
1. Admin action or command executed
2. scrape_rugipo_data() called
3. RUGIPOScraper fetches data
4. Parser extracts information
5. Categorizes results
6. DB updated (add/update)
7. Signal triggers
8. JSON auto-exported
9. Results reported
```

### When Scheduled Time Arrives (2 AM)

```
1. APScheduler triggers job
2. scheduled_scrape() executed
3. Scraper runs (same as manual)
4. Data merged into DB
5. Auto-export via signals
6. Results logged
```

---

## Error Handling

```
RUGIPOScraper
├─ Network Errors
│  └─ Logged, gracefully handled
├─ Parse Errors
│  └─ Continue with next section
├─ Timeout (10s)
│  └─ Log error, return empty
└─ HTTP Errors
   └─ Log error, continue

Database Operations
├─ Duplicate Detection
│  └─ Update existing if matches
├─ Categorization Failures
│  └─ Default to None, skip
└─ Save Failures
   └─ Log and continue

Export Operations
├─ File Permission Issues
│  └─ Try to create/fix directory
├─ JSON Encoding
│  └─ Use UTF-8 with ensure_ascii=False
└─ Directory Missing
   └─ Create with mkdir(parents=True)
```

---

## Performance Considerations

### Database

- Indexed: category, is_active, created_at
- Queries optimized for Q&A lookup
- Signaling via Django ORM

### Scraper

- 10-second timeout per URL
- Graceful fallback on failure
- Batch processing of results
- Memory efficient parsing

### Scheduler

- Background process (non-blocking)
- Runs outside request/response cycle
- Logs all activities
- Can be disabled in development

### JSON Export

- Only exports active Q&As
- Incremental (only when changed)
- Optimized file size (indented)

---

## Security

✅ **Admin Actions Protected**

- Require Django login
- CSRF protection enabled
- Admin permission checks

✅ **API Endpoints Protected**

- Require authentication (@login_required)
- Limit to trusted users only

✅ **Scraper Safety**

- Validates URLs
- Handles network errors
- Timeouts on slow responses
- Proper error logging

✅ **Data Validation**

- Model validation on save
- Category choices restricted
- Keyword sanitization
- HTML escaping in admin

---

## Logging

### Scraper Logs

- Started/completed messages
- Items added/updated count
- Errors with context
- Source of each Q&A

### Scheduler Logs

- Startup/shutdown
- Job registration
- Execution timestamps
- Success/failure status

### Export Logs

- Export path
- Item count
- Success/failure

---

This architecture enables:

- ✅ Multiple data entry methods
- ✅ Automatic synchronization
- ✅ Graceful degradation
- ✅ Optional automation
- ✅ Production readiness
- ✅ Easy troubleshooting
