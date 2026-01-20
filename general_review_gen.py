"""
General Synthetic Review Generator using Markov Chains
Processes all JSON files in a folder and generates positive, neutral, and negative reviews
Outputs 3 separate JSON files (one for each sentiment)
"""

import json
import random
import markovify
from datetime import datetime
from typing import List, Dict
import os


class SentimentReviewGenerator:
    def __init__(self, sentiment_type: str):
        """
        Initialize generator for a specific sentiment
        sentiment_type: 'positive', 'neutral', or 'negative'
        """
        self.sentiment_type = sentiment_type
        self.markov_model = None
        self.training_reviews = []
        
    def load_reviews_from_folder(self, folder_path: str):
        """Load all JSON files from folder and filter by sentiment"""
        print(f"\n{'='*60}")
        print(f"Loading {self.sentiment_type.upper()} reviews from folder...")
        print(f"{'='*60}")
        
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        
        if not json_files:
            print(f"No JSON files found in {folder_path}")
            return 0
        
        print(f"Found {len(json_files)} JSON file(s)")
        
        all_reviews = []
        
        for json_file in json_files:
            file_path = os.path.join(folder_path, json_file)
            print(f"  Processing: {json_file}...")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle both single product and combined formats
                reviews = []
                if 'reviews' in data:
                    reviews = data['reviews']
                elif 'products' in data:
                    for product in data['products']:
                        reviews.extend(product.get('reviews', []))
                
                # Filter by sentiment
                sentiment_reviews = [r for r in reviews if r.get('sentiment') == self.sentiment_type]
                all_reviews.extend(sentiment_reviews)
                
                print(f"    Found {len(sentiment_reviews)} {self.sentiment_type} reviews")
                
            except Exception as e:
                print(f"    Error reading {json_file}: {e}")
                continue
        
        self.training_reviews = all_reviews
        print(f"\n✓ Total {self.sentiment_type} reviews loaded: {len(all_reviews)}")
        
        return len(all_reviews)
    
    def train_markov_model(self, state_size: int = 2):
        """Train Markov chain model on review texts"""
        print(f"Training Markov model for {self.sentiment_type} reviews...")
        
        if not self.training_reviews:
            raise ValueError(f"No {self.sentiment_type} training data loaded.")
        
        # Combine all review texts
        review_texts = []
        for review in self.training_reviews:
            text = review.get('review_text', '')
            title = review.get('title', '')
            
            if title and text:
                combined = f"{title}. {text}"
            elif text:
                combined = text
            else:
                continue
            
            review_texts.append(combined)
        
        if not review_texts:
            raise ValueError(f"No valid review texts found in {self.sentiment_type} data")
        
        # Train the model
        training_text = "\n".join(review_texts)
        self.markov_model = markovify.Text(training_text, state_size=state_size)
        print(f"✓ Model trained on {len(review_texts)} {self.sentiment_type} review texts")

    
    def generate_review_text(self, seen_texts: set, seen_titles: set, max_attempts: int = 200) -> tuple:
        """Generate unique synthetic review text and title"""
        if not self.markov_model:
            raise ValueError("Model not trained. Call train_markov_model() first.")
        
        # Generate review text
        review_text = None
        for attempt in range(max_attempts):
            max_words = random.randint(15, 80)
            sentence = self.markov_model.make_sentence(tries=100, max_words=max_words)
            
            if sentence and len(sentence.split()) >= 10:
                if sentence not in seen_texts:
                    # Check for substantial similarity
                    is_unique = True
                    sentence_words = set(sentence.lower().split())
                    for existing in seen_texts:
                        existing_words = set(existing.lower().split())
                        if len(sentence_words & existing_words) / len(sentence_words | existing_words) > 0.7:
                            is_unique = False
                            break
                    
                    if is_unique:
                        review_text = sentence
                        break
        
        if not review_text:
            review_text = self.markov_model.make_sentence(tries=100)
        
        # Generate title
        title = None
        for attempt in range(max_attempts):
            max_chars = random.randint(40, 100)
            sentence = self.markov_model.make_short_sentence(max_chars=max_chars, tries=100)
            
            if sentence and 3 <= len(sentence.split()) <= 15:
                if sentence not in seen_titles:
                    title = sentence
                    break
        
        if not title:
            title = self.markov_model.make_short_sentence(max_chars=100, tries=100) or ""
        
        return title, review_text
    
    def sample_metadata(self) -> Dict:
        """Sample realistic metadata from training data"""
        if not self.training_reviews:
            return {}
        
        sample = random.choice(self.training_reviews)
        
        return {
            'rating': sample.get('rating'),
            'verified_purchase': sample.get('verified_purchase', False),
            'helpful_count': random.choice([0, 0, 0, 1, 2]) if random.random() > 0.7 else 0,
            'date': sample.get('date', ''),
        }
    
    def generate_reviewer_name(self) -> str:
        """Generate realistic reviewer names"""
        first_names = ['John', 'Sarah', 'Mike', 'Emily', 'David', 'Jessica', 'Chris', 
                      'Amanda', 'Ryan', 'Jennifer', 'Matt', 'Lisa', 'Tom', 'Karen',
                      'Alex', 'Nicole', 'Brian', 'Rachel', 'Kevin', 'Lauren']
        
        if random.random() > 0.3:
            last_initial = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            return f"{random.choice(first_names)} {last_initial}."
        else:
            return random.choice(first_names)
    
    def get_confidence_score_range(self) -> tuple:
        """Get appropriate confidence and score ranges for sentiment type"""
        if self.sentiment_type == 'positive':
            confidence = (0.70, 0.95)
            score = (0.65, 0.90)
        elif self.sentiment_type == 'negative':
            confidence = (0.65, 0.95)
            score = (0.10, 0.35)
        else:  # neutral
            confidence = (0.60, 0.90)
            score = (0.40, 0.60)
        
        return confidence, score

    
    def generate_synthetic_review(self, seen_texts: set, seen_titles: set, 
                                  product_id: str = None, product_name: str = None, 
                                  product_url: str = None) -> Dict:
        """Generate a single synthetic review"""
        title, review_text = self.generate_review_text(seen_texts, seen_titles)
        
        if not review_text:
            return None
        
        metadata = self.sample_metadata()
        confidence_range, score_range = self.get_confidence_score_range()
        
        confidence = round(random.uniform(*confidence_range), 4)
        score = round(random.uniform(*score_range), 4)
        
        synthetic_review = {
            'reviewer_name': self.generate_reviewer_name(),
            'rating': metadata.get('rating', None),
            'title': title or '',
            'review_text': review_text,
            'date': metadata.get('date', ''),
            'verified_purchase': metadata.get('verified_purchase', False),
            'helpful_count': metadata.get('helpful_count', 0),
            'sentiment': self.sentiment_type,
            'confidence': confidence,
            'score': score,
            'roberta_label': self.sentiment_type,
            'method': 'synthetic_markov'
        }
        
        if product_id:
            synthetic_review['product_id'] = product_id
        if product_name:
            synthetic_review['product_name'] = product_name
        if product_url:
            synthetic_review['product_url'] = product_url
        
        return synthetic_review
    
    def generate_dataset(self, num_reviews: int, num_products: int = 1, 
                        base_product_id: str = None) -> Dict:
        """Generate a complete synthetic dataset"""
        print(f"\n{'='*60}")
        print(f"Generating {num_reviews} {self.sentiment_type.upper()} reviews...")
        print(f"{'='*60}")
        
        reviews_per_product = num_reviews // num_products
        remainder = num_reviews % num_products
        
        products = []
        seen_texts = set()
        seen_titles = set()
        total_generated = 0
        
        for product_idx in range(num_products):
            product_id = f"{base_product_id or 'SYNTHETIC'}_{self.sentiment_type.upper()}_{product_idx + 1:03d}"
            product_name = f"Synthetic {self.sentiment_type.title()} Product {product_idx + 1}"
            product_url = f"https://walmart.com/synthetic/{product_id}"
            
            target_reviews = reviews_per_product + (1 if product_idx < remainder else 0)
            
            product_reviews = []
            attempts = 0
            max_attempts = target_reviews * 10
            failed_attempts = 0
            max_failed = 100
            
            print(f"Product {product_idx + 1}/{num_products}: Generating {target_reviews} reviews...")
            
            while len(product_reviews) < target_reviews and attempts < max_attempts:
                attempts += 1
                
                review = self.generate_synthetic_review(
                    seen_texts, seen_titles, 
                    product_id, product_name, product_url
                )
                
                if review and review['review_text']:
                    review_text = review['review_text']
                    review_title = review['title']
                    
                    if review_text not in seen_texts:
                        is_unique = True
                        review_words = set(review_text.lower().split())
                        
                        for existing_text in seen_texts:
                            existing_words = set(existing_text.lower().split())
                            intersection = len(review_words & existing_words)
                            union = len(review_words | existing_words)
                            
                            if union > 0:
                                similarity = intersection / union
                                if similarity > 0.6:
                                    is_unique = False
                                    break
                        
                        if is_unique:
                            seen_texts.add(review_text)
                            if review_title:
                                seen_titles.add(review_title)
                            
                            product_reviews.append(review)
                            total_generated += 1
                            failed_attempts = 0
                            
                            if len(product_reviews) % 50 == 0:
                                print(f"  Generated {len(product_reviews)}/{target_reviews}...")
                        else:
                            failed_attempts += 1
                    else:
                        failed_attempts += 1
                else:
                    failed_attempts += 1
                
                if failed_attempts >= max_failed:
                    print(f"  ⚠ Generated {len(product_reviews)}/{target_reviews} reviews for this product")
                    break
            
            if product_reviews:
                products.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'product_url': product_url,
                    'reviews': product_reviews
                })
        
        print(f"✓ Generated {total_generated} unique {self.sentiment_type} reviews")
        
        # Calculate averages
        all_reviews = []
        for product in products:
            all_reviews.extend(product['reviews'])
        
        confidences = [r['confidence'] for r in all_reviews]
        scores = [r['score'] for r in all_reviews]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        avg_score = sum(scores) / len(scores) if scores else 0
        
        dataset = {
            "metadata": {
                "filter": f"{self.sentiment_type.upper()}_ONLY",
                "total_products": len(products),
                f"total_{self.sentiment_type}_reviews": total_generated,
                "average_confidence": round(avg_confidence, 4),
                "average_score": round(avg_score, 4),
                "generation_method": "markov_chain_synthetic",
                "uniqueness": "100% (strict similarity checking)",
                "sentiment_analyzer": f"synthetic_{self.sentiment_type}",
                "device": "N/A",
                "generated_at": datetime.now().isoformat()
            },
            "products": products
        }
        
        return dataset



