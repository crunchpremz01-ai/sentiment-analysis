import json
import os
import glob
import csv
from datetime import datetime
from typing import List, Dict, Set
import re

class WalmartReviewMerger:
    def __init__(self):
        """Initialize the merger for combining multiple review JSON files"""
        self.all_reviews = []
        self.all_products = []
        self.seen_review_texts = set()
        self.product_map = {}  # product_id -> product data
        
    def load_json_file(self, filepath: str) -> Dict:
        """Load a single JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"  ⚠ Error loading {filepath}: {e}")
            return None
    
    def extract_reviews_from_json(self, data: Dict, source_file: str) -> tuple[List[Dict], Dict]:
        """
        Extract reviews and product info from various JSON formats.
        Returns: (reviews_list, product_info)
        """
        reviews = []
        product_info = {
            'product_id': None,
            'product_name': None,
            'product_url': None,
            'source_file': os.path.basename(source_file)
        }
        
        # Try to extract product-level metadata
        if isinstance(data, dict):
            if 'product_id' in data:
                product_info['product_id'] = str(data['product_id'])
            if 'product_name' in data:
                product_info['product_name'] = data['product_name']
            if 'product_url' in data:
                product_info['product_url'] = data['product_url']
        
        # Case 1: File with 'products' array (combined format)
        if isinstance(data, dict) and 'products' in data and isinstance(data['products'], list):
            for product in data['products']:
                if 'reviews' in product and isinstance(product['reviews'], list):
                    for review in product['reviews']:
                        # Add product context to each review
                        if 'product_id' not in review and 'product_id' in product:
                            review['product_id'] = product['product_id']
                        if 'product_name' not in review and 'product_name' in product:
                            review['product_name'] = product['product_name']
                        reviews.append(review)
        
        # Case 2: File with 'reviews' array directly
        elif isinstance(data, dict) and 'reviews' in data:
            if isinstance(data['reviews'], list):
                reviews = data['reviews']
            elif isinstance(data['reviews'], dict):
                # Handle sentiment-grouped reviews
                for sentiment_type in ['positive', 'negative', 'neutral']:
                    if sentiment_type in data['reviews']:
                        reviews.extend(data['reviews'][sentiment_type])
                if 'all' in data['reviews']:
                    reviews.extend(data['reviews']['all'])
        
        # Case 3: File is a list of reviews
        elif isinstance(data, list):
            reviews = data
        
        # Post-process reviews to ensure they have source info
        for review in reviews:
            review['source_file'] = os.path.basename(source_file)
            
            # If the review has a product_id inside it, trust it
            if 'product_id' in review and review['product_id']:
                if not product_info['product_id']:
                    product_info['product_id'] = str(review['product_id'])

        # FIX 1: ID Extraction / Fallback logic
        # If we still don't have a product ID, try to find one in the filename
        if not product_info['product_id']:
            # Look for explicit ID pattern _12345678_
            product_id_match = re.search(r'_(\d{8,})_', source_file)
            if product_id_match:
                product_info['product_id'] = product_id_match.group(1)
            else:
                # Fallback: Use the filename itself as a "Group ID" so reviews aren't orphaned
                # Clean up filename to make a readable ID
                clean_name = os.path.splitext(os.path.basename(source_file))[0]
                clean_name = re.sub(r'walmart_reviews_?', '', clean_name)
                clean_name = re.sub(r'_\d{8}_\d{6}$', '', clean_name) # Remove timestamp
                product_info['product_id'] = f"GROUP_{clean_name}"
                if not product_info['product_name']:
                    product_info['product_name'] = clean_name.replace('_', ' ').title()

        return reviews, product_info
    
    def is_duplicate_review(self, review_text: str) -> bool:
        """Check if review text has been seen before"""
        if not review_text or len(str(review_text)) < 10:
            return True
        
        # Normalize text for comparison
        normalized = str(review_text).strip().lower()
        
        if normalized in self.seen_review_texts:
            return True
        
        self.seen_review_texts.add(normalized)
        return False
    
    def merge_files(self, json_files: List[str], filter_sentiment: str = None) -> Dict:
        """Merge multiple JSON files into one combined structure."""
        print(f"\nMerging {len(json_files)} JSON files...")
        if filter_sentiment:
            print(f"Filtering for: {filter_sentiment.upper()} reviews only")
        
        total_reviews_loaded = 0
        total_duplicates_removed = 0
        total_filtered_out = 0
        
        for i, filepath in enumerate(json_files, 1):
            print(f"\n[{i}/{len(json_files)}] Processing: {os.path.basename(filepath)}")
            
            data = self.load_json_file(filepath)
            if not data:
                continue
            
            reviews, product_info = self.extract_reviews_from_json(data, filepath)
            
            if not reviews:
                print(f"  ⚠ No reviews found")
                continue
            
            print(f"  Found {len(reviews)} reviews")
            total_reviews_loaded += len(reviews)
            
            # Track product (Use the fallback ID we generated if needed)
            product_id = product_info.get('product_id', 'UNKNOWN_PRODUCT')
            
            if product_id not in self.product_map:
                self.product_map[product_id] = {
                    'product_id': product_id,
                    'product_name': product_info.get('product_name', f'Product {product_id}'),
                    'product_url': product_info.get('product_url'),
                    'source_files': [],
                    'reviews': []
                }
            
            if product_info['source_file'] not in self.product_map[product_id]['source_files']:
                self.product_map[product_id]['source_files'].append(product_info['source_file'])
            
            # Process reviews
            kept_count = 0
            duplicate_count = 0
            filtered_count = 0
            
            for review in reviews:
                review_text = review.get('review_text', '')
                
                # Check for duplicates
                if self.is_duplicate_review(review_text):
                    duplicate_count += 1
                    continue
                
                # Apply sentiment filter if specified
                if filter_sentiment:
                    review_sentiment = review.get('sentiment', '').lower()
                    if review_sentiment != filter_sentiment.lower():
                        filtered_count += 1
                        continue
                
                # FIX 2: Rating Sanity Check
                # Ensure rating is valid number <= 5
                if 'rating' in review and review['rating'] is not None:
                    try:
                        r_val = float(review['rating'])
                        if r_val > 5.0:
                            # Likely an extraction error (e.g. grabbed review count)
                            review['rating'] = None 
                        else:
                            review['rating'] = r_val
                    except (ValueError, TypeError):
                        review['rating'] = None

                # Keep this review
                self.all_reviews.append(review)
                kept_count += 1
                
                # Add to product's review list
                self.product_map[product_id]['reviews'].append(review)
            
            print(f"  Kept: {kept_count} | Duplicates: {duplicate_count} | Filtered: {filtered_count}")
            total_duplicates_removed += duplicate_count
            total_filtered_out += filtered_count
        
        # Build products array
        self.all_products = list(self.product_map.values())
        
        print(f"\n" + "="*60)
        print("MERGE SUMMARY")
        print("="*60)
        print(f"Total reviews loaded: {total_reviews_loaded}")
        print(f"Duplicates removed: {total_duplicates_removed}")
        if filter_sentiment:
            print(f"Filtered out (non-{filter_sentiment}): {total_filtered_out}")
        print(f"Unique reviews kept: {len(self.all_reviews)}")
        print(f"Products/Groups identified: {len(self.all_products)}")
        
        return self.build_combined_data(filter_sentiment)
    
    def build_combined_data(self, filter_sentiment: str = None) -> Dict:
        """Build the final combined data structure"""
        
        # Calculate statistics
        sentiments = {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}
        ratings = []
        confidences = []
        scores = []
        verified_count = 0
        
        for review in self.all_reviews:
            sentiment = review.get('sentiment', 'unknown')
            if not sentiment: sentiment = 'unknown'
            sentiment = sentiment.lower()
            sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
            
            # Only include valid ratings in average
            if review.get('rating') is not None:
                ratings.append(review['rating'])
            
            if review.get('confidence') is not None:
                try:
                    confidences.append(float(review['confidence']))
                except: pass
            
            if review.get('score') is not None:
                try:
                    scores.append(float(review['score']))
                except: pass
            
            if review.get('verified_purchase'):
                verified_count += 1
        
        avg_rating = sum(ratings) / len(ratings) if ratings else None
        avg_confidence = sum(confidences) / len(confidences) if confidences else None
        avg_score = sum(scores) / len(scores) if scores else None
        
        combined_data = {
            "metadata": {
                "total_files_merged": len(self.product_map),
                "total_products": len(self.all_products),
                "total_reviews": len(self.all_reviews),
                "merged_at": datetime.now().isoformat(),
                "statistics": {
                    "sentiment_distribution": sentiments,
                    "average_rating": round(avg_rating, 2) if avg_rating else None,
                    "average_confidence": round(avg_confidence, 4) if avg_confidence else None,
                    "average_score": round(avg_score, 4) if avg_score else None,
                    "verified_purchases": verified_count,
                    "verified_percentage": round(verified_count / len(self.all_reviews) * 100, 2) if self.all_reviews else 0
                }
            },
            "products": self.all_products
        }
        
        if filter_sentiment:
            combined_data["metadata"]["filter"] = f"{filter_sentiment.upper()}_ONLY"
        
        return combined_data
    
    def save_combined_json(self, combined_data: Dict, output_filename: str = None):
        """Save combined data to JSON file"""
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"walmart_reviews_combined_{timestamp}.json"
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Combined JSON saved to: {output_filename}")
        return output_filename
    
    def save_combined_csv(self, output_filename: str = None):
        """Save combined reviews to CSV file"""
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"walmart_reviews_combined_{timestamp}.csv"
        
        if not self.all_reviews:
            print("⚠ No reviews to save to CSV")
            return
        
        # Get all unique keys from all reviews to ensure no field is missed
        fieldnames = set()
        for review in self.all_reviews:
            fieldnames.update(review.keys())
        
        # Define preferred order
        preferred_order = ['product_id', 'product_name', 'product_url', 'reviewer_name', 
                          'rating', 'sentiment', 'confidence', 'score', 'roberta_label', 
                          'method', 'title', 'review_text', 'date', 'verified_purchase', 
                          'helpful_count', 'source_file']
        
        # Combine preferred with any extras found
        final_fields = [f for f in preferred_order if f in fieldnames]
        final_fields.extend([f for f in fieldnames if f not in preferred_order])
        
        with open(output_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=final_fields, extrasaction='ignore')
            writer.writeheader()
            for review in self.all_reviews:
                writer.writerow(review)
        
        print(f"✓ Combined CSV saved to: {output_filename}")
        return output_filename
    
    def print_detailed_summary(self, combined_data: Dict):
        """Print detailed statistics about the merged data"""
        metadata = combined_data['metadata']
        stats = metadata['statistics']
        
        print("\n" + "="*60)
        print("DETAILED STATISTICS")
        print("="*60)
        
        print(f"\nSentiment Distribution:")
        sentiments = stats['sentiment_distribution']
        total = sum(sentiments.values())
        for sentiment, count in sorted(sentiments.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                percentage = (count / total * 100) if total > 0 else 0
                bar = "█" * int(percentage / 2)
                print(f"  {sentiment.capitalize():10s}: {count:5d} ({percentage:5.1f}%) {bar}")
        
        if stats['average_rating']:
            print(f"\nAverage Rating: {stats['average_rating']:.2f} / 5.00")
        
        if stats['average_confidence']:
            print(f"Average Confidence: {stats['average_confidence']:.2%}")
        
        if stats['average_score']:
            print(f"Average Score: {stats['average_score']:.4f}")
        
        print(f"\nVerified Purchases: {stats['verified_purchases']} ({stats['verified_percentage']}%)")
        
        print(f"\n" + "="*60)
        print("PER-PRODUCT / GROUP BREAKDOWN")
        print("="*60)
        
        for i, product in enumerate(combined_data['products'], 1):
            print(f"\nGroup {i} - ID: {product['product_id']}")
            if product.get('product_name'):
                print(f"  Name: {product['product_name'][:60]}")
            print(f"  Reviews: {len(product['reviews'])}")
            
            # Product-specific stats
            prod_ratings = [r['rating'] for r in product['reviews'] if r.get('rating') is not None]
            if prod_ratings:
                avg = sum(prod_ratings) / len(prod_ratings)
                print(f"  Avg Rating: {avg:.2f}/5.00")
            else:
                print(f"  Avg Rating: N/A")


def find_json_files(directory: str = ".", pattern: str = "*.json") -> List[str]:
    """Find all JSON files in directory matching pattern"""
    search_path = os.path.join(directory, pattern)
    json_files = glob.glob(search_path)
    
    # Sort by modification time (oldest first)
    json_files.sort(key=os.path.getmtime)
    
    return json_files


def main():
    """Main function for merging Walmart review JSON files"""
    
    print("\n" + "="*60)
    print("WALMART REVIEWS JSON MERGER (FIXED)")
    print("="*60)
    print("\nThis script merges multiple review JSON files into one")
    print("✓ Removes duplicate reviews")
    print("✓ Auto-groups orphaned reviews by filename")
    print("✓ Fixes invalid ratings (e.g. 1060.0)")
    print("✓ Generates both JSON and CSV outputs")
    print()
    
    try:
        # Get directory
        directory = input("Enter directory containing JSON files (or press Enter for current): ").strip()
        if not directory:
            directory = "."
        
        if not os.path.exists(directory):
            print(f"Error: Directory '{directory}' does not exist")
            return
        
        # Find JSON files
        print(f"\nSearching for JSON files in: {directory}")
        
        # Ask for pattern
        print("\nFile pattern options:")
        print("1. All JSON files (*.json)")
        print("2. Neutral reviews only (*neutral*.json)")
        print("3. Combined files only (*combined*.json)")
        print("4. Custom pattern")
        
        pattern_choice = input("Enter choice (1-4, default=1): ").strip()
        
        if pattern_choice == "2":
            pattern = "*neutral*.json"
        elif pattern_choice == "3":
            pattern = "*combined*.json"
        elif pattern_choice == "4":
            pattern = input("Enter custom pattern (e.g., walmart_*.json): ").strip()
            if not pattern:
                pattern = "*.json"
        else:
            pattern = "*.json"
        
        json_files = find_json_files(directory, pattern)
        
        if not json_files:
            print(f"\nNo JSON files found matching pattern: {pattern}")
            return
        
        print(f"\nFound {len(json_files)} JSON file(s):")
        for i, filepath in enumerate(json_files, 1):
            size = os.path.getsize(filepath) / 1024  # KB
            print(f"  {i}. {os.path.basename(filepath)} ({size:.1f} KB)")
        
        # Ask for sentiment filter
        print("\nSentiment filter options:")
        print("1. Keep all reviews (no filter)")
        print("2. Keep only POSITIVE reviews")
        print("3. Keep only NEGATIVE reviews")
        print("4. Keep only NEUTRAL reviews")
        
        filter_choice = input("Enter choice (1-4, default=1): ").strip()
        
        filter_sentiment = None
        if filter_choice == "2":
            filter_sentiment = "positive"
        elif filter_choice == "3":
            filter_sentiment = "negative"
        elif filter_choice == "4":
            filter_sentiment = "neutral"
        
        # Confirm
        print("\n" + "="*60)
        print("READY TO MERGE")
        print("="*60)
        print(f"Files to merge: {len(json_files)}")
        print(f"Pattern: {pattern}")
        print(f"Sentiment filter: {filter_sentiment.upper() if filter_sentiment else 'None (keep all)'}")
        
        confirm = input("\nProceed with merge? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Merge cancelled.")
            return
        
        # Perform merge
        merger = WalmartReviewMerger()
        combined_data = merger.merge_files(json_files, filter_sentiment)
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = os.path.basename(directory) if directory != "." else "reviews"
        
        if filter_sentiment:
            output_json = f"walmart_reviews_{filter_sentiment}_{base_name}_combined_{timestamp}.json"
            output_csv = f"walmart_reviews_{filter_sentiment}_{base_name}_combined_{timestamp}.csv"
        else:
            output_json = f"walmart_reviews_{base_name}_combined_{timestamp}.json"
            output_csv = f"walmart_reviews_{base_name}_combined_{timestamp}.csv"
        
        # Save files
        merger.save_combined_json(combined_data, output_json)
        merger.save_combined_csv(output_csv)
        
        # Print detailed summary
        merger.print_detailed_summary(combined_data)
        
        print("\n" + "="*60)
        print("MERGE COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\nOutput files:")
        print(f"  JSON: {output_json}")
        print(f"  CSV:  {output_csv}")
        print(f"\nTotal unique reviews: {len(merger.all_reviews)}")
        print(f"Total products/groups: {len(merger.all_products)}")
        
    except KeyboardInterrupt:
        print("\n\nMerge cancelled by user.")
    except Exception as e:
        print(f"\nError during merge: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()