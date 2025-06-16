OpenAlex
=========

This script uses the OpenAlex API to query for UWinnipeg-affiliated items. It currently packages up the harvested metadata and item into the standard DSpace Simple Archive Format (see below).

There are three files in this script (excluding testing code):
- harvest_oa_records.py: main script
- openalex.py: business logic for consuming the OpenAlex API and outputting DSpace content
- openalex_record.py: handles the parsing of individual records (JSon -> Dublin Core)

The main script is harvest_oa_records.py, which 
- queries OpenAlex with the UWinnipeg ID
- Parses the results
- Outputs DSpace data

The business logic is in openalex.py, which specifies

- the OpenAlex base URL
- The UWinnipeg ID
- The base directory for output

openalex.py includes the following functions:

- create_base_dirs: creates the directory structure for output
- query: actually queries the OpenAlex API
- total_results: extracts a total record count from the returned data
- write_csv: writes the results as a CSV
- parse_results: parses the API data
- process_record: create a Dublin Core record for each record in the API data
- write_dspace_data: outputs the parsed data in Dspace Simple Archive Format

The DSpace Simple Archive Format structure:

<base_directory>/
  item_000/
    dublin_core.xml
    metadata_[prefix].xml (optional)
    contents
    collections (optional)
    file1.doc
    file2.doc
  item_001/.
    dublin_core.xml
    metadata_[prefix].xml (optional)
    contents
    collections (optional)
    file1.doc
    file2.doc
etc.

The actual record-processing work happens in openalex_record.py

openalex_record.py includes the following functions:

- check_pdf: see if record includes a PDF URL
- fetch_authors: extract all authors for a record
- fetch_keywords: extract all keywords for a record
- fetch_pdf: download item PDF if available
- build_record: construct the Dublin Core record
- write_dublin_core_file: writes an individual Dublin Core record to disk
