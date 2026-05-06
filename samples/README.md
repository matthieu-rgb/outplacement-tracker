# Samples - outplacement-tracker v0.1

This folder contains sample documents generated with fictional, anonymised data
for demonstration purposes.

## Available files

| File | Description |
|---|---|
| `sample_pdf_output_de.pdf` | Cumulative PDF DE - Max Mustermann - 3 fictional months |
| `sample_pdf_output_en.pdf` | Cumulative PDF EN - John Doe - 3 fictional months |
| `sample_output_de.docx` | Source Word document (DE) before conversion |
| `sample_output_en.docx` | Source Word document (EN) before conversion |
| `build_samples.py` | Python generation script |

## Fictional data

All data is entirely fictional. No real person is represented.

**Participant DE:** Max Mustermann, Beraterin Maria Schmidt
**Participant EN:** John Doe, Advisor Maria Schmidt

Three months of monthly updates are included (January to March 2026). Sections for
updates 04 to 12 are empty, illustrating the template behaviour for months not yet
submitted.

## Regenerating the samples

Prerequisites: python-docx installed, LibreOffice present on the machine.

```bash
cd /path/to/outplacement-tracker
python3 samples/build_samples.py
```

On a machine without LibreOffice, the script produces the .docx files but not the
PDFs. Open the .docx files in Microsoft Word and export to PDF manually.

## GDPR note

These files contain no real personal data.
The names "Max Mustermann" and "John Doe" are conventional placeholder names used
as demonstration data in the German and English-speaking contexts respectively.
No real email address, case number or identifying information is present.
