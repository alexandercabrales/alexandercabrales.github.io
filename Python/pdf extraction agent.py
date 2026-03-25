"""
PDF LEASE EXTRACTION AGENT — Phase 1 Prototype
================================================

This is a learning prototype. It demonstrates the pattern of:
  1. Reading a PDF
  2. Sending text to an LLM with a structured prompt
  3. Getting back structured data (JSON)
  4. Validating the extracted fields
  5. Presenting results for human review

IMPORTANT:
  - This prototype uses the Anthropic API as an example.
    At work, you would swap this for your company's approved
    LLM endpoint (Azure OpenAI, CoPilot Enterprise API, etc.)
  - NEVER run real company documents through a personal API key.
  - This is for learning with FAKE data only.

TO RUN:
  pip install pdfplumber anthropic
  export ANTHROPIC_API_KEY="your-key-here"
  python3 pdf_extraction_agent.py sample_lease.pdf
"""

import sys
import json
import pdfplumber


# ============================================================
# COMPONENT 1: PDF TEXT EXTRACTION
# ============================================================
# This function takes a PDF file path and returns the raw text.
# For digitally-generated PDFs (from Word/DocuSign), this works
# reliably. For scanned paper documents, you'd need OCR instead.
# ============================================================

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    Returns the full text as a single string.
    """
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += f"\n--- Page {i + 1} ---\n"
                full_text += page_text

    return full_text


# ============================================================
# COMPONENT 2: THE EXTRACTION PROMPT
# ============================================================
# This is the most important part of the agent. The prompt tells
# the LLM exactly what fields to extract and how to format them.
#
# You would customize this for YOUR database fields. The fields
# below match what you described: doc name, doc date, index
# number, and real estate entities.
# ============================================================

EXTRACTION_PROMPT = """You are a commercial real estate document data extraction agent.

Read the following lease document text and extract EXACTLY these fields.
Return ONLY valid JSON — no markdown, no explanation, no preamble.

Required fields:
{
  "doc_name": "The document title or type (e.g., 'Commercial Lease Agreement')",
  "doc_date": "The effective date or execution date in YYYY-MM-DD format",
  "tenant_entity": "The full legal entity name of the tenant",
  "landlord_entity": "The full legal entity name of the landlord",
  "premises_address": "The full street address of the leased premises",
  "store_number": "The store number if mentioned, otherwise null",
  "lease_commencement": "The lease commencement date in YYYY-MM-DD format",
  "lease_expiration": "The lease expiration date in YYYY-MM-DD format",
  "base_rent_psf": "The base rent per square foot per annum as a number",
  "monthly_rent": "The monthly rent amount as a number",
  "square_footage": "The rentable square footage as a number",
  "security_deposit": "The security deposit amount as a number",
  "annual_escalation": "The annual rent escalation percentage as a number or description",
  "renewal_options": "Description of renewal options",
  "ti_allowance_psf": "Tenant improvement allowance per square foot as a number",
  "ti_allowance_total": "Total tenant improvement allowance as a number",
  "permitted_use": "Brief description of the permitted use"
}

If a field is not found in the document, set its value to null.
Do not guess or infer — only extract what is explicitly stated.

DOCUMENT TEXT:
"""


# ============================================================
# COMPONENT 3: LLM CALL
# ============================================================
# This function sends the extracted text + prompt to an LLM
# and gets back structured JSON.
#
# THIS PROTOTYPE uses the Anthropic API as an example.
# At work, you would replace this with your approved endpoint:
#   - Azure OpenAI (if your company uses Microsoft Azure)
#   - Microsoft Graph API for CoPilot
#   - Any other approved LLM endpoint
#
# The PATTERN is the same regardless of which LLM you use:
#   1. Build the prompt (system + user message)
#   2. Send it to the API
#   3. Parse the JSON response
# ============================================================

def call_llm(document_text: str) -> dict:
    """
    Send document text to LLM and get structured extraction.
    Returns a dictionary of extracted fields.
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        print("\n[INFO] Anthropic library not installed.")
        print("  Install with: pip install anthropic")
        print("  Or replace this function with your approved LLM endpoint.\n")
        print("  For now, running in DEMO MODE with simulated extraction.\n")
        return None

    import os
    api_key = "INSERT_API_KEY_HERE"

    if not api_key:
        print("\n[INFO] No ANTHROPIC_API_KEY environment variable found.")
        print("  Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("  For now, running in DEMO MODE with simulated extraction.\n")
        return None

    # Build the full prompt
    full_prompt = EXTRACTION_PROMPT + document_text

    # Call the API
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )

    # Parse the response
    response_text = message.content[0].text

    # Clean up response in case the LLM wraps it in markdown
    response_text = response_text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]
    response_text = response_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse LLM response as JSON: {e}")
        print(f"  Raw response: {response_text[:500]}")
        return None


