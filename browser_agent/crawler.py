import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def crawl_async(url):
    """Crawl a URL using Playwright for headless browsing."""
    print(f"🕷️ Async crawling: {url}")
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Use a realistic User-Agent
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })

            # Go to the URL and wait for the network to be idle
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Get the rendered HTML
            content = await page.content()
            await browser.close()
            
            # Extract text content
            soup = BeautifulSoup(content, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator='\n')

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            print(f"⚠️ Playwright crawling {url} failed: {e}")
            return ""

def crawl(url):
    """Synchronous wrapper for async_crawl."""
    try:
        return asyncio.run(crawl_async(url))
    except Exception as e:
        print(f"⚠️ Crawl error: {e}")
        return ""
