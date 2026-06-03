# Flask Hello World

A minimal, visually polished Flask web application that serves a "Hello, World!" landing page with a modern gradient background, animated card component, and Google Fonts.

---

## Prerequisites

- Python **3.11** or higher
- `pip` (bundled with Python)
- Git (optional, for cloning)

---

## Project Structure

```
.
├── app.py                  # Flask application entry point
├── templates/
│   └── index.html          # Jinja2 landing page template
├── static/
│   └── css/
│       └── style.css       # All CSS styles and animations
├── tests/
│   └── test_app.py         # pytest unit tests
├── requirements.txt        # Pinned dependencies
└── README.md               # This file
```

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create and activate a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Verify Flask is installed:

```bash
flask --version
```

Expected output (versions may vary slightly):
```
Python 3.11.x
Flask 3.0.3
Werkzeug 3.0.x
```

---

## Running the Application

```bash
python app.py
```

The development server starts on **http://localhost:5000**.  
Open that URL in Chrome or Firefox to see the landing page.

Alternatively, use the Flask CLI:

```bash
flask --app app run --debug
```

---

## Running the Tests

Make sure your virtual environment is active, then run:

```bash
pytest
```

Expected output:

```
========================= test session starts ==========================
collected 3 items

tests/test_app.py ...                                            [100%]

========================== 3 passed in 0.xxs ===========================
```

### Test coverage

| Test | Description |
|------|-------------|
| `test_index_returns_200` | GET / returns HTTP 200 OK |
| `test_index_content_type_is_html` | Response Content-Type contains `text/html` |
| `test_index_body_contains_hello_world` | Response body contains `"Hello, World!"` |

---

## Screenshot

> _Screenshot placeholder — run the app and visit http://localhost:5000 to see the live result._

![Landing page preview](screenshot.png)

---

## Tech Stack

| Technology | Version |
|------------|---------|
| Python | 3.11+ |
| Flask | 3.0.3 |
| Jinja2 | 3.1 (bundled with Flask) |
| pytest | 8.2.2 |
| Google Fonts | Poppins (CDN) |

---

## License

MIT