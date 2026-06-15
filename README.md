# Toyota Echo Service Manual Merger

Scripts to scrape, download, sort, and merge individual PDF sections of the 2000–2002 Toyota Echo factory service manual (RM884U) into a single correctly-ordered document.

## Status
In development.

## Code Conventions

### Script Header Comments
Every script includes a header comment block describing:
- **Filename** and stage/step reference
- **Purpose**: what the script tests or does
- **Expected result**: what success looks like

Example:
```python
# script_name.py
# Stage N, Step N - Brief description
#
# Longer explanation of what this script tests or does,
# and why it matters in the context of the project.
#
# Expected result: what success looks like
```

## Terminology

This project uses the following terms to avoid ambiguity with the manual's own page numbering:

- **Page number** — the chapter-relative number printed in the header of each manual page (e.g., CH-2, CL-1). This is what the manual itself means by "page."
- **Folio number** — the sequential number printed in the footer of each manual page (e.g., 864, 865). Used internally to sort and merge PDF sections into the correct order.
