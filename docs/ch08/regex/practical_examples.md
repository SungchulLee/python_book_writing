# Practical Examples

!!! tip "Mental Model"
    Regex shines in four everyday tasks: *validating* input format, *extracting* structured fields from messy text, *cleaning* data by replacing or removing unwanted patterns, and *splitting* text on flexible delimiters. Each recipe here maps to one of those four tasks — once you recognize which category your problem falls in, the pattern almost writes itself.

## Data Cleaning

### Normalizing Whitespace

```python
import re

raw = "  Hello,\t\tWorld!  \n  Too   many   spaces.  "

# Collapse all whitespace to single space, strip edges
cleaned = re.sub(r'\s+', ' ', raw).strip()
print(cleaned)
# 'Hello, World! Too many spaces.'
```

### Removing Non-ASCII Characters

```python
import re

text = "Café résumé naïve"

# Remove non-ASCII
re.sub(r'[^\x00-\x7F]+', '', text)
# 'Caf rsum nave'

# Keep only alphanumeric and basic punctuation
re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)
# 'Caf rsum nave'
```

### Cleaning Financial Data

```python
import re

prices = ["\$1,234.56", "€ 2,100.00", "¥10,000", "\$42", "N/A"]

def extract_number(s):
    """Extract numeric value from a price string."""
    cleaned = re.sub(r'[^\d.]', '', s)
    if cleaned:
        return float(cleaned)
    return None

for p in prices:
    print(f"{p:>12} → {extract_number(p)}")
#    \$1,234.56 → 1234.56
#   € 2,100.00 → 2100.0
#      ¥10,000 → 10000.0
#          \$42 → 42.0
#          N/A → None
```

## Validation Patterns

### Email Validation

```python
import re

# Simplified email pattern (covers most common formats)
EMAIL_RE = re.compile(r"""
    ^
    [\w.+-]+          # local part: word chars, dots, plus, hyphen
    @                 # at sign
    [\w-]+            # domain name
    (?:\.[\w-]+)*     # optional subdomains
    \.                # dot before TLD
    [a-zA-Z]{2,}      # TLD (at least 2 letters)
    $
""", re.VERBOSE)

tests = [
    "user@example.com",
    "first.last+tag@sub.domain.co.uk",
    "not-an-email",
    "@missing-local.com",
    "missing-domain@",
    "spaces not@allowed.com",
]

for t in tests:
    valid = "✓" if EMAIL_RE.match(t) else "✗"
    print(f"  {valid} {t}")
#   ✓ user@example.com
#   ✓ first.last+tag@sub.domain.co.uk
#   ✗ not-an-email
#   ✗ @missing-local.com
#   ✗ missing-domain@
#   ✗ spaces not@allowed.com
```

### Date Validation

```python
import re

DATE_RE = re.compile(r"""
    ^
    (?P<year>\d{4})     # year: 4 digits
    [-/]                # separator
    (?P<month>0[1-9]|1[0-2])   # month: 01-12
    [-/]                # separator
    (?P<day>0[1-9]|[12]\d|3[01])  # day: 01-31
    $
""", re.VERBOSE)

tests = ["2024-01-15", "2024/12/31", "2024-13-01", "2024-00-15", "24-01-15"]
for t in tests:
    m = DATE_RE.match(t)
    status = f"✓ {m.groupdict()}" if m else "✗"
    print(f"  {status} ← {t}")
#   ✓ {'year': '2024', 'month': '01', 'day': '15'} ← 2024-01-15
#   ✓ {'year': '2024', 'month': '12', 'day': '31'} ← 2024/12/31
#   ✗ ← 2024-13-01
#   ✗ ← 2024-00-15
#   ✗ ← 24-01-15
```

### IP Address Validation

```python
import re

# Match IPv4 addresses (0.0.0.0 to 255.255.255.255)
IP_RE = re.compile(r"""
    ^
    (?:
        (?:25[0-5]|2[0-4]\d|[01]?\d\d?)   # octet: 0-255
        \.                                   # dot
    ){3}
    (?:25[0-5]|2[0-4]\d|[01]?\d\d?)       # last octet (no trailing dot)
    $
""", re.VERBOSE)

tests = ["192.168.1.1", "255.255.255.255", "0.0.0.0", "256.1.1.1", "1.2.3"]
for t in tests:
    valid = "✓" if IP_RE.match(t) else "✗"
    print(f"  {valid} {t}")
#   ✓ 192.168.1.1
#   ✓ 255.255.255.255
#   ✓ 0.0.0.0
#   ✗ 256.1.1.1
#   ✗ 1.2.3
```

## Log Parsing

### Apache/Nginx Access Log

