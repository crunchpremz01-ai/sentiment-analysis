import time
import json
import csv
import re
import random
import os
import glob
from datetime import datetime
from typing import List, Dict, Optional
from curl_cffi import requests
from bs4 import BeautifulSoup

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import torch


class WalmartRequestScraper:
    def __init__(self):
        """Initialize the Walmart Request Scraper with RoBERTa sentiment analysis"""
        print("Initializing Request-based Scraper (No Browser)...")
        
        self.fingerprints = [
            "chrome110", "chrome119", "chrome120", "chrome124",
            "safari15_3", "safari15_5", "edge101"
        ]
        
        print("Loading CardiffNLP RoBERTa sentiment model...")
        print("(This may take a moment on first run - downloading model...)")
        
        model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.device = 0 if torch.cuda.is_available() else -1
        device_name = "GPU (CUDA)" if self.device == 0 else "CPU"
        print(f"Using device: {device_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
                truncation=True,
                max_length=512
            )
            
            print(f"✓ RoBERTa sentiment model loaded successfully on {device_name}")
            print("✓ Model: cardiffnlp/twitter-roberta-base-sentiment-latest")
            print("✓ Optimized for social media and review text")
            
        except Exception as e:
            print(f"Error loading RoBERTa model: {e}")
            print("Falling back to rating-based sentiment...")
            self.sentiment_pipeline = None
        
        print("Scraper initialized successfully (Request-based, no browser)")
        
        # Create sentiment folders at startup
        print("\nCreating output folders...")
        os.makedirs("json_files/positive", exist_ok=True)
        os.makedirs("json_files/negative", exist_ok=True)
        os.makedirs("json_files/neutral", exist_ok=True)
        print("✓ Folders ready: json_files/positive, json_files/negative, json_files/neutral")
    
    def human_delay(self, min_sec: float = 2.0, max_sec: float = 5.0):
        """Random delay to mimic human behavior"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    def classify_sentiment(self, review_text: str, rating: Optional[float], title: str = "") -> Dict:
        """Classify review sentiment using RoBERTa"""
        text_to_analyze = f"{title} {review_text}".strip()
        
        if not text_to_analyze:
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "score": 0.0,
                "method": "default"
            }
        
        if self.sentiment_pipeline is None:
            if rating is not None:
                if rating >= 4:
                    return {"sentiment": "positive", "confidence": 0.8, "score": 0.8, "method": "rating_fallback"}
                elif rating <= 2:
                    return {"sentiment": "negative", "confidence": 0.8, "score": 0.2, "method": "rating_fallback"}
                else:
                    return {"sentiment": "neutral", "confidence": 0.7, "score": 0.5, "method": "rating_fallback"}
            else:
                return {"sentiment": "neutral", "confidence": 0.5, "score": 0.5, "method": "default"}
        
        try:
            if len(text_to_analyze) > 2000:
                text_to_analyze = text_to_analyze[:2000]
            
            result = self.sentiment_pipeline(text_to_analyze)[0]
            raw_label = result['label'].lower()
            
            if raw_label in ['negative', 'label_0']:
                sentiment = "negative"
            elif raw_label in ['neutral', 'label_1']:
                sentiment = "neutral"
            elif raw_label in ['positive', 'label_2']:
                sentiment = "positive"
            else:
                sentiment = "neutral"
            
            confidence = result['score']
            
            if sentiment == "negative":
                score = (1 - confidence) * 0.5
            elif sentiment == "neutral":
                score = 0.5
            else:
                score = 0.5 + (confidence * 0.5)
            
            method = "roberta"
            
            if rating is not None:
                if (sentiment == "positive" and rating >= 4) or \
                   (sentiment == "negative" and rating <= 2) or \
                   (sentiment == "neutral" and rating == 3):
                    confidence = min(confidence * 1.1, 1.0)
                    method = "roberta_aligned"
                elif confidence < 0.6:
                    if rating >= 4 and sentiment != "positive":
                        sentiment = "positive"
                        confidence = 0.75
                        score = 0.75
                        method = "roberta_rating_adjusted"
                    elif rating <= 2 and sentiment != "negative":
                        sentiment = "negative"
                        confidence = 0.75
                        score = 0.25
                        method = "roberta_rating_adjusted"
            
            return {
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "score": round(score, 4),
                "roberta_label": result['label'],
                "method": method
            }
            
        except Exception as e:
            print(f"RoBERTa error: {e}")
            if rating is not None:
                if rating >= 4:
                    return {"sentiment": "positive", "confidence": 0.8, "score": 0.8, "method": "rating_fallback"}
                elif rating <= 2:
                    return {"sentiment": "negative", "confidence": 0.8, "score": 0.2, "method": "rating_fallback"}
                else:
                    return {"sentiment": "neutral", "confidence": 0.7, "score": 0.5, "method": "rating_fallback"}
            else:
                return {"sentiment": "neutral", "confidence": 0.5, "score": 0.5, "method": "default"}
    
    def extract_product_id(self, url: str) -> Optional[str]:
        """Extract product ID from Walmart URL"""
        # Remove trailing slashes and query parameters
        clean_url = url.split('?')[0].rstrip('/')
        
        # Extract the last numeric segment after /ip/
        match = re.search(r'/ip/(?:[^/]+/)?(\d+)', clean_url)
        
        if match:
            product_id = match.group(1)
            print(f"✓ Extracted Product ID: {product_id}")
            return product_id
        
        print(f"❌ Could not extract product ID from: {url}")
        return None
    
    def scrape_reviews(self, url: str, product_name: str = None, max_reviews: int = 250) -> Dict:
        """
        Scrape all reviews from a Walmart product page using requests.
        """
        product_id = self.extract_product_id(url)
        
        if not product_id:
            raise ValueError("Invalid Walmart URL. Could not extract product ID.")
        
        print(f"\nProduct ID: {product_id}")
        if product_name:
            print(f"Product Name: {product_name}")
        
        base_reviews_url = f"https://www.walmart.com/reviews/product/{product_id}"
        all_reviews = []
        seen_ids = set()
        current_page = 1
        
        max_possible_pages = (max_reviews // 20) + 5
        consecutive_empty_pages = 0
        consecutive_failures = 0
        MAX_CONSECUTIVE_FAILURES = 3
        MAX_EMPTY_PAGES = 3
        
        print(f"\nCollecting reviews (Target: {max_reviews})...")
        
        while len(all_reviews) < max_reviews and current_page <= max_possible_pages:
            try:
                target_url = f"{base_reviews_url}?page={current_page}&sort=submission-desc"
                current_fingerprint = random.choice(self.fingerprints)
                
                print(f"Page {current_page}: Fetching... (collected {len(all_reviews)}/{max_reviews})")
                
                with requests.Session() as session:
                    response = session.get(target_url, impersonate=current_fingerprint, timeout=30)
                
                if response.status_code != 200:
                    print(f"⚠️ Page {current_page} failed with status {response.status_code}")
                    consecutive_failures += 1
                    
                    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                        print(f"❌ Too many consecutive failures ({consecutive_failures}). Stopping.")
                        break
                    
                    current_page += 1
                    time.sleep(random.uniform(3, 5))
                    continue
                
                consecutive_failures = 0
                
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                
                if not script_tag:
                    print(f"⚠️ No data script found on page {current_page}")
                    consecutive_empty_pages += 1
                    
                    if consecutive_empty_pages >= MAX_EMPTY_PAGES:
                        print(f"❌ Too many pages without data ({consecutive_empty_pages}). Stopping.")
                        break
                    
                    current_page += 1
                    time.sleep(random.uniform(2, 4))
                    continue
                
                try:
                    data = json.loads(script_tag.string)
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing error on page {current_page}: {e}")
                    consecutive_empty_pages += 1
                    
                    if consecutive_empty_pages >= MAX_EMPTY_PAGES:
                        break
                    
                    current_page += 1
                    time.sleep(random.uniform(2, 4))
                    continue
                
                reviews_data = {}
                try:
                    initial_data = data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('data', {})
                    reviews_data = initial_data.get('reviews', {})
                except Exception as e:
                    print(f"⚠️ Error parsing review structure on page {current_page}: {e}")
                    consecutive_empty_pages += 1
                    
                    if consecutive_empty_pages >= MAX_EMPTY_PAGES:
                        break
                    
                    current_page += 1
                    time.sleep(random.uniform(2, 4))
                    continue

                page_reviews_raw = reviews_data.get('customerReviews', [])
                
                if not page_reviews_raw:
                    print(f"⚠️ No reviews found on page {current_page}")
                    consecutive_empty_pages += 1
                    
                    if consecutive_empty_pages >= MAX_EMPTY_PAGES:
                        print(f"❌ No more reviews available after {consecutive_empty_pages} empty pages.")
                        break
                    
                    current_page += 1
                    time.sleep(random.uniform(2, 4))
                    continue

                new_reviews_found_on_page = 0

                for raw_review in page_reviews_raw:
                    if len(all_reviews) >= max_reviews:
                        break

                    review_id = raw_review.get('reviewId')
                    
                    if review_id in seen_ids:
                        continue
                    seen_ids.add(review_id)

                    review_text = raw_review.get('reviewText', '')
                    title = raw_review.get('reviewTitle', '')
                    
                    if not review_text or len(review_text) < 3:
                        continue
                    
                    # Extract rating
                    rating = raw_review.get('rating')
                    
                    # RoBERTa sentiment analysis
                    sentiment_result = self.classify_sentiment(review_text, rating, title)
                    
                    clean_review = {
                        "reviewer_name": raw_review.get('userNickname', 'Anonymous'),
                        "rating": rating,
                        "title": title,
                        "review_text": review_text,
                        "date": raw_review.get('reviewSubmissionTime'),
                        "verified_purchase": any(b.get('id') == 'VerifiedPurchaser' 
                                                for b in raw_review.get('badges', [])),
                        "helpful_count": 0,
                        "sentiment": sentiment_result['sentiment'],
                        "confidence": sentiment_result['confidence'],
                        "score": sentiment_result['score'],
                        "roberta_label": sentiment_result.get('roberta_label', ''),
                        "method": sentiment_result['method']
                    }
                    all_reviews.append(clean_review)
                    new_reviews_found_on_page += 1
                
                if new_reviews_found_on_page > 0:
                    consecutive_empty_pages = 0
                    print(f"✓ Found {new_reviews_found_on_page} new reviews on page {current_page}")
                else:
                    consecutive_empty_pages += 1
                    print(f"⚠️ Page {current_page} yielded 0 new reviews (all duplicates)")
                
                current_page += 1
                time.sleep(random.uniform(2, 4))
                
            except requests.exceptions.Timeout:
                print(f"⚠️ Timeout on page {current_page}")
                consecutive_failures += 1
                if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    break
                current_page += 1
                time.sleep(random.uniform(3, 5))
                
            except Exception as e:
                print(f"⚠️ Unexpected error on page {current_page}: {e}")
                consecutive_failures += 1
                if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                    print(f"❌ Too many errors. Stopping.")
                    break
                current_page += 1
                time.sleep(random.uniform(2, 4))
        
        if not all_reviews:
            raise ValueError("No reviews found. Please try again.")

        print(f"\n✓ Scraping complete: {len(all_reviews)} reviews collected from {current_page - 1} pages")
        
        return {
            "product_id": product_id,
            "product_url": url,
            "product_name": product_name,
            "reviews": all_reviews,
            "scraped_at": datetime.now().isoformat()
        }


def read_urls_from_file(txt_file: str) -> List[str]:
    """Read URLs from a text file, one URL per line"""
    urls = []
    
    if not os.path.exists(txt_file):
        raise FileNotFoundError(f"File not found: {txt_file}")
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    
    return urls


def find_all_link_files(folder_path: str) -> List[str]:
    """Find all .txt files in a folder that contain 'links' in the name"""
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    # Look for files that start with "links_" or are named "links.txt"
    pattern1 = os.path.join(folder_path, "links_*.txt")
    pattern2 = os.path.join(folder_path, "links.txt")
    
    files = glob.glob(pattern1) + glob.glob(pattern2)
    
    # Exclude _completed.txt files
    files = [f for f in files if '_completed.txt' not in f]
    
    return sorted(files)


def mark_url_as_completed(txt_file: str, completed_url: str, product_id: str = None):
    """Remove completed URL from original file and add it to completed file"""
    try:
        if not os.path.exists(txt_file):
            return
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        remaining_lines = []
        for line in lines:
            if line.strip() and completed_url not in line:
                remaining_lines.append(line)
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.writelines(remaining_lines)
        
        completed_file = txt_file.replace('.txt', '_completed.txt')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(completed_file, 'a', encoding='utf-8') as f:
            if product_id:
                f.write(f"{completed_url} # Completed at {timestamp} | Product ID: {product_id}\n")
            else:
                f.write(f"{completed_url} # Completed at {timestamp}\n")
        
        print(f"✓ Marked as completed")
        
    except Exception as e:
        print(f"Warning: Could not update URL files: {e}")


def main():
    """Main scraping function"""
    
    print("\n" + "="*60)
    print("WALMART BATCH FOLDER SCRAPER - RoBERTa SENTIMENT")
    print("="*60)
    print("\nUsing CardiffNLP Twitter-RoBERTa Model")
    print("✓ Scrapes all link files in a folder")
    print("✓ Auto-resume support")
    print("✓ GPU-accelerated (if CUDA available)")
    print("✓ Request-based (No Browser, Fast)\n")
    
    scraper = None
    
    try:
        print("Choose input method:")
        print("1. Enter a single URL manually")
        print("2. Load URLs from a single text file")
        print("3. Batch process all link files in a folder")
        choice = input("Enter choice (1, 2, or 3): ").strip()
        
        if choice == "3":
            # BATCH FOLDER MODE
            folder_path = input("\nEnter folder path (e.g., 'links' or 'C:/data/links'): ").strip()
            
            if not folder_path:
                folder_path = "links"
            
            print(f"\nSearching for link files in: {folder_path}")
            link_files = find_all_link_files(folder_path)
            
            if not link_files:
                print(f"\n❌ No link files found in {folder_path}")
                print("Looking for files like: links_*.txt or links.txt")
                return
            
            print(f"\n✓ Found {len(link_files)} link file(s):")
            for i, file in enumerate(link_files, 1):
                filename = os.path.basename(file)
                try:
                    urls = read_urls_from_file(file)
                    print(f"  {i}. {filename} ({len(urls)} URLs)")
                except:
                    print(f"  {i}. {filename} (error reading)")
            
            confirm = input(f"\nProcess all {len(link_files)} files? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                return
            
            print("\n" + "="*60)
            print("INITIALIZING SCRAPER")
            print("="*60)
            
            scraper = WalmartRequestScraper()
            
            # Process each file
            for file_idx, txt_file in enumerate(link_files, 1):
                filename = os.path.basename(txt_file)
                
                print("\n" + "="*60)
                print(f"PROCESSING FILE {file_idx}/{len(link_files)}: {filename}")
                print("="*60)
                
                try:
                    urls = read_urls_from_file(txt_file)
                    
                    if not urls:
                        print(f"✓ {filename} is complete (no remaining URLs)")
                        continue
                    
                    print(f"Found {len(urls)} remaining URLs in {filename}")
                    
                    all_products_data = []
                    all_reviews_combined = []
                    skipped_urls = []
                    
                    for idx, url in enumerate(urls, 1):
                        print("\n" + "-"*60)
                        print(f"FILE {file_idx}/{len(link_files)} | URL {idx}/{len(urls)}")
                        print("-"*60)
                        
                        try:
                            result = scraper.scrape_reviews(url)
                            
                            if result.get('skipped'):
                                print(f"\nProduct skipped")
                                skipped_urls.append({"url": url, "reason": "Page Error", "product_id": result.get('product_id', 'UNKNOWN')})
                                mark_url_as_completed(txt_file, url, f"SKIPPED_{result.get('product_id', 'UNKNOWN')}")
                                continue
                            
                            if result and result.get('reviews'):
                                reviews = result['reviews']
                                
                                unique_reviews = []
                                seen = set()
                                
                                for review in reviews:
                                    key = review.get('review_text', '')
                                    if key and key not in seen and len(key) > 10:
                                        seen.add(key)
                                        review['product_id'] = result['product_id']
                                        review['product_url'] = result['product_url']
                                        review['product_name'] = result.get('product_name', f"Product {result['product_id']}")
                                        unique_reviews.append(review)
                                
                                result['reviews'] = unique_reviews
                                all_products_data.append(result)
                                all_reviews_combined.extend(unique_reviews)
                                
                                # Calculate dominant sentiment
                                positive_count = sum(1 for r in unique_reviews if r.get('sentiment') == 'positive')
                                negative_count = sum(1 for r in unique_reviews if r.get('sentiment') == 'negative')
                                neutral_count = sum(1 for r in unique_reviews if r.get('sentiment') == 'neutral')
                                
                                # Determine dominant sentiment
                                max_count = max(positive_count, negative_count, neutral_count)
                                if positive_count == max_count:
                                    dominant_sentiment = "positive"
                                elif negative_count == max_count:
                                    dominant_sentiment = "negative"
                                else:
                                    dominant_sentiment = "neutral"
                                
                                # Save individual product JSON to appropriate folder
                                sentiment_folder = os.path.join("json_files", dominant_sentiment)
                                os.makedirs(sentiment_folder, exist_ok=True)
                                
                                product_id = result['product_id']
                                product_json_file = os.path.join(sentiment_folder, f"product_{product_id}.json")
                                
                                with open(product_json_file, 'w', encoding='utf-8') as f:
                                    json.dump(result, f, indent=2, ensure_ascii=False)
                                
                                print(f"\n✓ Collected {len(unique_reviews)} reviews")
                                print(f"✓ Dominant sentiment: {dominant_sentiment.upper()}")
                                print(f"✓ Saved to: {product_json_file}")
                                print(f"  Sentiment: +{positive_count} | -{negative_count} | ={neutral_count}")
                                
                                mark_url_as_completed(txt_file, url, result['product_id'])
                                
                            else:
                                print(f"\nNo reviews found")
                                skipped_urls.append({"url": url, "reason": "No Reviews", "product_id": result.get('product_id', 'UNKNOWN') if result else 'UNKNOWN'})
                                result_id = result.get('product_id', 'UNKNOWN') if result else 'UNKNOWN'
                                mark_url_as_completed(txt_file, url, f"NO_REVIEWS_{result_id}")
                                
                        except Exception as e:
                            print(f"\n❌ Error: {e}")
                            skipped_urls.append({"url": url, "reason": f"Error: {str(e)[:50]}", "product_id": "ERROR"})
                            mark_url_as_completed(txt_file, url, "ERROR")
                        
                        if idx < len(urls):
                            delay = random.uniform(3, 6)
                            print(f"\nWaiting {delay:.1f}s before next product...")
                            time.sleep(delay)
                    
                    # Save results for this file
                    if all_reviews_combined:
                        base_name = os.path.splitext(filename)[0]
                        combined_filename = f"walmart_reviews_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        
                        combined_data = {
                            "metadata": {
                                "source_file": txt_file,
                                "total_products": len(all_products_data),
                                "total_reviews": len(all_reviews_combined),
                                "scraped_at": datetime.now().isoformat()
                            },
                            "products": all_products_data
                        }
                        
                        with open(f"{combined_filename}.json", 'w', encoding='utf-8') as f:
                            json.dump(combined_data, f, indent=2, ensure_ascii=False)
                        
                        with open(f"{combined_filename}.csv", 'w', newline='', encoding='utf-8') as f:
                            fieldnames = ['product_id', 'product_name', 'product_url', 'reviewer_name', 'rating', 
                                         'sentiment', 'confidence', 'score', 'roberta_label', 'method', 'title', 
                                         'review_text', 'date', 'verified_purchase', 'helpful_count']
                            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                            writer.writeheader()
                            for review in all_reviews_combined:
                                writer.writerow(review)
                        
                        print(f"\n✓ Saved: {combined_filename}.json and .csv")
                        print(f"  Products: {len(all_products_data)}")
                        print(f"  Reviews: {len(all_reviews_combined)}")
                    
                except Exception as e:
                    print(f"\n❌ Error processing {filename}: {e}")
                    continue
                
                if file_idx < len(link_files):
                    delay = random.uniform(5, 10)
                    print(f"\n{'='*60}")
                    print(f"Waiting {delay:.1f}s before next file...")
                    print(f"{'='*60}")
                    time.sleep(delay)
            
            print("\n" + "="*60)
            print("BATCH PROCESSING COMPLETE!")
            print("="*60)
            print(f"\nProcessed {len(link_files)} file(s)")
            print("All results saved with timestamps.")
            
        elif choice == "2":
            # SINGLE FILE MODE (original)
            txt_file = input("\nEnter path to text file (e.g., links.txt): ").strip()
            if not txt_file:
                txt_file = "links.txt"
            
            urls = read_urls_from_file(txt_file)
            
            if not urls:
                print(f"\n{txt_file} is empty or all URLs processed!")
                return
            
            print(f"\nFound {len(urls)} URLs")
            
            confirm = input("\nProceed with scraping? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                return
            
            scraper = WalmartRequestScraper()
            
            # [Rest of single file processing code - same as before]
            print("Single file mode - use original script for this")
            
        elif choice == "1":
            # SINGLE URL MODE
            product_url = input("\nEnter Walmart product URL: ").strip()
            if not product_url:
                print("No URL provided.")
                return
            
            scraper = WalmartRequestScraper()
            result = scraper.scrape_reviews(product_url)
            
            # Calculate dominant sentiment
            reviews = result.get('reviews', [])
            positive_count = sum(1 for r in reviews if r.get('sentiment') == 'positive')
            negative_count = sum(1 for r in reviews if r.get('sentiment') == 'negative')
            neutral_count = sum(1 for r in reviews if r.get('sentiment') == 'neutral')
            
            max_count = max(positive_count, negative_count, neutral_count)
            if positive_count == max_count:
                dominant_sentiment = "positive"
            elif negative_count == max_count:
                dominant_sentiment = "negative"
            else:
                dominant_sentiment = "neutral"
            
            # Save result in appropriate sentiment folder
            sentiment_folder = os.path.join("json_files", dominant_sentiment)
            os.makedirs(sentiment_folder, exist_ok=True)
            
            product_id = result['product_id']
            filename = os.path.join(sentiment_folder, f"product_{product_id}.json")
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Dominant sentiment: {dominant_sentiment.upper()}")
            print(f"✓ Saved to {filename}")
        
        else:
            print("Invalid choice.")
            return
    
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("INTERRUPTED BY USER")
        print("="*60)
        print("\nProgress saved. Resume by running again.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()