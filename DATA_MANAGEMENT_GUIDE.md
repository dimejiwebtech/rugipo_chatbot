# Data Management System Setup Guide

This guide explains how to use the new data management system for the RUGIPO chatbot, which includes:

1. **Django Admin Dashboard** - Add/edit Q&A through web interface
2. **Web Scraper** - Automatically pull data from RUGIPO website
3. **Automated Export** - Auto-export data to JSON
4. **Scheduled Tasks** - Optional periodic scraping

---

## Quick Start

### Option 1: Manual Add/Edit via Admin (Recommended for Development)

1. **Start the server:**

   ```bash
   python manage.py runserver
   ```

2. **Go to admin panel:**

   - Visit: `http://127.0.0.1:8000/admin/`
   - Login with your superuser credentials

3. **Add Q&A:**

   - Go to: Knowledge → Engineering Q&As
   - Click "Add Engineering Q&A"
   - Fill in the form:
     - **Category:** Select the engineering department
     - **Question:** The question students might ask
     - **Answer:** The answer to provide
     - **Keywords:** Comma-separated keywords for search
   - Click "Save"
   - JSON file automatically updates!

4. **Manage Q&A:**
   - Filter by category or active status
   - Search by question/answer/keywords
   - Enable/disable Q&As with checkboxes
   - Bulk activate/deactivate

---

### Option 2: Automatic Web Scraping (One-Time or Scheduled)

#### A. Manual Trigger (In Admin Panel)

1. In the Q&A admin list, there's a **"Scrape RUGIPO website for new data"** action
2. Select any Q&A (or just select one as placeholder)
3. From the "Action" dropdown, select the scrape action
4. Click "Go"
5. The system will:
   - Scrape RUGIPO website
   - Add new Q&As to database
   - Update existing ones if changed
   - Auto-export to JSON

#### B. Manual Trigger (Command Line)

Run a single scrape:

```bash
python manage.py scrape_rugipo
```

Run scrape and export:

```bash
python manage.py scrape_rugipo --export
```

---

## Full Workflow Options

### Workflow 1: Manual Management + Manual Export

**Best for:** Development, small teams, testing

```
Staff edits in Admin → Auto-saves to DB → Signal auto-exports to JSON
```

Steps:

1. Staff adds/edits Q&A via admin dashboard
2. Signals automatically export to `data/engineering_qa.json`
3. Chatbot reads from JSON

**Commands:**

```bash
# Add/edit via web interface only
python manage.py runserver
```

---

### Workflow 2: Manual Management + Periodic Scraping

**Best for:** Production with manual + automated updates

```
Staff edits in Admin → Combined with → Periodic website scrapes
         ↓                                      ↓
    Updates DB                         Updates DB
         └──────────→ Auto-export to JSON ←─────┘
```

Steps:

1. Staff manages Q&A manually
2. Scraper runs daily (or on-demand) to fetch new data
3. Everything syncs to JSON

**Setup:**

```bash
# In your .env file, add:
START_SCHEDULER=true
```

Then run:

```bash
python manage.py runserver
```

The scraper will run automatically at 2 AM daily.

Or manually trigger:

```bash
python manage.py scrape_rugipo --export
```

---

### Workflow 3: Full Automation

**Best for:** Production with minimal manual intervention

```
RUGIPO Website → Scraper (runs daily) → Database → JSON
                                           ↑
                     Admin (for corrections) ↓
```

Steps:

1. Enable scheduler in `.env`
2. Scraper runs automatically
3. Staff only makes corrections/additions via admin

**Setup:**

```bash
# In .env:
START_SCHEDULER=true
```

Then:

```bash
python manage.py runserver
```

---

## Management Commands

### Export Q&A to JSON

```bash
python manage.py export_qa
```

Output: `✓ Successfully exported Q&A to: /path/to/engineering_qa.json`

---

### Scrape Website (Manual)

```bash
python manage.py scrape_rugipo
```

Output:

```
🔄 Starting RUGIPO data scrape...
✓ Scrape completed!
  • Added: 5 Q&As
  • Updated: 2 Q&As
  • Total processed: 7
```

With auto-export:

```bash
python manage.py scrape_rugipo --export
```

---

### Auto-Reload JSON via Admin

In Django admin Q&A page:

1. Click the "Export all active Q&As to JSON" action
2. Select any Q&A
3. Click "Go"
4. Done!

---

## API Endpoints (For Developers)

### Trigger Scrape Programmatically

**POST** `/api/knowledge/scrape/`

Requires login. Returns:

