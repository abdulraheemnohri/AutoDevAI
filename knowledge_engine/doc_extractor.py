import re

def extract_sections(doc_content):
    """Extracts structured sections (headers and paragraphs) from Markdown content."""
    sections = []
    lines = doc_content.splitlines()

    current_section = None
    current_content = []

    for line in lines:
        # Check for headers (e.g., # Header, ## Header)
        header_match = re.match(r'^(#+)\s+(.+)$', line)
        if header_match:
            if current_section:
                sections.append({
                    "title": current_section,
                    "content": "\n".join(current_content).strip()
                })
            current_section = header_match.group(2)
            current_content = []
        else:
            current_content.append(line)

    # Add the last section
    if current_section:
        sections.append({
            "title": current_section,
            "content": "\n".join(current_content).strip()
        })
    elif current_content:
        # If no headers found, return as one section
        sections.append({
            "title": "General",
            "content": "\n".join(current_content).strip()
        })

    return sections