def main():
    print("\n" + "="*70)
    print("GENERAL SYNTHETIC REVIEW GENERATOR")
    print("="*70)
    print("Generates Positive, Neutral, and Negative reviews from folder")
    print("Outputs 3 separate JSON files (one for each sentiment)")
    print("="*70)
    
    # Get folder path
    folder_path = input("\nEnter folder path containing JSON files: ").strip()
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found!")
        return
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a directory!")
        return
    
    # Get number of reviews for each sentiment
    print("\n" + "="*70)
    print("How many reviews to generate for each sentiment?")
    print("="*70)
    
    try:
        num_positive = int(input("Positive reviews (default: 50): ").strip() or "50")
        num_neutral = int(input("Neutral reviews (default: 50): ").strip() or "50")
        num_negative = int(input("Negative reviews (default: 50): ").strip() or "50")
    except ValueError:
        print("Invalid input! Using defaults (50 each)")
        num_positive = num_neutral = num_negative = 50
    
    # Get number of products
    try:
        num_products = int(input("\nHow many products to distribute reviews across? (default: 1): ").strip() or "1")
    except ValueError:
        num_products = 1
    
    print(f"\n{'='*70}")
    print("CONFIGURATION")
    print(f"{'='*70}")
    print(f"Folder: {folder_path}")
    print(f"Positive reviews: {num_positive}")
    print(f"Neutral reviews: {num_neutral}")
    print(f"Negative reviews: {num_negative}")
    print(f"Products per sentiment: {num_products}")
    print(f"{'='*70}")
    
    confirm = input("\nProceed with generation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Generation cancelled.")
        return
    
    # Process each sentiment
    sentiments = ['positive', 'neutral', 'negative']
    review_counts = [num_positive, num_neutral, num_negative]
    generated_files = []
    
    for sentiment, num_reviews in zip(sentiments, review_counts):
        if num_reviews <= 0:
            print(f"\nSkipping {sentiment} (0 reviews requested)")
            continue
        
        try:
            print(f"\n{'='*70}")
            print(f"PROCESSING {sentiment.upper()} REVIEWS")
            print(f"{'='*70}")
            
            # Initialize generator
            generator = SentimentReviewGenerator(sentiment)
            
            # Load reviews from folder
            total_loaded = generator.load_reviews_from_folder(folder_path)
            
            if total_loaded == 0:
                print(f"⚠ No {sentiment} reviews found in folder. Skipping...")
                continue
            
            # Train model
            generator.train_markov_model(state_size=2)
            
            # Generate synthetic reviews
            synthetic_dataset = generator.generate_dataset(
                num_reviews=num_reviews,
                num_products=num_products,
                base_product_id="SYNTHETIC"
            )
            
            # Save to file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"_combined_walmart_reviews_synthetic_{sentiment}_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(synthetic_dataset, f, indent=2, ensure_ascii=False)
            
            generated_files.append({
                'sentiment': sentiment,
                'file': output_file,
                'count': synthetic_dataset['metadata'][f'total_{sentiment}_reviews'],
                'products': synthetic_dataset['metadata']['total_products']
            })
            
            print(f"\n✓ {sentiment.upper()} reviews saved to: {output_file}")
            
        except Exception as e:
            print(f"\n❌ Error generating {sentiment} reviews: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Final summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE!")
    print("="*70)
    
    if generated_files:
        print(f"\nGenerated {len(generated_files)} file(s):\n")
        for file_info in generated_files:
            print(f"  {file_info['sentiment'].upper()}:")
            print(f"    File: {file_info['file']}")
            print(f"    Reviews: {file_info['count']}")
            print(f"    Products: {file_info['products']}")
            print()
        
        # Show sample from first file
        if generated_files:
            first_file = generated_files[0]
            print(f"{'='*70}")
            print(f"SAMPLE REVIEWS ({first_file['sentiment'].upper()})")
            print(f"{'='*70}")
            
            try:
                with open(first_file['file'], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data['products']:
                    first_product = data['products'][0]
                    print(f"\nProduct: {first_product['product_name']}")
                    
                    for i, review in enumerate(first_product['reviews'][:3], 1):
                        print(f"\nReview {i}:")
                        print(f"  Reviewer: {review['reviewer_name']}")
                        print(f"  Title: {review['title']}")
                        print(f"  Text: {review['review_text'][:100]}...")
                        print(f"  Confidence: {review['confidence']:.2%}")
            except Exception as e:
                print(f"Could not display samples: {e}")
        
        print(f"\n{'='*70}")
        print("✓ All files saved successfully!")
        print("✓ Structure matches scraper output format")
        print(f"{'='*70}\n")
    else:
        print("\n⚠ No files were generated. Check for errors above.")


if __name__ == "__main__":
    main()