```json
{
  "success": true,
  "message": "Scraping completed successfully",
  "result": {
    "added": 5,
    "updated": 2,
    "total": 7
  }
}
```

---

### Export to JSON Programmatically

**POST** `/api/knowledge/export/`

Requires login. Returns:

```json
{
  "success": true,
  "message": "Exported to ...",
  "path": "/absolute/path/to/engineering_qa.json"
}
```

---

## Configuration

### In Settings (`config/settings.py`)

```python
# Location of JSON file
KNOWLEDGE_BASE_JSON_PATH = BASE_DIR / 'data' / 'engineering_qa.json'

# Enable/disable auto-scraper at startup
START_SCHEDULER = False  # Set to True to enable daily 2 AM scraping
```

### In .env File

```
# Optional: Enable automatic daily scraping
START_SCHEDULER=false
```

---

## Scraper Configuration

The scraper in `knowledge/scraper.py` looks for:

1. **Program Information** - From `/engineering` pages
2. **Contact Information** - From `/about/staff` pages
3. **FAQs** - From `/faq` pages

It automatically:

- Categorizes by engineering department
- Extracts keywords
- Detects duplicates
- Updates existing Q&As
- Creates new entries

**Note:** You may need to customize the scraper based on RUGIPO's actual website structure.

---

## Troubleshooting

### Issue: "Signal not running - changes not auto-exporting"

**Solution:** Signals are enabled by default. If they're not working:

1. Restart Django server
2. Check that `knowledge/signals.py` is imported in `knowledge/apps.py`

---

### Issue: Scraper returns no data

**Possible Causes:**

1. RUGIPO website structure changed - update selectors in `scraper.py`
2. Website uses JavaScript to load content - use Selenium/Playwright instead
3. Website blocks requests - add proper headers or delays

**Solution:**

1. Inspect the website with browser dev tools
2. Update CSS selectors in `scraper.py`
3. Test with: `python manage.py shell`
   ```python
   from knowledge.scraper import RUGIPOScraper
   scraper = RUGIPOScraper()
   data = scraper.scrape_program_info()
   print(data)
   ```

---

### Issue: Scheduler not running

**Solution:**

1. Ensure `START_SCHEDULER=true` in `.env`
2. Restart Django server
3. Check logs for errors
4. Verify APScheduler is installed: `pip list | grep apscheduler`

---

### Issue: Permission denied when exporting JSON

**Solution:**

```bash
# Ensure data directory exists
mkdir data

# Give write permissions
chmod 755 data/
```

---

## Best Practices

1. **Regular Backups:** Keep backups of `data/engineering_qa.json`
2. **Version Control:** Don't commit the JSON file, only the database backups
3. **Monitor Scrapes:** Check logs for scraper errors
4. **Test Selectors:** Before full scrape, test CSS selectors in browser console
5. **Manual Review:** Review scraped data before marking as active
6. **Keywords:** Add meaningful keywords for better chatbot search

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     RUGIPO Chatbot                          │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼────────┐  ┌──────▼───────┐
            │  Django Admin  │  │ API Endpoints│
            │   Dashboard    │  │ (Scrape/Exp) │
            └───────┬────────┘  └──────┬───────┘
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Django Models    │
                    │  EngineeringQA     │
                    │   (Database)       │
                    └─────────┬──────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼───────┐    ┌────────▼────────┐    ┌─────▼────────┐
   │   Signals  │    │   Scheduler     │    │   Scraper    │
   │ (Auto-exp) │    │   (Daily 2 AM)  │    │ (Manual/Auto)│
   └────┬───────┘    └────────┬────────┘    └─────┬────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  JSON Export Util  │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  engineering_qa.json
                    │   (Data File)      │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  OpenAI Service    │
                    │  (Loads on startup)│
                    └────────────────────┘
```

---

## Next Steps

1. **Add Initial Data:**

   - Use admin to add FAQs manually, or
   - Run scraper to fetch from website

2. **Test the Workflow:**

   ```bash
   python manage.py runserver
   # Go to admin and add a Q&A
   # Check if JSON updates automatically
   ```

3. **Enable Scraper (Optional):**

   - Update `.env`: `START_SCHEDULER=true`
   - Customize scraper selectors for RUGIPO site

4. **Monitor & Maintain:**
   - Check logs for errors
   - Review scraped data quality
   - Update selectors if website changes

---

## Support & Questions

For issues or questions:

- Check the troubleshooting section
- Review Django admin interface help
- Check scraper logs in console
- Inspect website structure with browser dev tools
