from bs4 import BeautifulSoup
import re

def parse_page_for_docs(html_content):
    """Parses HTML content to extract documentation-like text and sections."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
        script.decompose()

    # Find relevant content sections (common names in documentation sites)
    main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article', re.I))

    if main_content:
        text = main_content.get_text(separator='\n')
    else:
        text = soup.get_text(separator='\n')

    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text

def extract_code_snippets(html_content):
    """Extracts code snippets from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    snippets = []

    # Common code block tags
    for code in soup.find_all(['code', 'pre']):
        snippets.append(code.get_text())

    return list(set(snippets))