# ============================================================
# DEMO MODE: SIMULATED EXTRACTION
# ============================================================
# If you don't have an API key set up yet, the agent runs in
# demo mode using simple text search. This shows you what the
# OUTPUT looks like so you understand the pattern.
#
# In a real agent, the LLM does this work much more reliably.
# ============================================================

def demo_extraction(text: str) -> dict:
    """
    Simple keyword-based extraction for demo purposes.
    This is NOT how a real agent works — it's just to show
    the output format while you're learning.
    """
    print("[DEMO MODE] Using simple text matching instead of LLM.")
    print("  Set up an API key to see real AI extraction.\n")

    result = {
        "doc_name": None,
        "doc_date": None,
        "tenant_entity": None,
        "landlord_entity": None,
        "premises_address": None,
        "store_number": None,
        "lease_commencement": None,
        "lease_expiration": None,
        "base_rent_psf": None,
        "monthly_rent": None,
        "square_footage": None,
        "security_deposit": None,
        "annual_escalation": None,
        "renewal_options": None,
        "ti_allowance_psf": None,
        "ti_allowance_total": None,
        "permitted_use": None
    }

    # Very basic text matching — the LLM does this 100x better
    if "COMMERCIAL LEASE AGREEMENT" in text:
        result["doc_name"] = "Commercial Lease Agreement"

    if "March 15, 2026" in text:
        result["doc_date"] = "2026-03-15"

    if "GOLDEN STATE RETAIL HOLDINGS INC" in text:
        result["tenant_entity"] = "GOLDEN STATE RETAIL HOLDINGS INC."

    if "PACIFIC GATEWAY PROPERTIES LLC" in text:
        result["landlord_entity"] = "PACIFIC GATEWAY PROPERTIES LLC"

    if "8750 Fremont Boulevard" in text:
        result["premises_address"] = "8750 Fremont Boulevard, Fremont, California 94538"

    if "Store #847" in text:
        result["store_number"] = "847"

    if "July 1, 2026" in text:
        result["lease_commencement"] = "2026-07-01"

    if "June 30, 2036" in text:
        result["lease_expiration"] = "2036-06-30"

    if "$47.50 per square foot" in text:
        result["base_rent_psf"] = 47.50

    if "$49,479.17" in text:
        result["monthly_rent"] = 49479.17

    if "12,500 rentable square feet" in text:
        result["square_footage"] = 12500

    if "$98,958.34" in text:
        result["security_deposit"] = 98958.34

    if "three percent (3%)" in text:
        result["annual_escalation"] = "3% annually"

    if "two (2) options to renew" in text:
        result["renewal_options"] = "Two 5-year renewal options at fair market rent"

    if "$35.00 per rentable square foot" in text:
        result["ti_allowance_psf"] = 35.00

    if "$437,500.00" in text:
        result["ti_allowance_total"] = 437500.00

    if "retail discount department store" in text:
        result["permitted_use"] = "Retail discount department store"

    return result


# ============================================================
# COMPONENT 4: VALIDATION
# ============================================================
# After extraction, run basic sanity checks on the data.
# These catch obvious errors before human review.
# ============================================================