```python
import re

LOG_RE = re.compile(r"""
    (?P<ip>[\d.]+)              # IP address
    \s+-\s+-\s+                 # identd and user (usually - -)
    \[(?P<date>[^\]]+)\]        # date in brackets
    \s+
    "(?P<method>\w+)            # HTTP method
    \s+(?P<path>\S+)            # request path
    \s+(?P<proto>[^"]+)"        # protocol
    \s+(?P<status>\d{3})        # status code
    \s+(?P<size>\d+|-)          # response size
""", re.VERBOSE)

log_line = '192.168.1.100 - - [15/Jan/2024:10:30:45 +0000] "GET /api/data HTTP/1.1" 200 1234'

match = LOG_RE.match(log_line)
if match:
    info = match.groupdict()
    for k, v in info.items():
        print(f"  {k:>8}: {v}")
#        ip: 192.168.1.100
#      date: 15/Jan/2024:10:30:45 +0000
#    method: GET
#      path: /api/data
#     proto: HTTP/1.1
#    status: 200
#      size: 1234
```

### Python Traceback Extraction

```python
import re

traceback_text = """
Traceback (most recent call last):
  File "main.py", line 42, in process_data
    result = compute(data)
  File "utils.py", line 15, in compute
    return data / 0
ZeroDivisionError: division by zero
"""

# Extract file, line number, and function name
FRAME_RE = re.compile(r'File "(?P<file>[^"]+)", line (?P<line>\d+), in (?P<func>\w+)')

for m in FRAME_RE.finditer(traceback_text):
    print(m.groupdict())
# {'file': 'main.py', 'line': '42', 'func': 'process_data'}
# {'file': 'utils.py', 'line': '15', 'func': 'compute'}

# Extract the exception type and message
exc_match = re.search(r'^(\w+Error): (.+)$', traceback_text, re.M)
if exc_match:
    print(f"Exception: {exc_match.group(1)}")  # ZeroDivisionError
    print(f"Message: {exc_match.group(2)}")     # division by zero
```

## Text Transformation

### Markdown to Plain Text

```python
import re

md = """
# Main Title
This is **bold** and *italic* text.
Here's a [link](https://example.com) and `inline code`.
- List item 1
- List item 2
"""

def md_to_plain(text):
    text = re.sub(r'^#+\s+', '', text, flags=re.M)       # headers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)         # bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)              # italic
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)      # links
    text = re.sub(r'`(.+?)`', r'\1', text)                # inline code
    text = re.sub(r'^[-*]\s+', '• ', text, flags=re.M)   # list items
    return text.strip()

print(md_to_plain(md))
# Main Title
# This is bold and italic text.
# Here's a link and inline code.
# • List item 1
# • List item 2
```

### CamelCase ↔ snake_case

```python
import re

def camel_to_snake(name):
    """Convert camelCase or PascalCase to snake_case."""
    # Insert underscore before uppercase letters
    s = re.sub(r'(?<=[a-z0-9])([A-Z])', r'_\1', name)
    # Handle consecutive uppercase (e.g., HTTPResponse → http_response)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    return s.lower()

def snake_to_camel(name):
    """Convert snake_case to camelCase."""
    parts = name.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])

print(camel_to_snake("myVariableName"))    # my_variable_name
print(camel_to_snake("HTTPResponse"))       # http_response
print(camel_to_snake("getHTTPSUrl"))        # get_https_url

print(snake_to_camel("my_variable_name"))  # myVariableName
print(snake_to_camel("http_response"))      # httpResponse
```

## Financial Data Patterns

### Ticker and Price Extraction

```python
import re

text = """
AAPL closed at \$182.63 (+1.25%)
GOOGL rose to \$141.80 (-0.34%)
MSFT ended at \$378.91 (+0.89%)
"""

STOCK_RE = re.compile(r'(?P<ticker>[A-Z]{1,5})\s+\w+\s+\w+\s+\$(?P<price>[\d.]+)\s+\((?P<change>[+-][\d.]+%)\)')

for m in STOCK_RE.finditer(text):
    d = m.groupdict()
    print(f"  {d['ticker']:>5}: ${d['price']} ({d['change']})")
#    AAPL: \$182.63 (+1.25%)
#   GOOGL: \$141.80 (-0.34%)
#    MSFT: \$378.91 (+0.89%)
```

### CSV Line Parser

```python
import re

def parse_csv_line(line):
    """Parse a CSV line handling quoted fields with commas."""
    pattern = r'(?:"([^"]*(?:""[^"]*)*)"|([^,]*))'
    fields = []
    for quoted, unquoted in re.findall(pattern, line):
        field = quoted.replace('""', '"') if quoted else unquoted
        fields.append(field.strip())
    return [f for f in fields if f or f == '']

line = 'John,"New York, NY",42,"He said ""hi"""'
print(parse_csv_line(line))
# ['John', 'New York, NY', '42', 'He said "hi"']
```

## Common Regex Recipes

| Task | Pattern |
|---|---|
| Integer | `r'[+-]?\d+'` |
| Float | `r'[+-]?\d*\.?\d+'` |
| Scientific notation | `r'[+-]?\d*\.?\d+(?:[eE][+-]?\d+)?'` |
| Hex color | `r'#[0-9a-fA-F]{3,6}\b'` |
| US phone | `r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'` |
| URL | `r'https?://\S+'` |
| Email (simple) | `r'[\w.+-]+@[\w-]+\.[\w.]+'` |
| IP address | `r'\b(?:\d{1,3}\.){3}\d{1,3}\b'` |
| ISO date | `r'\d{4}-\d{2}-\d{2}'` |
| Blank lines | `r'^\s*$'` with `re.M` |
| Duplicate words | `r'\b(\w+)\s+\1\b'` |
| HTML tags | `r'<[^>]+>'` |

