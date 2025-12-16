# Quick Reference: Data Management System

## What Was Added

✅ **Django Admin Dashboard** - Add/edit Q&A without manual JSON editing
✅ **Automated JSON Export** - Auto-exports when you save in admin
✅ **Web Scraper** - Pulls data from RUGIPO website
✅ **Scheduled Tasks** - Optional automatic daily scraping at 2 AM
✅ **Management Commands** - Run scraper from terminal

---

## Three Ways to Update Data

### 1. Admin Dashboard (Easiest - Recommended)

```bash
python manage.py runserver
# Visit http://127.0.0.1:8000/admin/
# Go to Engineering Q&As → Add/Edit
# Save → Auto-exports to JSON ✓
```

### 2. Manual Scraping (Command Line)

```bash
python manage.py scrape_rugipo --export
# Fetches from RUGIPO website → Updates DB → Exports JSON
```

### 3. Scraping Action (In Admin)

- In Q&A admin list
- Select any item
- Choose "Scrape RUGIPO website for new data" action
- Click Go → Fetches and exports ✓

---

## Install Required Packages

Already installed:

- ✅ beautifulsoup4 (web scraping)
- ✅ requests (HTTP requests)
- ✅ apscheduler (scheduled tasks)

---

## Enable Automatic Daily Scraping (Optional)

Edit `.env`:

```
START_SCHEDULER=true
```

Restart server. Scraper runs daily at 2 AM.

---

## File Changes Made

**New Files:**

- `knowledge/scraper.py` - Web scraper
- `knowledge/scheduler.py` - Task scheduler
- `knowledge/urls.py` - API endpoints
- `knowledge/management/commands/export_qa.py` - Export command
- `knowledge/management/commands/scrape_rugipo.py` - Scrape command
- `DATA_MANAGEMENT_GUIDE.md` - Full documentation

**Modified Files:**

- `knowledge/admin.py` - Added scrape action
- `knowledge/views.py` - Added API endpoints
- `knowledge/apps.py` - Initialize scheduler
- `config/urls.py` - Added knowledge API routes
- `config/settings.py` - Added scheduler config

**Already Good:**

- `knowledge/signals.py` ✓ (auto-export on save)
- `knowledge/utils.py` ✓ (export function)

---

## Test It Out

1. Start server:

   ```bash
   python manage.py runserver
   ```

2. Go to admin: `http://127.0.0.1:8000/admin/`

3. Add a new Q&A:

   - Knowledge → Engineering Q&As → Add
   - Fill form → Save

4. Check if JSON updated:

   - Open `data/engineering_qa.json`
   - Your new Q&A should be there ✓

5. (Optional) Test scraper:
   ```bash
   python manage.py scrape_rugipo --export
   ```

---

## Customization

### Update Scraper for RUGIPO Website

Edit `knowledge/scraper.py`:

1. Find the methods: `scrape_program_info()`, `scrape_contact_info()`, `scrape_faqs()`
2. Update CSS selectors to match RUGIPO's website structure
3. Test: `python manage.py scrape_rugipo`

Example: If HOD info is in `<div class="staff-list">`, update the selector there.

---

## Key Features

| Feature              | How to Use                       | Auto-Run?         |
| -------------------- | -------------------------------- | ----------------- |
| **Admin Dashboard**  | Visit `/admin/`, add Q&A         | ✓ exports on save |
| **Manual Export**    | `python manage.py export_qa`     | No                |
| **Manual Scrape**    | `python manage.py scrape_rugipo` | No                |
| **Scrape Action**    | Admin → select → choose action   | No                |
| **Scheduled Scrape** | Set `START_SCHEDULER=true`       | ✓ daily at 2 AM   |
| **API Trigger**      | POST to `/api/knowledge/scrape/` | No                |

---

## Troubleshooting

**JSON not updating?**

- Signals work automatically when saving in admin
- If not working, restart server

**Scraper returns no data?**

- RUGIPO website structure may be different
- Update CSS selectors in `scraper.py`
- Or test RUGIPO website manually

**Scheduler not starting?**

- Ensure `.env` has `START_SCHEDULER=true`
- Restart Django server
- Check if APScheduler is installed: `pip list | grep apscheduler`

---

## Full Documentation

See `DATA_MANAGEMENT_GUIDE.md` for complete details.
