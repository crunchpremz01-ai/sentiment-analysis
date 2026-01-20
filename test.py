from curl_cffi import requests
import json

url = "https://www.walmart.com/reviews/product/5251143774?page=1"

response = requests.get(url, impersonate="chrome120")

print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content Length: {len(response.text)}")

# Save response
with open('test_response.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# Check for common issues
if 'captcha' in response.text.lower():
    print("❌ CAPTCHA DETECTED")
elif 'robot' in response.text.lower():
    print("❌ BOT DETECTION")
elif '__NEXT_DATA__' in response.text:
    print("✓ Data structure found!")
else:
    print("⚠️ Unusual response - check test_response.html")