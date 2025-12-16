# 🚀 Getting Started - Data Management System

## What You Have Now

✅ **No More Manual JSON Editing!**

Instead of manually editing `data/engineering_qa.json`, you now have:

1. **Admin Dashboard** - Add Q&A through web form
2. **Web Scraper** - Fetch data from RUGIPO website
3. **Scheduler** - Optional automatic daily updates
4. **Auto-Export** - JSON always stays in sync

---

## Start Here (5 Minutes)

### Step 1: Start Server

```bash
python manage.py runserver
```

### Step 2: Open Admin

Visit: `http://127.0.0.1:8000/admin/`

### Step 3: Login

Use your superuser username/password

### Step 4: Add Q&A

1. Click: **Knowledge** → **Engineering Q&As** → **Add**
2. Fill the form:
   - **Category:** Pick one (Civil, Computer, Electrical, Mechanical, Agricultural)
   - **Question:** What students ask
   - **Answer:** Your answer
   - **Keywords:** Comma-separated for search
3. Click **Save**
4. **Done!** JSON updates automatically ✓

---

## Three Ways to Add Data

### Way 1: Admin Dashboard (Easiest)

```
Admin → Add Q&A → Save
↓
JSON auto-updates ✓
```

### Way 2: Manual Scrape (Command)

```bash
python manage.py scrape_rugipo --export
```

### Way 3: Admin Scrape Action

```
Admin → Q&A → Select any →
  Action: "Scrape RUGIPO website" → Go
↓
Fetches website → Updates DB → Auto-exports ✓
```

---

## Key Features

| Feature                | Location                | How                                        |
| ---------------------- | ----------------------- | ------------------------------------------ |
| **Add Q&A**            | `/admin/`               | Web form                                   |
| **Edit Q&A**           | `/admin/`               | Click item                                 |
| **Delete Q&A**         | `/admin/`               | Check box + delete                         |
| **Search Q&A**         | `/admin/`               | Search box                                 |
| **Filter by category** | `/admin/`               | Left panel                                 |
| **Export to JSON**     | Command                 | `python manage.py export_qa`               |
| **Scrape website**     | Admin action or command | Button or `python manage.py scrape_rugipo` |

---

## Enable Auto-Scraping (Optional)

Want the scraper to run automatically every day at 2 AM?

1. Edit `.env` file
2. Add this line: `START_SCHEDULER=true`
3. Restart server: `Ctrl+C` then `python manage.py runserver`
4. ✓ Done! Scraper runs daily now

---

## Common Tasks

### Add a Q&A

```
1. Go to admin
2. Knowledge → Engineering Q&As → Add
3. Fill form
4. Click Save
5. Check JSON auto-updated ✓
```

### Update a Q&A

```
1. Go to admin
2. Knowledge → Engineering Q&As
3. Click the Q&A you want to edit
4. Change fields
5. Click Save
6. JSON auto-updates ✓
```

### Bulk Import from Website

```bash
python manage.py scrape_rugipo --export
```

Fetches from RUGIPO website → Adds to database → Exports to JSON

### Export Manually

```bash
python manage.py export_qa
```

Takes current database → Creates fresh JSON file

---

## If Something Goes Wrong

### JSON not updating?

- Signals work automatically
- Try restarting server: `Ctrl+C` then `python manage.py runserver`

### Scraper returns no data?

- Website structure might be different
- Customizer `knowledge/scraper.py` selectors (see DATA_MANAGEMENT_GUIDE.md)

### Scheduler not running?

- Check `.env`: Does it have `START_SCHEDULER=true`?
- Restart server

---

## Files to Read

For more details, read these in order:

1. **QUICK_REFERENCE.md** (2 min)

   - One-page cheat sheet

2. **DATA_MANAGEMENT_GUIDE.md** (15 min)

   - Complete tutorial

3. **SYSTEM_ARCHITECTURE.md** (20 min)
   - How it all works

---

## That's It!

You now have a professional data management system.

**Next step:** Start server and visit `/admin/` to add your first Q&A!

```bash
python manage.py runserver
# Then open: http://127.0.0.1:8000/admin/
```

✨ **No more manual JSON editing!**

---

## Quick Commands Reference

```bash
# Start server
python manage.py runserver

# Export database to JSON
python manage.py export_qa

# Scrape website (one-time)
python manage.py scrape_rugipo

# Scrape and export
python manage.py scrape_rugipo --export

# Check database
python manage.py dbshell

# Shell access
python manage.py shell

# See Q&A count
python manage.py shell
>>> from knowledge.models import EngineeringQA
>>> EngineeringQA.objects.count()
```

---

**Questions?** Read the documentation files or check the troubleshooting section.

**Ready?** Fire up the server and go to `/admin/`! 🚀
