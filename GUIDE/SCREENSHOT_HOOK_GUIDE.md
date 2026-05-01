# 📸 SCREENSHOT HOOK DOCUMENTATION

## Overview

The **Screenshot Hook** is an automated system that captures browser screenshots when tests fail, providing visual evidence of what went wrong.

---

## 🎯 What It Does

| When Test | Action |
|-----------|--------|
| ✅ PASSES | No screenshot (clean run) |
| ❌ FAILS | Automatically capture screenshot |
| ⏭️ SKIPS | No screenshot |

---

## 🔧 How It Works

### Architecture

```
Test Runs
  ↓
Test Fails (Assertion or Exception)
  ↓
pytest_runtest_failed hook triggered
  ↓
capture_failure_screenshot() called
  ↓
Screenshot saved to qa-framework/screenshots/
  ↓
Logged to console and log file
```

---

## 🏗️ Components

### 1. **store_page_reference Fixture**
```python
@pytest.fixture(autouse=True)
def store_page_reference(request, page=None):
    """Store page reference for use in screenshot hook"""
    if page is not None:
        _page_reference[request.node.nodeid] = page
    yield
    # Cleanup after test
```

**Purpose:** Keeps a reference to the browser page so hooks can access it

**Why Needed:** Hooks don't have direct access to fixtures, so we store the page temporarily

---

### 2. **pytest_runtest_failed Hook**
```python
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_failed(item, call):
    """Hook called immediately when a test FAILS"""
    logger.error(f"TEST FAILED: {item.name}")
    
    if item.nodeid in _page_reference:
        page = _page_reference[item.nodeid]
        capture_failure_screenshot(page, item.name)
```

**What It Does:**
- ✅ Detects test failure
- ✅ Retrieves page reference
- ✅ Calls screenshot capture function
- ✅ Logs failure details

**When It Runs:** Immediately after test fails (before cleanup)

---

### 3. **capture_failure_screenshot Function**
```python
def capture_failure_screenshot(page, test_name: str):
    """Capture screenshot when a test fails"""
    
    # 1. Create screenshots directory
    screenshots_dir = Path("qa-framework/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Generate unique filename with milliseconds
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]
    screenshot_filename = f"{test_name}_FAILED_{timestamp}.png"
    screenshot_path = screenshots_dir / screenshot_filename
    
    # 3. Capture screenshot from current page state
    page.screenshot(path=str(screenshot_path))
    
    # 4. Log details about the screenshot
    logger.error(f"✗ SCREENSHOT CAPTURED: {screenshot_path}")
    logger.error(f"  File size: {screenshot_path.stat().st_size / 1024:.1f} KB")
    logger.error(f"  URL at failure: {page.url}")
    logger.error(f"  Title: {page.title()}")
    
    # 5. Return metadata for future use
    return {
        "path": str(screenshot_path),
        "timestamp": timestamp,
        "test_name": test_name,
        "url": page.url,
        "title": page.title(),
        "file_size_kb": screenshot_path.stat().st_size / 1024
    }
```

**What It Does:**
1. Creates `qa-framework/screenshots/` directory if it doesn't exist
2. Generates unique filename: `test_name_FAILED_YYYYMMDD_HHMMSS.png`
3. Captures current state of browser page
4. Logs screenshot path and metadata
5. Returns metadata for report attachment

---

### 4. **pytest_runtest_passed Hook**
```python
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_passed(item, call):
    """Hook called immediately when a test PASSES"""
    logger.info(f"✓ TEST PASSED: {item.name}")
    logger.info(f"  Execution time: {call.stop - call.start:.2f}s")
```

**What It Does:**
- Logs successful test completion
- Tracks execution time
- No screenshot (passing test)

---

## 📊 File Output

### Screenshot Filename Format

```
{test_name}_FAILED_{timestamp}.png
```

### Examples

```
test_smoke_valid_login_FAILED_20260501_143022.png
test_login_negative_FAILED_20260501_143025.png
test_empty_fields_login_FAILED_20260501_143030.png
test_special_characters_FAILED_20260501_143035.png
```

### Directory Structure

```
qa-framework/screenshots/
├── test_login_negative_FAILED_20260501_143025.png        ← 245 KB
├── test_empty_fields_FAILED_20260501_143030.png         ← 312 KB
└── test_special_chars_FAILED_20260501_143035.png        ← 198 KB
```