!!! tip "Regex Is Not Always the Answer"
    For structured formats like JSON, XML, HTML, or CSV, prefer dedicated parsers (`json`, `xml.etree`, `html.parser`, `csv` modules). Regex is best for semi-structured text, validation, and simple extraction tasks.

## Summary

| Category | Key Takeaway |
|---|---|
| Data cleaning | `re.sub()` for normalization; extract numbers from messy strings |
| Validation | `re.fullmatch()` with verbose patterns for readable validators |
| Log parsing | Named groups + `finditer()` for structured extraction |
| Transformation | Backreferences in `re.sub()` for reordering and reformatting |
| Financial data | Combine named groups with specific numeric patterns |
| When NOT to use | Prefer dedicated parsers for JSON, XML, HTML, CSV |

---

## Runnable Example: `practical_applications_tutorial.py`

```python
"""
Python Regular Expressions - Tutorial 07: Practical Applications
================================================================

This tutorial demonstrates real-world applications of regex patterns.

DIFFICULTY: ADVANCED
"""

import re

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*70)
    print("REAL-WORLD REGEX PATTERNS")
    print("="*70)

    # Email validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    emails = ["user@example.com", "invalid@", "test@test.co.uk"]
    print("\nEmail Validation:")
    for email in emails:
        valid = bool(re.match(email_pattern, email))
        print(f"  {'✓' if valid else '✗'} {email}")

    # URL validation
    url_pattern = r"^https?://(?:www\.)?[\w.-]+\.\w+(?:/[\w./?%&=-]*)?$"
    urls = ["https://example.com", "http://www.test.org/page", "invalid"]
    print("\nURL Validation:")
    for url in urls:
        valid = bool(re.match(url_pattern, url))
        print(f"  {'✓' if valid else '✗'} {url}")

    # Phone number formatting
    phone_text = "Call 5551234567 or 8005551234"
    phone_pattern = r"(\d{3})(\d{3})(\d{4})"
    formatted = re.sub(phone_pattern, r"() -", phone_text)
    print(f"\nPhone Formatting:\n  Before: {phone_text}\n  After: {formatted}")

    # Extract all links from HTML
    html = '<a href="http://example.com">Link</a> <a href="http://test.org">Test</a>'
    link_pattern = r'href="(https?://[^"]+)"'
    links = re.findall(link_pattern, html)
    print(f"\nExtracted Links: {links}")

    # Data extraction from logs
    log = "2024-03-15 14:30:45 ERROR Connection failed"
    log_pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)"
    match = re.search(log_pattern, log)
    if match:
        print(f"\nLog Parsing:")
        print(f"  Date: {match.group(1)}")
        print(f"  Time: {match.group(2)}")
        print(f"  Level: {match.group(3)}")
        print(f"  Message: {match.group(4)}")

    # Text cleaning
    text = "Hello!!!  How are   you???  "
    cleaned = re.sub(r'\s+', ' ', text).strip()
    cleaned = re.sub(r'([!?]){2,}', r'', cleaned)
    print(f"\nText Cleaning:\n  Before: '{text}'\n  After: '{cleaned}'")

    # IP address validation
    ip_pattern = r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
    ips = ["192.168.1.1", "256.1.1.1", "10.0.0.1"]
    print("\nIP Address Validation:")
    for ip in ips:
        valid = bool(re.match(ip_pattern, ip))
        print(f"  {'✓' if valid else '✗'} {ip}")

    print("\n" + "="*70)
    print("END OF TUTORIAL - All concepts completed!")
    print("="*70)
```


---

## Runnable Example: `regex_web_scraping_tutorial.py`

