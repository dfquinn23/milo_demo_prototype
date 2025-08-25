MILO Demo Sample Data
=====================
Client: Delgado Family Trust

Folder Layout (drop-in for your `/data` folder):
├─ emails.csv
├─ portfolio.csv
├─ ips.yaml
└─ transcripts/
   ├─ 2025-01-15_strategy_checkin.txt
   └─ 2025-06-30_midyear_review.txt

File Schemas
------------
1) emails.csv
   - date (YYYY-MM-DD)
   - from, to (email address strings)
   - subject (short text)
   - body (free text)
   - thread_id (optional, used to thread conversations)
   - client_id (optional label used for filtering/partitioning)

2) transcripts/*.txt
   - File naming: YYYY-MM-DD_<slug>.txt
   - First line should contain date and meeting type (free text).
   - Bullet points encouraged for easy summarization.

3) portfolio.csv
   - ticker (string, e.g., VTI)
   - name (friendly name)
   - weight (0–1 float; must sum to ~1.00)
   - sleeve (Equity | Fixed Income | Real Assets | Cash)

4) ips.yaml
   - client: {name, id}
   - objective: string
   - benchmark: {name, description}
   - return_target: {type, value_pct, note}
   - allocation_policy: {bands per sleeve, rebalancing rules}
   - constraints: {liquidity, prohibited, esg notes}
   - spending_policy: {donor-advised fund timing, etc.}

Notes for Real Client Data
--------------------------
• Keep PII out of cloud-bound paths (use your redaction layer).
• For SharePoint/Graph ingestion, preserve original filenames and last-modified timestamps.
• If you add PDFs/DOCX, store them in a subfolder `docs/` and add a simple manifest.csv with columns:
     filename, doc_type, client_id, date, notes
  Your loader can OCR PDFs and extract text for embeddings before analysis.

Ready to Use
------------
Point DATA_DIR to this folder, or copy its contents into your project's `data/` directory.