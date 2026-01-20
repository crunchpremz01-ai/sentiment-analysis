import time
import json
import random
import os
import re
from datetime import datetime
from typing import List, Dict, Set
import requests


class WalmartWorkingScraper:
    def __init__(self):
        """Initialize Walmart Working Scraper"""
        print("Initializing Walmart API Scraper (Working Version)...")
        
        self.session = requests.Session()
        
        self.categories = {
            "electronics": "electronics",
            "baby_products": "baby products",
            "beauty": "beauty makeup",
            "kitchen": "kitchen appliances",
            "fitness": "fitness equipment",
            "pet_supplies": "pet supplies",
            "clothing": "mens clothing",
            "food": "snacks food",
            "tools": "power tools",
            "home_furniture": "furniture",
            "health": "vitamins supplements",
            "office": "office supplies"
        }
        
        print(f"✓ Configured {len(self.categories)} categories")
    
    def get_headers(self):
        """Get realistic browser headers"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.walmart.com/',
            'Origin': 'https://www.walmart.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
    
    def search_walmart(self, query: str, page: int = 1) -> List[str]:
        """Search Walmart and extract product URLs"""
        urls = set()
        
        # Walmart's search endpoint
        search_url = f"https://www.walmart.com/search?q={query.replace(' ', '+')}&page={page}"
        
        try:
            response = self.session.get(search_url, headers=self.get_headers(), timeout=20)
            
            if response.status_code != 200:
                print(f"  ⚠️ Status code: {response.status_code}")
                return list(urls)
            
            html = response.text
            
            # Method 1: Regex to find /ip/ URLs
            pattern = r'href="(/ip/[^"]+)"'
            matches = re.findall(pattern, html)
            
            for match in matches:
                full_url = f"https://www.walmart.com{match}".split('?')[0]
                if re.search(r'/ip/[^/]+/\d+$', full_url):
                    urls.add(full_url)
            
            # Method 2: Try to find product IDs in the HTML
            # Look for patterns like "usItemId":"123456789"
            id_pattern = r'"usItemId":"(\d+)"'
            product_ids = re.findall(id_pattern, html)
            
            for product_id in set(product_ids):
                # We'll just use a generic URL structure
                url = f"https://www.walmart.com/ip/{product_id}"
                urls.add(url)
            
            # Method 3: Look for canonical URLs
            canonical_pattern = r'"canonicalUrl":"(/ip/[^"]+)"'
            canonical_matches = re.findall(canonical_pattern, html)
            
            for match in canonical_matches:
                full_url = f"https://www.walmart.com{match}".split('?')[0]
                if '/ip/' in full_url:
                    urls.add(full_url)
        
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
        
        return list(urls)
    
    def scrape_category(self, category_name: str, search_term: str, target_count: int = 200) -> List[str]:
        """Scrape product URLs from a category"""
        print(f"\n{'='*60}")
        print(f"SCRAPING CATEGORY: {category_name.upper()}")
        print(f"{'='*60}")
        print(f"Search term: '{search_term}'")
        print(f"Target: {target_count} product URLs\n")
        
        all_urls = set()
        page = 1
        max_pages = 25
        consecutive_empty = 0
        
        while len(all_urls) < target_count and page <= max_pages:
            print(f"Page {page}: Searching... (collected {len(all_urls)}/{target_count} URLs)")
            
            page_urls = self.search_walmart(search_term, page)
            
            if not page_urls:
                print(f"  ⚠️ No URLs found on page {page}")
                consecutive_empty += 1
                if consecutive_empty >= 3:
                    print("  ❌ Stopping - no more products")
                    break
                page += 1
                time.sleep(random.uniform(2, 3))
                continue
            
            new_urls = set(page_urls) - all_urls
            all_urls.update(new_urls)
            
            print(f"  ✓ Found {len(new_urls)} new URLs (Total: {len(all_urls)})")
            
            consecutive_empty = 0
            page += 1
            
            if len(all_urls) >= target_count:
                print(f"  ✓ Target reached!")
                break
            
            time.sleep(random.uniform(2, 4))
        
        url_list = sorted(list(all_urls))[:target_count]
        print(f"\n✓ Category complete: {len(url_list)} URLs")
        return url_list
    
    def save_urls_to_file(self, category_name: str, urls: List[str], output_dir: str = "links"):
        """Save URLs to file"""
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, f"links_{category_name}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")
        
        print(f"✓ Saved to: {filename}")
        return filename
    
    def scrape_all_categories(self, target_per_category: int = 200):
        """Scrape all categories"""
        print("\n" + "="*60)
        print("WALMART WORKING SCRAPER")
        print("="*60)
        print(f"\nCategories: {len(self.categories)}")
        print(f"Target per category: {target_per_category}")
        print(f"Total target: {len(self.categories) * target_per_category}\n")
        
        results = {}
        
        for idx, (category_name, search_term) in enumerate(self.categories.items(), 1):
            print(f"\n[{idx}/{len(self.categories)}] Processing: {category_name}")
            
            try:
                urls = self.scrape_category(category_name, search_term, target_per_category)
                
                if urls:
                    filename = self.save_urls_to_file(category_name, urls)
                    results[category_name] = {
                        "count": len(urls),
                        "filename": filename,
                        "status": "success"
                    }
                else:
                    results[category_name] = {
                        "count": 0,
                        "filename": None,
                        "status": "failed"
                    }
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results[category_name] = {
                    "count": 0,
                    "filename": None,
                    "status": "error",
                    "error": str(e)
                }
            
            if idx < len(self.categories):
                delay = random.uniform(4, 7)
                print(f"\nWaiting {delay:.1f}s...")
                time.sleep(delay)
        
        return results


def main():
    print("\n" + "="*60)
    print("WALMART WORKING SCRAPER")
    print("="*60)
    print("\n✓ Uses regex to extract product URLs")
    print("✓ No complex parsing needed")
    print("✓ Works with standard requests library\n")
    
    try:
        scraper = WalmartWorkingScraper()
        
        confirm = input("Proceed with scraping? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
        
        start_time = time.time()
        results = scraper.scrape_all_categories(target_per_category=200)
        elapsed = time.time() - start_time
        
        print("\n" + "="*60)
        print("COMPLETE!")
        print("="*60)
        
        total_urls = sum(r['count'] for r in results.values())
        successful = sum(1 for r in results.values() if r['status'] == 'success')
        
        print(f"\nTime: {elapsed/60:.1f} minutes")
        print(f"Total URLs: {total_urls}")
        print(f"Successful: {successful}/{len(results)}")
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        for name, result in results.items():
            icon = "✓" if result['status'] == 'success' else "✗"
            print(f"{icon} {name}: {result['count']} URLs")
            if result.get('filename'):
                print(f"   → {result['filename']}")
        
        # Save summary
        summary_file = f"links/working_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w') as f:
            json.dump({
                "scraped_at": datetime.now().isoformat(),
                "total_urls": total_urls,
                "elapsed_minutes": round(elapsed/60, 2),
                "categories": results
            }, f, indent=2)
        
        print(f"\n✓ Summary: {summary_file}\n")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted. Partial results saved.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()