---

## 🔄 Execution Flow Example

### Test Passes
```
[12:30:22] Starting test: test_smoke_valid_login
[12:30:23] Browser launched for test: test_smoke_valid_login
[12:30:23] [STEP] NAVIGATE: Opening login page
[12:30:23] [STEP] LOGIN: Entering credentials
[12:30:24] [STEP] VERIFY: Checking dashboard visible
[12:30:24] ✓ TEST PASSED: test_smoke_valid_login
[12:30:24]   Execution time: 0.75s
[12:30:24] Closing browser for test: test_smoke_valid_login
```

**Result:** ✅ No screenshot (passing)

---

### Test Fails
```
[12:30:25] Starting test: test_login_negative
[12:30:26] Browser launched for test: test_login_negative
[12:30:26] [STEP] NAVIGATE: Opening login page
[12:30:26] [STEP] LOGIN: Entering invalid credentials
[12:30:27] [STEP] VERIFY: Waiting for error message
[12:30:28] ✗ TEST FAILED: test_login_negative
[12:30:28] ✗ SCREENSHOT CAPTURED: qa-framework/screenshots/test_login_negative_FAILED_20260501_143028.png
[12:30:28]   File size: 245.3 KB
[12:30:28]   URL at failure: https://example.com/app/login
[12:30:28]   Title: Login - Example Application
[12:30:28] Closing browser for test: test_login_negative
```

**Result:** 📸 Screenshot captured automatically

---

## 🎨 Hook Sequence

```
Test Execution
    ↓
Assertion/Exception occurs
    ↓
pytest_runtest_failed ← Hook 1: CAPTURE SCREENSHOT
    ├─ Page is still active with failure state
    ├─ Screenshot captures current screen
    └─ Metadata logged
    ↓
pytest_runtest_makereport ← Hook 2: Record result
    ├─ Test marked as FAILED
    ├─ Duration recorded
    └─ Report updated
    ↓
pytest_runtest_passed ← Hook 3: (if passed)
    ├─ Test marked as PASSED
    └─ Duration recorded
    ↓
Cleanup (conftest page fixture)
    ├─ Browser closed
    ├─ Context closed
    └─ Page reference removed
```

---

## 💾 What Gets Logged

### Console Output (When Test Fails)
```
✗ TEST FAILED: test_login_negative
✗ SCREENSHOT CAPTURED: qa-framework/screenshots/test_login_negative_FAILED_20260501_143028.png
  File size: 245.3 KB
  URL at failure: https://example.com/app/login
  Title: Login - Example Application
```

### Log File Entry
```
2026-05-01 12:30:28 - [ERROR] - conftest - TEST FAILED: test_login_negative
2026-05-01 12:30:28 - [ERROR] - conftest - ✗ SCREENSHOT CAPTURED: qa-framework/screenshots/test_login_negative_FAILED_20260501_143028.png
2026-05-01 12:30:28 - [ERROR] - conftest -   File size: 245.3 KB
2026-05-01 12:30:28 - [ERROR] - conftest -   URL at failure: https://example.com/app/login
2026-05-01 12:30:28 - [ERROR] - conftest -   Title: Login - Example Application
```

---

## 🚀 Usage

### Run Tests with Screenshot Capture

```bash
# Run all tests
pytest qa-framework/tests/ -v

# Run negative tests (designed to test failure path)
pytest qa-framework/tests/negative/ -v

# Run with verbose screenshot logging
pytest qa-framework/tests/ -v -s
```

### View Screenshots

```bash
# List all failure screenshots
ls -la qa-framework/screenshots/

# Open screenshot in image viewer
open qa-framework/screenshots/test_login_negative_FAILED_*.png
```

---

## 🎯 Why This Matters

### Without Screenshot Hook
```
Test failed: test_login_negative
❌ No visual evidence
❌ Don't know what page looked like at failure
❌ Hard to debug UI issues
```

### With Screenshot Hook
```
Test failed: test_login_negative
✓ Screenshot: test_login_negative_FAILED_20260501_143028.png
✓ Can see exact page state
✓ Easy to debug (was button missing? wrong color? etc.)
```

---

