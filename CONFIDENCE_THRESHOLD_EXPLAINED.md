# Confidence Threshold - Simple Explanation

## 📊 Understanding Your Results

### Example Result Message:
**"25 of 31 reviews met your 70% confidence threshold. 6 reviews were excluded."**

---

## What Actually Happened:

### Page 1: ~10 reviews analyzed
- → 8 meet 70% confidence ✓ (8/25 target)
- → 2 below 70% ✗ (filtered out)

### Page 2: ~10 reviews analyzed  
- → 8 meet 70% confidence ✓ (16/25 target)
- → 2 below 70% ✗ (filtered out)

### Page 3: ~10 reviews analyzed
- → 8 meet 70% confidence ✓ (24/25 target)
- → 2 below 70% ✗ (filtered out)

### Page 4: ~1 review analyzed
- → 1 meets 70% confidence ✓ (25/25 target reached!)
- → 0 below 70% ✗

### Total: 31 reviews processed, 25 included, 6 filtered

---

## The Math:

- **31 total reviews** = All reviews the system scraped and analyzed
- **25 included** = Reviews with ≥70% confidence (your target met!)
- **6 filtered out** = Reviews with <70% confidence (19% rejection rate)

---

## Why This is Good:

✅ You wanted 25 reviews

✅ You got exactly 25 **high-quality** reviews

✅ System automatically processed extra reviews to compensate for filtering

✅ 6 low-confidence reviews were excluded to maintain quality

**The system is working perfectly!** It scraped ~4 pages to give you 25 high-confidence reviews instead of just taking the first 25 mixed-quality reviews. 🎯

---

## Step-by-Step Process:

### For Each Review:

1. **Scrape review** from Walmart page
2. **Analyze with ML model** → Get sentiment + confidence score
3. **Check confidence threshold**:
   - If confidence ≥ 70% → **Include it** (add to results)
   - If confidence < 70% → **Skip it** (don't include, move to next)
4. **Repeat** until you have 25 included reviews

---

## Visual Example:

```
Review 1: Confidence 85% → ✓ Include (1/25)
Review 2: Confidence 45% → ✗ Skip
Review 3: Confidence 92% → ✓ Include (2/25)
Review 4: Confidence 68% → ✗ Skip (below 70%)
Review 5: Confidence 78% → ✓ Include (3/25)
Review 6: Confidence 55% → ✗ Skip
...continues until 25 reviews included...
```

---

## The Code Logic:

```python
# For each review scraped:
sentiment_result = self.analyzer.predict_sentiment(review_text, title)
total_processed_reviews += 1  # Count this review

# Check if it meets threshold
if confidence_threshold != 'default':
    threshold_value = float(confidence_threshold) / 100.0  # 70% = 0.70
    confidence_meets_threshold = sentiment_result['confidence'] >= threshold_value

if confidence_meets_threshold:
    all_reviews.append(clean_review)  # ✓ Include it
else:
    filtered_reviews_count += 1  # ✗ Skip it, just count
```

---

## Key Points:

✅ **Every review is analyzed** by the ML model (no skipping analysis)

✅ **Only high-confidence reviews are included** in final results

✅ **Low-confidence reviews are counted but not shown** to you

✅ **System keeps going** until it has 25 qualifying reviews

---

## Quick Reference

| Setting | What It Means |
|---------|---------------|
| **Default** | No filtering - includes all reviews |
| **50% or Higher** | Only reviews where AI is ≥50% confident |
| **70% or Higher** | Only reviews where AI is ≥70% confident (recommended) |
| **80% or Higher** | Only reviews where AI is ≥80% confident |
| **90% or Higher** | Only reviews where AI is ≥90% confident (strictest) |

---

## Common Questions

### Q: Why did it process 31 reviews when I wanted 25?
**A:** Because 6 reviews didn't meet the 70% confidence threshold, so the system kept scraping until it found 25 that did.

### Q: Does it analyze every review?
**A:** Yes! Every review gets analyzed by the ML model. Low-confidence reviews are just not included in the final results.

### Q: What if no reviews meet my threshold?
**A:** You'll get an error suggesting to lower the threshold. This means your threshold is too strict.

### Q: Which threshold should I use?
**A:** 
- **Default**: Maximum coverage
- **70%**: Good balance (recommended)
- **90%**: Maximum quality (may get fewer results)

---

That's it! The confidence threshold ensures you get high-quality sentiment predictions by filtering out reviews where the AI isn't confident enough. 🎯