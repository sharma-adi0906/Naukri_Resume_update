import os, sys, time, logging
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ── Load credentials ──────────────────────────────────────────────────────────
# Dynamically resolves to whatever folder the script is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(BASE_DIR, ".env"))

EMAIL       = os.getenv("NAUKRI_EMAIL")
PASSWORD    = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.getenv("RESUME_PATH")

print(f"RESUME_PATH value  : {RESUME_PATH}")
print(f"File exists check  : {os.path.exists(RESUME_PATH) if RESUME_PATH else 'PATH IS EMPTY'}")

LOG_FILE     = os.path.join(BASE_DIR, "naukri_refresh.log")
SESSION_FILE = os.path.join(BASE_DIR, "naukri_session.json")

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s"
)
log = logging.getLogger(__name__)


def run():
    log.info("=== Naukri refresh started ===")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Reuse saved session if available (avoids re-login every day)
        if os.path.exists(SESSION_FILE):
            context = browser.new_context(storage_state=SESSION_FILE)
            log.info("Loaded saved session")
        else:
            context = browser.new_context()

        page = context.new_page()

        try:
            page.goto("https://www.naukri.com", wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)

            if not _is_logged_in(page):
                log.info("Not logged in — attempting login")
                _login(page)
                context.storage_state(path=SESSION_FILE)
                log.info("Session saved for future runs")
            else:
                log.info("Already logged in via saved session")

            # Go to profile page
            page.goto("https://www.naukri.com/mnjuser/profile", timeout=30000)
            time.sleep(3)

            # Click Refresh
            refreshed = _click_refresh(page)

            # Upload resume
            if RESUME_PATH and os.path.exists(RESUME_PATH):
                _upload_resume(page)
            else:
                log.info("Resume upload skipped")

            if refreshed:
                log.info("SUCCESS — Profile refreshed at %s", datetime.now().strftime("%Y-%m-%d %H:%M"))
                print("SUCCESS - Naukri profile refreshed")
            else:
                log.warning("Refresh button not found — Naukri may have updated their UI")
                print("WARNING - Refresh button not found, check log")

        except PlaywrightTimeout as e:
            log.error("Timeout: %s", str(e))
            _screenshot(page, "timeout")
            sys.exit(1)
        except Exception as e:
            log.error("Error: %s", str(e))
            _screenshot(page, "error")
            sys.exit(1)
        finally:
            browser.close()


def _is_logged_in(page):
    try:
        page.wait_for_selector("a[href*='mnjuser/profile']", timeout=5000)
        return True
    except PlaywrightTimeout:
        return False


def _login(page):
    page.goto("https://www.naukri.com", wait_until="domcontentloaded")
    time.sleep(2)
    page.click("a[href*='login']")
    time.sleep(2)
    page.fill("input[placeholder*='Email']", EMAIL)
    page.fill("input[type='password']", PASSWORD)
    page.click("button[type='submit']")
    time.sleep(4)
    try:
        page.wait_for_selector("a[href*='mnjuser/profile']", timeout=10000)
        log.info("Login successful")
    except PlaywrightTimeout:
        log.error("Login failed — check credentials or CAPTCHA")
        _screenshot(page, "login_failed")
        raise Exception("Login failed")


def _click_refresh(page):
    selectors = [
        "span.update-btn-txt",
        "button[data-ga-track*='refresh']",
        ".refresh-btn",
        "//span[contains(text(), 'Refresh')]",
        "//button[contains(text(), 'Refresh')]",
    ]
    for sel in selectors:
        try:
            if sel.startswith("//"):
                page.click(f"xpath={sel}", timeout=5000)
            else:
                page.click(sel, timeout=5000)
            time.sleep(2)
            log.info("Refresh clicked using: %s", sel)
            return True
        except PlaywrightTimeout:
            continue
    return False


def _upload_resume(page):
    try:
        log.info("Looking for dummyUpload button...")

        # Verify the button exists first
        try:
            page.wait_for_selector("input.dummyUpload", timeout=8000)
            log.info("Found dummyUpload button")
        except PlaywrightTimeout:
            log.error("dummyUpload button not found on page")
            _screenshot(page, "no_button")
            return False

        # expect_file_chooser intercepts the OS file dialog before it opens
        # and sets our file directly — no manual clicking needed
        with page.expect_file_chooser(timeout=10000) as fc_info:
            page.click("input.dummyUpload")

        file_chooser = fc_info.value
        file_chooser.set_files(RESUME_PATH)
        log.info("Resume file set: %s", os.path.basename(RESUME_PATH))
        time.sleep(3)

        # Click Save/Upload/Confirm if a dialog appears after file selection
        for confirm in [
            "button:has-text('Save')",
            "button:has-text('Upload')",
            "button:has-text('Confirm')",
            "//button[contains(text(), 'Save')]",
            "//button[contains(text(), 'Upload')]",
        ]:
            try:
                if confirm.startswith("//"):
                    page.click(f"xpath={confirm}", timeout=5000)
                else:
                    page.click(confirm, timeout=5000)
                log.info("Confirmed with: %s", confirm)
                time.sleep(2)
                break
            except PlaywrightTimeout:
                continue

        _screenshot(page, "after_upload")
        return True

    except Exception as e:
        log.error("Upload error: %s", str(e))
        _screenshot(page, "upload_error")
        return False

def _screenshot(page, label):
    path = os.path.join(BASE_DIR, f"screenshot_{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    page.screenshot(path=path)
    log.info("Screenshot saved: %s", path)


if __name__ == "__main__":
    run()