## 🔧 Customization

### Capture Screenshots for PASSED Tests

```python
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_passed(item, call):
    """Capture screenshot for ALL tests (optional)"""
    if item.nodeid in _page_reference:
        page = _page_reference[item.nodeid]
        # Capture screenshot even on pass
        capture_screenshot(page, item.name, status="PASSED")
```

---

### Custom Screenshot Path

```python
def capture_failure_screenshot(page, test_name: str, custom_dir: str = None):
    """Capture with custom directory"""
    screenshots_dir = Path(custom_dir or "qa-framework/screenshots")
    # ... rest of code ...
```

---

### Screenshot with DOM Dump

```python
def capture_failure_screenshot(page, test_name: str):
    """Capture screenshot AND save HTML"""
    # Save screenshot
    page.screenshot(path=screenshot_path)
    
    # ALSO save HTML for inspection
    page.content()  # or page.save_as(html_path)
```

---

## 🐛 Troubleshooting

### Issue 1: No Screenshots Being Captured

#### ❌ Problem
```
Test fails but no screenshot in qa-framework/screenshots/
```

#### ✅ Solution
Check that:
1. Page fixture is being used in test
2. `store_page_reference` fixture is not skipped
3. Playwright is not in headless mode (check conftest.py)

```python
# In conftest.py
browser = p.chromium.launch(headless=True)  # ✓ Should work
```

---

### Issue 2: Screenshots Are Blank

#### ❌ Problem
```
Screenshot exists but shows blank page
```

#### ✅ Solution
Add wait for page to load:

```python
def test_something(page):
    log.step("NAVIGATE", "Going to page")
    page.goto("https://example.com")
    page.wait_for_load_state("networkidle")  # ← Add this
    # ... rest of test ...
```

---

### Issue 3: Screenshot Capture Too Slow

#### ❌ Problem
```
Tests are much slower with screenshot capture
```

#### ✅ Solution
Screenshots only capture on failure, so no performance impact on passing tests.

For optimization:
```python
# Capture full page screenshot (default)
page.screenshot(path=str(screenshot_path))

# Or capture viewport only (faster)
page.screenshot(path=str(screenshot_path), full_page=False)
```

---

## 📋 Complete Example Test

```python
from utils.logger import TestLogger
import pytest

log = TestLogger(__name__)

@pytest.mark.negative
@pytest.mark.p1
def test_invalid_login(page):
    """
    This test will fail and trigger screenshot capture.
    """
    log.info("=" * 50)
    log.info("TEST: Negative - Invalid Login")
    log.info("=" * 50)
    
    log.step("NAVIGATE", "Opening login page")
    page.goto("https://example.com/login")
    
    log.step("LOGIN", "Entering invalid credentials")
    page.fill("input[name=username]", "wronguser")
    page.fill("input[name=password]", "wrongpass")
    page.click("button[type=submit]")
    
    log.step("VERIFY", "Checking error message")
    error_message = page.locator(".error-message")
    
    # This should pass, but let's intentionally fail to see screenshot
    assert error_message.is_visible(), "Error message should appear"
```

**When this test fails:**
- ✓ Screenshot is automatically captured
- ✓ Path logged to console and file
- ✓ Metadata shows URL, title, file size
- ✓ Screenshot available in `qa-framework/screenshots/`

---

## 🎓 Key Concepts

| Concept | Explanation |
|---------|-------------|
| **Hook** | Pytest function that runs at specific test lifecycle points |
| **pytest_runtest_failed** | Hook called when test fails |
| **pytest_runtest_passed** | Hook called when test passes |
| **tryfirst=True** | Hook runs as early as possible |
| **Fixture Reference** | Store fixture objects for use in hooks |
| **Timestamp** | Unique identifier with milliseconds |
| **Metadata** | Screenshot info (URL, title, size) |

---

## ✅ Summary

The screenshot hook system provides:
- ✅ Automatic screenshot capture on test failure
- ✅ Unique filename with timestamp
- ✅ Detailed metadata logging
- ✅ No performance impact on passing tests
- ✅ Easy debugging of UI issues
- ✅ Visual evidence for bug reports

**Created:** May 1, 2026  
**Feature Level:** Level 3 (Advanced)  
**Status:** ✅ Production Ready
