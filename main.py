import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Sử dụng biến môi trường
os.environ["AGENTQL_API_KEY"] = os.getenv("AGENTQL_API_KEY")

import agentql
from playwright.sync_api import sync_playwright

def scrape_toolify():
    results = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True
        )
        page = agentql.wrap(browser.new_page())
        page.goto("https://www.toolify.ai/vi/new")

        TOOLS_QUERY = """
        {
          newly_launched {
            ai_tools {
              name
              description 
              tags[]
            }
          }
        }
        """

        response = page.query_data(TOOLS_QUERY)
        
        if isinstance(response, dict) and 'newly_launched' in response:
            tool = response['newly_launched']['ai_tools']
            if isinstance(tool, dict):
                results.append({
                    "name": tool.get('name', ''),
                    "description": tool.get('description', ''),
                    "tags": tool.get('tags', [])
                })
        
        browser.close()
    return results

if __name__ == '__main__':
    try:
        results = scrape_toolify()
        print("Kết quả thu thập được:")
        for tool in results:
            print(f"\nTên: {tool['name']}")
            print(f"Mô tả: {tool['description']}")
            print(f"Tags: {', '.join(tool['tags'])}")
    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")
