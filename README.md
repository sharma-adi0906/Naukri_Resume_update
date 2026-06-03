# Naukri Resume Auto-Update 🚀

> Auto-update your resume on [naukri.com](https://www.naukri.com) with one click — or schedule it to run daily at 9 AM automatically.

---

## Prerequisites

- **Python** installed with **"Add python.exe to PATH"** checked during installation
- Install required packages:

```bash
pip install playwright python-dotenv
playwright install chromium
```

---

## Setup

**1. Clone this repository**

```bash
git clone https://github.com/sharma-adi0906/Naukri_Resume_update.git
cd Naukri_Resume_update
```

**2. Configure your credentials**

create the `.env` file and fill in your details:

```env
NAUKRI_EMAIL=your_email@gmail.com
NAUKRI_PASSWORD=your_password
RESUME_PATH=C:\Users\YourName\Desktop\Naukri_Resume_update\YourResume.pdf
```

> 💡 **Tip:** Keep your resume file inside this project folder and paste its full path in `RESUME_PATH`.  
> To get the exact path: **Shift + Right-click** the file in File Explorer → **"Copy as path"** → paste it here (remove the surrounding quotes).

---

## Usage

### Run Manually

```bash
python naukri_refresh.py
```

### Schedule with Task Scheduler (Recommended)

Run once and it will trigger automatically every day at 9 AM.

**Step 1 — Find your Python path**

```cmd
where.exe python
```

Copy the output (e.g. `C:\Python314\python.exe`) and paste it into `task-scheduler.ps1` where the Python path is specified.

**Step 2 — Register the scheduled task**

Open PowerShell **as Administrator**, then copy the full contents of `task-scheduler.ps1` and run it.

**Step 3 — Verify the task is scheduled**

```powershell
Get-ScheduledTask -TaskName "Naukri Daily Resume Upload"
```

**Step 4 — Start the task immediately (optional test)**

```powershell
Start-ScheduledTask -TaskName "Naukri Daily Resume Upload"
```

---

## Project Structure

```
Naukri_Resume_update/
├── naukri_refresh.py       # Main automation script
├── task-scheduler.ps1      # PowerShell script to register the Windows Task
├── .env                    # Your credentials (never commit this)
├── naukri_refresh.log      # Auto-generated run log
└── README.md
```

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `playwright: command not found` | Run `python -m playwright install chromium` instead |
| `Resume upload skipped` | Check `RESUME_PATH` in `.env` — run `python naukri_refresh.py` and look for the path debug output |
| Login fails | Delete `naukri_session.json` and re-run to trigger a fresh login |
| Scheduled task doesn't run | Verify Python path in `task-scheduler.ps1` using `where.exe python` |

---

## Notes

- On first run, the script saves a session cookie (`naukri_session.json`) so it doesn't need to log in every day
- If a run fails, a screenshot is saved in the project folder for debugging
- Check `naukri_refresh.log` to see the history of all runs
