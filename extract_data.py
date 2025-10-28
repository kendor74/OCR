import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Your Notion token_v2 cookie from the browser
TOKEN = "v03%3AeyJhbGciOiJkaXIiLCJraWQiOiJwcm9kdWN0aW9uOnRva2VuLXYzOjIwMjQtMTEtMDciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0..IgG8Uk5mVpmS7hhUzVAIYw.QskmSt7MUueGgNM0gu6UQL4YVZWoYfF4KXA7VQ2FX4NygMZcxYpSqZ4MAG7Au5Ja_J0V8YxnGGJBWjy9MkpM2o8qaQNbWgb26e_x6-DL8CHcvC_GF62BtbtM8uD_MJQcj4fW80zn3QJTCHk1SYWIg93kkKMfGtUvcNUsYkPIacQw7JzWp6vYllewS3j7XoO43egTt_nT5pHospVwnOuRTXFx41dlbolbXfbmdAxiuf3RKsJYhl_equ8vFI2OtmrUVhiHN3aK5uyry3gmVwgngWg_M6h5f0wmy7wxU98UxxFmda9TBlH8Alu33CbSJbu71x3U0A-SPJvgtaLrqYqTGGWAgTbdjnqSnao5ivyEcRbo_amRZt8cAIMjoGLXl1gG.4HIr_k2o1IM7a_5gkquAr9Hs8kOPABwa9K1YDdlUrMw"
URL = "https://www.notion.so/axxis/Insurance-Product-Configuration-43bde923d3a9406e915974653fc71504"

async def scrape_notion():
    async with async_playwright() as p:
        # Launch Chromium in headless mode
        browser = await p.chromium.launch(headless=True)

        # Create a browser context with authentication
        context = await browser.new_context(
            storage_state={
                "cookies": [{
                    "name": "token_v2",
                    "value": TOKEN,
                    "domain": ".notion.so",
                    "path": "/"
                }]
            }
        )

        # Open a new page
        page = await context.new_page()
        print(f"🔄 Opening {URL} ...")

        # ✅ FIX 1: Use "domcontentloaded" instead of "networkidle"
        # ✅ FIX 2: Increase timeout to 2 minutes
        await page.goto(URL, wait_until="domcontentloaded", timeout=120000)

        # ✅ FIX 3: Wait 5 extra seconds for lazy-loaded content
        await page.wait_for_timeout(5000)

        # Get the rendered HTML
        html = await page.content()

        # Save raw HTML
        with open("Insurance Product Configuration.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ HTML saved to notion_page_raw.html")

        # Close the browser
        await browser.close()

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        # Extract visible text
        text = soup.get_text(separator="\n", strip=True)

        with open("notion_clean.txt", "w", encoding="utf-8") as f:
            f.write(text)

        print("✅ Clean text saved to notion_clean.txt")

if __name__ == "__main__":
    asyncio.run(scrape_notion())



# import os
# import json
# import pandas as pd
# from notion_client import Client
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize Notion client
# notion = Client(auth=os.getenv("NOTION_API_KEY"))

# # Root database ID (replace if needed)
# ROOT_DATABASE_ID = os.getenv("NOTION_ROOT_DATABASE_ID")

# # ---------------------------------------------------------------------
# # Helper: Get rich text content safely
# def get_text(rich_text_array):
#     """Extracts plain text from Notion's rich_text property."""
#     return "".join([t["plain_text"] for t in rich_text_array]) if rich_text_array else ""

# # ---------------------------------------------------------------------
# # Step 1: Query all pages in a database
# def get_database_pages(database_id):
#     results = []
#     has_more = True
#     next_cursor = None

#     while has_more:
#         response = notion.databases.query(
#             database_id=database_id,
#             start_cursor=next_cursor
#         )
#         results.extend(response["results"])
#         has_more = response.get("has_more", False)
#         next_cursor = response.get("next_cursor", None)

#     return results

# # ---------------------------------------------------------------------
# # Step 2: Recursively extract data from a page (tables, text, sub-pages)
# def extract_page_content(page_id):
#     blocks = []
#     cursor = None
#     while True:
#         response = notion.blocks.children.list(page_id, start_cursor=cursor)
#         blocks.extend(response["results"])
#         if not response.get("has_more"):
#             break
#         cursor = response["next_cursor"]
#     return blocks

# # ---------------------------------------------------------------------
# # Step 3: Process a block to extract tables or text
# def process_block(block):
#     block_type = block["type"]

#     # Handle paragraph text
#     if block_type == "paragraph":
#         return {"type": "text", "content": get_text(block[block_type]["rich_text"])}

#     # Handle table blocks
#     if block_type == "table":
#         table_rows = []
#         table_id = block["id"]
#         table_blocks = extract_page_content(table_id)

#         for row in table_blocks:
#             if row["type"] == "table_row":
#                 cells = row["table_row"]["cells"]
#                 row_data = [get_text(cell) for cell in cells]
#                 table_rows.append(row_data)

#         return {"type": "table", "data": table_rows}

#     # Handle headings
#     if block_type.startswith("heading_"):
#         return {"type": "heading", "content": get_text(block[block_type]["rich_text"])}

#     return None

# # ---------------------------------------------------------------------
# # Step 4: Extract full structured data for one page
# def extract_full_page(page_id, title="Untitled"):
#     print(f"📄 Extracting page: {title}")
#     blocks = extract_page_content(page_id)

#     page_content = []
#     for block in blocks:
#         processed = process_block(block)
#         if processed:
#             page_content.append(processed)

#     return {"page_id": page_id, "title": title, "content": page_content}

# # ---------------------------------------------------------------------
# # Step 5: Main — Export All Pages
# def export_notion_to_json():
#     print("🔄 Fetching pages from database...")
#     pages = get_database_pages(ROOT_DATABASE_ID)

#     all_pages = []
#     for page in pages:
#         page_id = page["id"]
#         title = get_text(page["properties"].get("Name", {}).get("title", []))
#         page_data = extract_full_page(page_id, title)
#         all_pages.append(page_data)

#     # Save everything into JSON
#     with open("notion_export.json", "w", encoding="utf-8") as f:
#         json.dump(all_pages, f, ensure_ascii=False, indent=4)

#     print(f"✅ Export complete! {len(all_pages)} pages saved to notion_export.json")

#     # OPTIONAL: Save tables to CSV for RAG indexing
#     all_tables = []
#     for page in all_pages:
#         for block in page["content"]:
#             if block["type"] == "table":
#                 for row in block["data"]:
#                     all_tables.append({
#                         "page": page["title"],
#                         **{f"col_{i+1}": val for i, val in enumerate(row)}
#                     })

#     if all_tables:
#         df = pd.DataFrame(all_tables)
#         df.to_csv("notion_tables.csv", index=False, encoding="utf-8")
#         print(f"📊 Extracted {len(all_tables)} table rows → notion_tables.csv")

# # Run the export
# if __name__ == "__main__":
#     export_notion_to_json()