```python
"""
Topic 7.10 - Regex for Web Scraping and Data Extraction Tutorial

Real-world regex patterns for extracting structured data from
semi-structured web content (HTML, JSON-in-HTML, API responses).

When APIs aren't available, web scraping often requires parsing raw HTML
or embedded JSON to extract the data you need. Regex is the tool for this:
find patterns in messy text and pull out clean, structured fields.

This tutorial builds a complete pipeline:
  raw text → regex extraction → deduplication → pandas DataFrame → CSV

Inspired by a Starbucks store location scraper that parses store data
(ID, name, latitude, longitude, city, state, zip) from web responses.

Learning Objectives:
- Writing multi-group regex patterns for structured data extraction
- Extracting repeated records from large text blocks
- Non-greedy matching (.*?) to avoid over-matching
- Named groups for readability
- Deduplication patterns for scraped data
- Building DataFrames from extracted data
- Combining regex with pandas for data pipelines

Prerequisites:
- ch07/regex (regex basics, groups, quantifiers)
- ch10/core (pandas DataFrame basics)
- ch15/networking (HTTP requests, web scraping)

Author: Python Educator
Date: 2024
"""

import re
import csv
import json
from typing import Any


# ============================================================================
# PART 1: BEGINNER - Extracting Fields from Structured Text
# ============================================================================

def demonstrate_basic_field_extraction():
    """
    Extract key-value pairs from semi-structured text using regex groups.

    Web APIs and HTML pages often embed data in predictable formats.
    Regex groups let you extract specific fields from these patterns.
    """
    print("=" * 70)
    print("BEGINNER: Extracting Fields from Structured Text")
    print("=" * 70)

    # --- Extracting from JSON-like text ---
    print("\n1. Extracting from JSON-like text in HTML")
    print("-" * 50)

    # Simulate text embedded in a web page (common in store locators)
    html_fragment = '''
    <script>var storeData = {"storeNumber":"12345","name":"Downtown Plaza",
    "coordinates":{"latitude":34.0522,"longitude":-118.2437},
    "address":{"city":"Los Angeles","state":"CA","postalCode":"90012"}};
    </script>
    '''

    # Extract store number
    store_num = re.search(r'"storeNumber":"(\d+)"', html_fragment)
    if store_num:
        print(f"   Store number: {store_num.group(1)}")

    # Extract store name
    store_name = re.search(r'"name":"([^"]+)"', html_fragment)
    if store_name:
        print(f"   Store name  : {store_name.group(1)}")

    # Extract latitude and longitude
    lat = re.search(r'"latitude":([-\d.]+)', html_fragment)
    lon = re.search(r'"longitude":([-\d.]+)', html_fragment)
    if lat and lon:
        print(f"   Latitude    : {lat.group(1)}")
        print(f"   Longitude   : {lon.group(1)}")

    # Extract city
    city = re.search(r'"city":"([^"]+)"', html_fragment)
    if city:
        print(f"   City        : {city.group(1)}")

    # --- Non-greedy vs greedy matching ---
    print(f"\n2. Non-greedy matching: .*? vs .*")
    print("-" * 50)

    text = '"name":"First Store","other":"data","name":"Second Store"'

    # Greedy: .* grabs as much as possible
    greedy = re.search(r'"name":"(.*)"', text)
    print(f"   Greedy  .*  : {greedy.group(1) if greedy else 'None'}")
    # Gets: First Store","other":"data","name":"Second Store

    # Non-greedy: .*? grabs as little as possible
    nongreedy = re.search(r'"name":"(.*?)"', text)
    print(f"   Non-greedy .*? : {nongreedy.group(1) if nongreedy else 'None'}")
    # Gets: First Store

    print("\n   Key insight: Use .*? when extracting from quoted values")
    print("   to stop at the FIRST closing quote, not the last one.")

    # --- Named groups for readability ---
    print(f"\n3. Named groups (?P<name>...) for readability")
    print("-" * 50)

    log_line = '2024-03-15 14:30:45 [ERROR] Server: Connection refused (port 5432)'

    pattern = (
        r'(?P<date>\d{4}-\d{2}-\d{2}) '
        r'(?P<time>\d{2}:\d{2}:\d{2}) '
        r'\[(?P<level>\w+)\] '
        r'(?P<source>\w+): '
        r'(?P<message>.+)'
    )

    match = re.search(pattern, log_line)
    if match:
        print(f"   date    = {match.group('date')}")
        print(f"   time    = {match.group('time')}")
        print(f"   level   = {match.group('level')}")
        print(f"   source  = {match.group('source')}")
        print(f"   message = {match.group('message')}")
        print(f"\n   As dict: {match.groupdict()}")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: INTERMEDIATE - Multi-Record Extraction from Web Content
# ============================================================================

def demonstrate_multi_record_extraction():
    """
    Extract multiple records from a block of text using regex.

    Web pages often contain many similar data records (store listings,
    product cards, search results). The strategy:
    1. Use re.findall() or re.finditer() to find all record boundaries
    2. Extract fields from each record with groups
    """
    print("=" * 70)
    print("INTERMEDIATE: Extracting Multiple Records")
    print("=" * 70)

    # Simulate a web response with multiple store records
    # This mimics what a store locator API might return embedded in HTML
    response_text = '''
    {"stores":[
        {"storeNumber":"10234","name":"Main St & 5th","coordinates":
         {"latitude":34.0522,"longitude":-118.2437},"address":
         {"city":"Los Angeles","countrySubdivisionCode":"CA","postalCode":"90012"},"slug":"main-st"},
        {"storeNumber":"10567","name":"Hollywood & Vine","coordinates":
         {"latitude":34.1017,"longitude":-118.3267},"address":
         {"city":"Hollywood","countrySubdivisionCode":"CA","postalCode":"90028"},"slug":"hollywood"},
        {"storeNumber":"10891","name":"Venice Boardwalk","coordinates":
         {"latitude":33.9850,"longitude":-118.4695},"address":
         {"city":"Venice","countrySubdivisionCode":"CA","postalCode":"90291"},"slug":"venice"},
        {"storeNumber":"10234","name":"Main St & 5th","coordinates":
         {"latitude":34.0522,"longitude":-118.2437},"address":
         {"city":"Los Angeles","countrySubdivisionCode":"CA","postalCode":"90012"},"slug":"duplicate"}
    ]}
    '''

    # --- Step 1: Split into individual records ---
    print("\n1. Finding individual records with re.findall()")
    print("-" * 50)

    # Each record runs from "storeNumber" to "slug"
    record_pattern = r'"storeNumber":.*?"slug"'
    records = re.findall(record_pattern, response_text, re.DOTALL)
    print(f"   Found {len(records)} records")

    # --- Step 2: Extract fields from each record ---
    print(f"\n2. Extracting fields with multi-group pattern")
    print("-" * 50)

    # This pattern uses 7 capturing groups to extract all fields at once
    field_pattern = (
        r'"storeNumber":"(.*?)"'       # Group 1: store ID
        r'.*?"name":"(.*?)"'           # Group 2: store name
        r'.*?"latitude":([\d.-]+)'     # Group 3: latitude
        r'.*?"longitude":([\d.-]+)'    # Group 4: longitude
        r'.*?"city":"(.*?)"'           # Group 5: city
        r'.*?"countrySubdivisionCode":"(.*?)"'  # Group 6: state
        r'.*?"postalCode":"(.*?)"'     # Group 7: zip code
    )

    extracted = []
    for record in records:
        match = re.search(field_pattern, record, re.DOTALL)
        if match:
            extracted.append(match.groups())
            store_id, name, lat, lon, city, state, zip_code = match.groups()
            print(f"   Store {store_id}: {name}")
            print(f"     Location: ({lat}, {lon})")
            print(f"     Address:  {city}, {state} {zip_code}")
            print()

    # --- Alternative: re.findall with groups returns list of tuples ---
    print("3. Shortcut: re.findall() with groups")
    print("-" * 50)

    # When the pattern has groups, findall returns list of tuples
    all_matches = re.findall(field_pattern, response_text, re.DOTALL)
    print(f"   re.findall returned {len(all_matches)} tuples")
    for m in all_matches:
        print(f"   {m[0]}: {m[1]} in {m[4]}, {m[5]}")

    print("\n" + "=" * 70 + "\n")
    return all_matches


# ============================================================================
# PART 3: INTERMEDIATE - Deduplication Patterns
# ============================================================================

def demonstrate_deduplication(records: list[tuple]) -> list[tuple]:
    """
    Deduplicate scraped records.

    Web scraping often produces duplicates because:
    - The same item appears on multiple pages
    - Search regions overlap (nearby zip codes)
    - Pagination issues

    Args:
        records: List of tuples (store_id, name, lat, lon, city, state, zip)

    Returns:
        Deduplicated list
    """
    print("=" * 70)
    print("INTERMEDIATE: Deduplication Patterns for Scraped Data")
    print("=" * 70)

    print(f"\n   Records before dedup: {len(records)}")

    # --- Method 1: Track seen IDs ---
    print(f"\n1. Method 1: Track seen IDs with a set")
    print("-" * 50)

    seen_ids = set()
    unique_records = []
    duplicates = 0

    for record in records:
        store_id = record[0]
        if store_id not in seen_ids:
            seen_ids.add(store_id)
            unique_records.append(record)
        else:
            duplicates += 1
            print(f"   Duplicate found: store {store_id} ({record[1]})")

    print(f"   After dedup: {len(unique_records)} unique, {duplicates} removed")

    # --- Method 2: dict.fromkeys() preserves order ---
    print(f"\n2. Method 2: dict keyed by ID (preserves insertion order)")
    print("-" * 50)

    store_dict = {}
    for record in records:
        store_id = record[0]
        if store_id not in store_dict:
            store_dict[store_id] = record

    unique_via_dict = list(store_dict.values())
    print(f"   Result: {len(unique_via_dict)} unique records")

    # --- Method 3: Using pandas (for large datasets) ---
    print(f"\n3. Method 3: pandas drop_duplicates (best for large data)")
    print("-" * 50)
    print("   import pandas as pd")
    print("   df = pd.DataFrame(records, columns=[...])")
    print("   df = df.drop_duplicates(subset=['store_id'])")
    print("   # Handles thousands of records efficiently")

    # --- Why sets work well here ---
    print(f"\n4. Why set-based dedup is O(n)")
    print("-" * 50)
    print("   set.add() and 'in set' are both O(1) average case")
    print("   Looping through n records: n × O(1) = O(n)")
    print("   vs. list-based 'if id in seen_list': O(n) per check → O(n²)")
    print("   For 10,000 records: set is ~10,000x faster than list!")

    print("\n" + "=" * 70 + "\n")
    return unique_records


# ============================================================================
# PART 4: INTERMEDIATE - Building a DataFrame from Scraped Data
# ============================================================================

def demonstrate_dataframe_construction(records: list[tuple]):
    """
    Convert extracted records into a structured pandas DataFrame.

    This is the typical final step in a scraping pipeline:
    raw text → regex → tuples → DataFrame → CSV/analysis
    """
    print("=" * 70)
    print("INTERMEDIATE: Building a DataFrame from Scraped Data")
    print("=" * 70)

    columns = ["store_id", "name", "latitude", "longitude",
               "city", "state", "zip_code"]

    # --- Method 1: From list of tuples ---
    print(f"\n1. DataFrame from list of tuples")
    print("-" * 50)

    # We'll use a simulated dataset here (real scraping would use actual data)
    sample_records = [
        ("10234", "Main St & 5th",       "34.0522", "-118.2437", "Los Angeles", "CA", "90012"),
        ("10567", "Hollywood & Vine",     "34.1017", "-118.3267", "Hollywood",   "CA", "90028"),
        ("10891", "Venice Boardwalk",     "33.9850", "-118.4695", "Venice",      "CA", "90291"),
        ("11023", "Pasadena Old Town",    "34.1478", "-118.1445", "Pasadena",    "CA", "91101"),
        ("11156", "Santa Monica Pier",    "34.0094", "-118.4973", "Santa Monica","CA", "90401"),
        ("11289", "Beverly Hills Plaza",  "34.0736", "-118.4004", "Beverly Hills","CA","90210"),
        ("11422", "Downtown Arts Dist",   "34.0402", "-118.2351", "Los Angeles", "CA", "90013"),
        ("11555", "Glendale Galleria",    "34.1456", "-118.2551", "Glendale",    "CA", "91210"),
        ("11688", "Burbank Media Dist",   "34.1808", "-118.3090", "Burbank",     "CA", "91502"),
        ("11821", "Long Beach Pike",      "33.7675", "-118.1924", "Long Beach",  "CA", "90802"),
    ]

    # Direct construction — most common approach
    # (importing pandas only if available, since this is a regex tutorial)
    try:
        import pandas as pd

        df = pd.DataFrame(sample_records, columns=columns)

        # Convert numeric columns from strings
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)

        print(f"   Shape: {df.shape}")
        print(f"   Dtypes:\n{df.dtypes}")
        print(f"\n   Preview:")
        print(df[["store_id", "name", "city", "zip_code"]].to_string(index=False))

        # --- Quick analysis ---
        print(f"\n2. Quick analysis of scraped data")
        print("-" * 50)

        print(f"   Total stores    : {len(df)}")
        print(f"   Unique cities   : {df['city'].nunique()}")
        print(f"   Stores per city :")
        city_counts = df["city"].value_counts()
        for city, count in city_counts.items():
            print(f"     {city}: {count}")

        print(f"\n   Geographic bounds:")
        print(f"     Lat range : {df['latitude'].min():.4f} to {df['latitude'].max():.4f}")
        print(f"     Lon range : {df['longitude'].min():.4f} to {df['longitude'].max():.4f}")

        # --- Save to CSV ---
        print(f"\n3. Saving to CSV")
        print("-" * 50)

        csv_path = "/tmp/scraped_stores.csv"
        df.to_csv(csv_path, index=False)
        print(f"   Saved {len(df)} records to {csv_path}")

        # Verify by reading back
        df_check = pd.read_csv(csv_path)
        print(f"   Verified: read back {len(df_check)} records")

    except ImportError:
        print("   (pandas not available — showing CSV approach instead)")

        # Fallback: pure csv module
        csv_path = "/tmp/scraped_stores.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(sample_records)
        print(f"   Wrote {len(sample_records)} records to {csv_path}")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 5: ADVANCED - Complete Regex Scraping Pipeline
# ============================================================================

def demonstrate_complete_pipeline():
    """
    A complete pipeline that combines all the patterns:
    1. Simulate fetching a web response
    2. Extract records with regex
    3. Clean and normalize fields
    4. Deduplicate
    5. Build DataFrame
    6. Export to CSV

    This mirrors how real web scrapers work.
    """
    print("=" * 70)
    print("ADVANCED: Complete Regex Scraping Pipeline")
    print("=" * 70)

    # --- Step 1: Simulated web response ---
    # In practice, this comes from requests.get(url).text
    print("\n--- Step 1: Receive web response ---")

    response_text = '''
    window.__INITIAL_STATE__ = {"stores":{"items":[
    {"storeNumber":"10234","name":"Main St \\u0026 5th Ave","coordinates":
     {"latitude":34.0522,"longitude":-118.2437},"address":
     {"city":"Los Angeles","countrySubdivisionCode":"CA",
      "postalCode":"90012-1234"},"slug":"main-st"},
    {"storeNumber":"10567","name":"Hollywood \\u0026 Vine","coordinates":
     {"latitude":34.1017,"longitude":-118.3267},"address":
     {"city":"Hollywood ","countrySubdivisionCode":"CA",
      "postalCode":"90028"},"slug":"hw-vine"},
    {"storeNumber":"10891","name":"Venice  Boardwalk","coordinates":
     {"latitude":33.9850,"longitude":-118.4695},"address":
     {"city":"Venice","countrySubdivisionCode":"CA",
      "postalCode":"90291"},"slug":"venice-bw"},
    {"storeNumber":"10234","name":"Main St \\u0026 5th Ave","coordinates":
     {"latitude":34.0522,"longitude":-118.2437},"address":
     {"city":"Los Angeles","countrySubdivisionCode":"CA",
      "postalCode":"90012-1234"},"slug":"main-st-dup"}
    ]}};
    '''

    print(f"   Response length: {len(response_text)} chars")

    # --- Step 2: Extract records ---
    print("\n--- Step 2: Extract records with regex ---")

    record_pattern = r'"storeNumber":.*?"slug"'
    raw_records = re.findall(record_pattern, response_text, re.DOTALL)
    print(f"   Found {len(raw_records)} raw records")

    field_pattern = (
        r'"storeNumber":"(?P<id>.*?)"'
        r'.*?"name":"(?P<name>.*?)"'
        r'.*?"latitude":(?P<lat>[\d.-]+)'
        r'.*?"longitude":(?P<lon>[\d.-]+)'
        r'.*?"city":"(?P<city>.*?)"'
        r'.*?"countrySubdivisionCode":"(?P<state>.*?)"'
        r'.*?"postalCode":"(?P<zip>.*?)"'
    )

    extracted = []
    for record in raw_records:
        match = re.search(field_pattern, record, re.DOTALL)
        if match:
            extracted.append(match.groupdict())

    print(f"   Extracted {len(extracted)} records")
    for rec in extracted:
        print(f"   {rec['id']}: {rec['name']} — {rec['city']}, {rec['state']}")

    # --- Step 3: Clean and normalize ---
    print("\n--- Step 3: Clean and normalize fields ---")

    def clean_record(record: dict) -> dict:
        """
        Clean a single scraped record.

        Common cleaning tasks:
        - Decode unicode escapes (\\u0026 → &)
        - Strip whitespace
        - Normalize zip codes (take first 5 digits)
        - Collapse multiple spaces
        """
        cleaned = {}
        cleaned["store_id"] = record["id"].strip()
        # Decode unicode escapes like \u0026
        cleaned["name"] = (
            record["name"]
            .encode("utf-8")
            .decode("unicode_escape")
            .strip()
        )
        # Collapse multiple spaces
        cleaned["name"] = re.sub(r"\s+", " ", cleaned["name"])
        cleaned["latitude"] = float(record["lat"])
        cleaned["longitude"] = float(record["lon"])
        cleaned["city"] = record["city"].strip()
        cleaned["state"] = record["state"].strip()
        # Normalize zip to 5 digits
        cleaned["zip_code"] = record["zip"][:5]
        return cleaned

    cleaned_records = [clean_record(r) for r in extracted]
    print(f"   Cleaned {len(cleaned_records)} records")
    for rec in cleaned_records:
        print(f"   {rec['store_id']}: {rec['name']} — {rec['city']}, "
              f"{rec['state']} {rec['zip_code']}")

    # --- Step 4: Deduplicate ---
    print("\n--- Step 4: Deduplicate ---")

    seen = set()
    unique = []
    for rec in cleaned_records:
        if rec["store_id"] not in seen:
            seen.add(rec["store_id"])
            unique.append(rec)
        else:
            print(f"   Removed duplicate: {rec['store_id']} ({rec['name']})")

    print(f"   {len(cleaned_records)} → {len(unique)} after dedup")

    # --- Step 5: Build DataFrame ---
    print("\n--- Step 5: Build DataFrame ---")

    try:
        import pandas as pd
        df = pd.DataFrame(unique)
        print(df.to_string(index=False))
    except ImportError:
        for rec in unique:
            print(f"   {rec}")

    # --- Step 6: Save to CSV ---
    print("\n--- Step 6: Save to CSV ---")

    csv_path = "/tmp/scraped_stores_pipeline.csv"
    fieldnames = ["store_id", "name", "latitude", "longitude",
                   "city", "state", "zip_code"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique)

    print(f"   Saved {len(unique)} records to {csv_path}")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 6: ADVANCED - Regex Patterns for Common Web Formats
# ============================================================================

def demonstrate_common_web_patterns():
    """
    A reference of regex patterns commonly needed in web scraping.
    """
    print("=" * 70)
    print("ADVANCED: Common Regex Patterns for Web Scraping")
    print("=" * 70)

    # --- JSON embedded in HTML (window.__DATA__) ---
    print("\n1. Extracting embedded JSON from HTML <script> tags")
    print("-" * 50)

    html = '''
    <html><head>
    <script>window.__INITIAL_DATA__ = {"user":"alice","count":42};</script>
    </head></html>
    '''

    pattern = r'window\.__INITIAL_DATA__\s*=\s*({.*?});'
    match = re.search(pattern, html)
    if match:
        data = json.loads(match.group(1))
        print(f"   Extracted: {data}")
        print(f"   user={data['user']}, count={data['count']}")

    # --- HTML table rows ---
    print(f"\n2. Extracting data from HTML tables")
    print("-" * 50)

    table_html = '''
    <table>
    <tr><td>Apple</td><td>$1.20</td><td>In Stock</td></tr>
    <tr><td>Banana</td><td>$0.50</td><td>Low Stock</td></tr>
    <tr><td>Cherry</td><td>$3.00</td><td>Out of Stock</td></tr>
    </table>
    '''

    row_pattern = r'<tr><td>(.*?)</td><td>\$([\d.]+)</td><td>(.*?)</td></tr>'
    rows = re.findall(row_pattern, table_html)
    print(f"   Found {len(rows)} rows:")
    for name, price, status in rows:
        print(f"   {name}: ${price} ({status})")

    # --- Coordinates from various formats ---
    print(f"\n3. Extracting coordinates from various formats")
    print("-" * 50)

    texts = [
        'Located at lat: 34.0522, lng: -118.2437',
        'GPS: (40.7128, -74.0060)',
        '"latitude":51.5074,"longitude":-0.1278',
        'position="48.8566,2.3522"',
    ]

    coord_patterns = [
        (r'lat:\s*([\d.-]+),\s*lng:\s*([\d.-]+)', "lat/lng format"),
        (r'\(([\d.-]+),\s*([\d.-]+)\)', "parenthesized format"),
        (r'"latitude":([\d.-]+).*?"longitude":([\d.-]+)', "JSON format"),
        (r'position="([\d.-]+),([\d.-]+)"', "attribute format"),
    ]

    for text, (pattern, fmt) in zip(texts, coord_patterns):
        match = re.search(pattern, text)
        if match:
            print(f"   {fmt}: ({match.group(1)}, {match.group(2)})")

    # --- Meta tags and Open Graph ---
    print(f"\n4. Extracting meta tags from HTML")
    print("-" * 50)

    html_head = '''
    <meta name="description" content="Best coffee shop in LA">
    <meta property="og:title" content="Starbucks - Main St">
    <meta property="og:image" content="https://example.com/store.jpg">
    '''

    meta_pattern = r'<meta\s+(?:name|property)="([^"]+)"\s+content="([^"]+)"'
    metas = re.findall(meta_pattern, html_head)
    for name, content in metas:
        print(f"   {name}: {content}")

    # --- Pagination links ---
    print(f"\n5. Extracting pagination info")
    print("-" * 50)

    pagination_html = '''
    <a href="/stores?page=1">1</a>
    <a href="/stores?page=2">2</a>
    <a href="/stores?page=3" class="current">3</a>
    <a href="/stores?page=4">4</a>
    <a href="/stores?page=5">Next</a>
    '''

    page_pattern = r'href="/stores\?page=(\d+)"'
    pages = re.findall(page_pattern, pagination_html)
    print(f"   Available pages: {pages}")
    print(f"   Last page: {max(int(p) for p in pages)}")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print(" " * 8 + "REGEX FOR WEB SCRAPING AND DATA EXTRACTION")
    print(" " * 20 + "Complete Tutorial")
    print("=" * 70 + "\n")

    # Beginner
    demonstrate_basic_field_extraction()

    # Intermediate
    records = demonstrate_multi_record_extraction()
    unique_records = demonstrate_deduplication(records)
    demonstrate_dataframe_construction(unique_records)

    # Advanced
    demonstrate_complete_pipeline()
    demonstrate_common_web_patterns()

    print("\n" + "=" * 70)
    print("Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Use .*? (non-greedy) to extract quoted values")
    print("2. Multi-group patterns extract several fields at once")
    print("3. re.findall() with groups returns list of tuples")
    print("4. Named groups (?P<name>...) improve readability")
    print("5. Always deduplicate scraped data (use sets for O(n))")
    print("6. Clean data before analysis: strip, normalize, convert types")
    print("7. Pipeline: fetch → regex → clean → dedup → DataFrame → CSV")
    print("8. re.DOTALL flag lets . match newlines in multi-line content")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Write a function `extract_emails` that takes a text string and returns a list of all email addresses found in it. Use a regex pattern that matches common email formats. Test with a string containing emails mixed with other text.

??? success "Solution to Exercise 1"

    ```python
    import re

    def extract_emails(text):
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.findall(pattern, text)

    # Test
    text = "Contact alice@example.com or bob.smith@test.org. Not an email: @invalid"
    print(extract_emails(text))
    # ['alice@example.com', 'bob.smith@test.org']
    ```

---

**Exercise 2.**
Write a function `clean_phone_numbers` that takes a list of phone number strings in various formats (`"(555) 123-4567"`, `"555.123.4567"`, `"555-123-4567"`) and returns them all in a standardized format `"555-123-4567"`. Use `re.sub` to strip non-digit characters first, then reformat.

??? success "Solution to Exercise 2"

    ```python
    import re

    def clean_phone_numbers(phones):
        result = []
        for phone in phones:
            digits = re.sub(r'\D', '', phone)
            if len(digits) == 10:
                formatted = f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
                result.append(formatted)
        return result

    # Test
    phones = ["(555) 123-4567", "555.123.4567", "555-123-4567"]
    print(clean_phone_numbers(phones))
    # ['555-123-4567', '555-123-4567', '555-123-4567']
    ```

---

**Exercise 3.**
Write a function `parse_csv_line` that takes a single CSV line string and correctly handles quoted fields (which may contain commas). For example, `'Alice,"New York, NY",30'` should return `["Alice", "New York, NY", "30"]`. Use `re.findall` with a pattern that handles both quoted and unquoted fields.

??? success "Solution to Exercise 3"

    ```python
    import re

    def parse_csv_line(line):
        pattern = r'"([^"]*?)"|([^,]+)'
        matches = re.findall(pattern, line)
        return [quoted or unquoted for quoted, unquoted in matches]

    # Test
    line = 'Alice,"New York, NY",30'
    print(parse_csv_line(line))
    # ['Alice', 'New York, NY', '30']
    ```