def validate_extraction(data: dict) -> list:
    """
    Run validation checks on extracted data.
    Returns a list of warnings (empty list = all good).
    """
    warnings = []

    # Check for missing critical fields
    critical_fields = ["doc_name", "doc_date", "tenant_entity",
                       "landlord_entity", "premises_address"]
    for field in critical_fields:
        if data.get(field) is None:
            warnings.append(f"MISSING: {field} — could not be extracted")

    # Check date format
    for date_field in ["doc_date", "lease_commencement", "lease_expiration"]:
        val = data.get(date_field)
        if val and not (len(val) == 10 and val[4] == "-" and val[7] == "-"):
            warnings.append(f"FORMAT: {date_field} = '{val}' — expected YYYY-MM-DD")

    # Check rent is positive
    if data.get("base_rent_psf") is not None and data["base_rent_psf"] <= 0:
        warnings.append(f"VALUE: base_rent_psf = {data['base_rent_psf']} — should be positive")

    if data.get("monthly_rent") is not None and data["monthly_rent"] <= 0:
        warnings.append(f"VALUE: monthly_rent = {data['monthly_rent']} — should be positive")

    # Check square footage is reasonable
    if data.get("square_footage") is not None:
        sf = data["square_footage"]
        if sf < 500 or sf > 500000:
            warnings.append(f"VALUE: square_footage = {sf} — seems unusual")

    # Cross-check: monthly rent should roughly equal (PSF * SF / 12)
    if (data.get("base_rent_psf") and data.get("square_footage")
            and data.get("monthly_rent")):
        expected_monthly = round(data["base_rent_psf"] * data["square_footage"] / 12, 2)
        actual_monthly = data["monthly_rent"]
        diff_pct = abs(expected_monthly - actual_monthly) / expected_monthly * 100
        if diff_pct > 5:
            warnings.append(
                f"CROSS-CHECK: monthly_rent (${actual_monthly:,.2f}) doesn't match "
                f"PSF * SF / 12 (${expected_monthly:,.2f}) — {diff_pct:.1f}% difference"
            )

    return warnings


# ============================================================
# COMPONENT 5: HUMAN REVIEW DISPLAY
# ============================================================
# Present the extracted data in a clear format for review.
# In a real tool, this could be a web interface or a form.
# For this prototype, it's a clean terminal display.
# ============================================================

def display_for_review(data: dict, warnings: list, pdf_path: str):
    """
    Display extracted data for human review.
    """
    print("=" * 64)
    print("  PDF EXTRACTION AGENT — RESULTS FOR HUMAN REVIEW")
    print("=" * 64)
    print(f"  Source: {pdf_path}")
    print("-" * 64)

    # Group fields by category for readability
    categories = {
        "Document Info": ["doc_name", "doc_date"],
        "Entities": ["landlord_entity", "tenant_entity"],
        "Premises": ["premises_address", "store_number", "square_footage"],
        "Term": ["lease_commencement", "lease_expiration"],
        "Financials": ["base_rent_psf", "monthly_rent", "security_deposit",
                       "annual_escalation"],
        "Other Terms": ["renewal_options", "ti_allowance_psf",
                        "ti_allowance_total", "permitted_use"]
    }

    for category, fields in categories.items():
        print(f"\n  {category}")
        print(f"  {'—' * 40}")
        for field in fields:
            value = data.get(field)
            if value is None:
                display_val = "[NOT FOUND]"
            elif isinstance(value, float):
                display_val = f"${value:,.2f}" if value > 100 else f"{value}"
            else:
                display_val = str(value)

            # Format field name for display
            display_name = field.replace("_", " ").title()
            print(f"  {display_name:<25} {display_val}")

    # Show warnings
    if warnings:
        print(f"\n  {'!' * 50}")
        print(f"  WARNINGS ({len(warnings)})")
        print(f"  {'!' * 50}")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print(f"\n  All validation checks passed.")

    print(f"\n{'=' * 64}")
    print("  NEXT STEP: Verify these values against the PDF,")
    print("  then enter into your database.")
    print("=" * 64)

    # Also save as JSON for programmatic use
    output_file = pdf_path.replace(".pdf", "_extracted.json")
    with open(output_file, "w") as f:
        json.dump({
            "source_file": pdf_path,
            "extracted_data": data,
            "warnings": warnings
        }, f, indent=2)
    print(f"\n  JSON saved to: {output_file}")


# ============================================================
# MAIN: PUT IT ALL TOGETHER
# ============================================================

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_extraction_agent.py <path-to-lease.pdf>")
        print("Example: python3 pdf_extraction_agent.py sample_lease.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # Step 1: Extract text from PDF
    print(f"\n[1/4] Reading PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print("[ERROR] No text extracted from PDF.")
        print("  This might be a scanned document that needs OCR.")
        sys.exit(1)

    print(f"  Extracted {len(text)} characters from {pdf_path}")

    # Step 2: Send to LLM for extraction
    print(f"\n[2/4] Sending to LLM for field extraction...")
    extracted = call_llm(text)

    # Fall back to demo mode if no API key
    if extracted is None:
        extracted = demo_extraction(text)

    # Step 3: Validate
    print(f"\n[3/4] Running validation checks...")
    warnings = validate_extraction(extracted)
    print(f"  {len(warnings)} warning(s) found")

    # Step 4: Display for human review
    print(f"\n[4/4] Preparing results for review...\n")
    display_for_review(extracted, warnings, pdf_path)


if __name__ == "__main__":
    main()
