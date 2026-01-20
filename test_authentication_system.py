"""
Complete Authentication System Test Script
Tests: Registration, Login, Analysis, User Session Isolation
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3001"

# Test product URL
TEST_PRODUCT_URL = "https://www.walmart.com/ip/Kitchen-in-the-box-15-in-1-Bread-Machine-2LB-Stainless-Steel-Automatic-Bread-Maker-with-Recipes-Silver/5528298909"

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def print_step(text):
    print(f"\n{Colors.BOLD}→ {text}{Colors.RESET}")

# Test Data
user1_data = {
    "fullName": "Test User One",
    "email": f"testuser1_{int(time.time())}@example.com",
    "password": "testpass123"
}

user2_data = {
    "fullName": "Test User Two",
    "email": f"testuser2_{int(time.time())}@example.com",
    "password": "testpass456"
}

def test_user_registration(user_data):
    """Test user registration"""
    print_step(f"Testing registration for {user_data['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('token'):
                print_success(f"Registration successful")
                print_info(f"User ID: {data['user']['id']}")
                print_info(f"Email: {data['user']['email']}")
                print_info(f"Token: {data['token'][:20]}...")
                return data['token'], data['user']
            else:
                print_error(f"Registration failed: {data}")
                return None, None
        else:
            print_error(f"Registration failed: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print_error(f"Registration error: {e}")
        return None, None

def test_user_login(email, password):
    """Test user login"""
    print_step(f"Testing login for {email}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('token'):
                print_success(f"Login successful")
                print_info(f"Token: {data['token'][:20]}...")
                return data['token'], data['user']
            else:
                print_error(f"Login failed: {data}")
                return None, None
        else:
            print_error(f"Login failed: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None, None

def test_get_current_user(token):
    """Test getting current user info"""
    print_step("Testing get current user")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Got current user info")
            print_info(f"User: {data['user']['fullName']} ({data['user']['email']})")
            return data['user']
        else:
            print_error(f"Failed to get user: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error getting user: {e}")
        return None

def test_product_analysis(token, user_email):
    """Test product analysis"""
    print_step(f"Testing product analysis for {user_email}")
    print_info(f"Product URL: {TEST_PRODUCT_URL}")
    
    try:
        # Start analysis
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={
                "url": TEST_PRODUCT_URL,
                "max_reviews": 25,
                "confidence_threshold": "default",
                "category": "kitchen"
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code != 200:
            print_error(f"Analysis failed: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        session_id = data.get('session_id')
        print_success(f"Analysis started (Session: {session_id})")
        
        # Poll for results
        print_info("Polling for results...")
        max_attempts = 60
        attempt = 0
        
        while attempt < max_attempts:
            time.sleep(2)
            attempt += 1
            
            status_response = requests.get(f"{BASE_URL}/api/status/{session_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                
                if status_data.get('status') == 'complete':
                    print_success("Analysis completed!")
                    result = status_data.get('data', {})
                    metadata = result.get('metadata', {})
                    print_info(f"Total reviews: {metadata.get('total_reviews', 0)}")
                    print_info(f"Positive: {metadata.get('positive_count', 0)}")
                    print_info(f"Negative: {metadata.get('negative_count', 0)}")
                    print_info(f"Neutral: {metadata.get('neutral_count', 0)}")
                    return result
                elif status_data.get('status') == 'error':
                    print_error(f"Analysis error: {status_data.get('message')}")
                    return None
                else:
                    progress = status_data.get('progress', 0)
                    message = status_data.get('message', 'Processing...')
                    print(f"\r  Progress: {progress}% - {message}", end='', flush=True)
        
        print_error("\nAnalysis timeout")
        return None
        
    except Exception as e:
        print_error(f"Analysis error: {e}")
        return None

def test_dashboard_data(token, user_email):
    """Test dashboard data retrieval"""
    print_step(f"Testing dashboard data for {user_email}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            overall = data.get('overall', {})
            categories = data.get('categories', [])
            
            print_success("Dashboard data retrieved")
            print_info(f"Total products: {overall.get('total_products', 0)}")
            print_info(f"Total reviews: {overall.get('total_reviews', 0)}")
            print_info(f"Categories: {len(categories)}")
            
            for cat in categories:
                print_info(f"  - {cat['category']}: {cat['total_reviews']} reviews")
            
            return data
        else:
            print_error(f"Failed to get dashboard: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Dashboard error: {e}")
        return None

def test_analysis_history(token, user_email):
    """Test analysis history retrieval"""
    print_step(f"Testing analysis history for {user_email}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/dashboard/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            history = data.get('history', [])
            
            print_success(f"History retrieved: {len(history)} analyses")
            
            for item in history:
                print_info(f"  - ID: {item['id']}, Category: {item['category']}, Reviews: {item['total_reviews']}")
            
            return history
        else:
            print_error(f"Failed to get history: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"History error: {e}")
        return None

def test_user_isolation(token1, user1_email, token2, user2_email):
    """Test that users can only see their own data"""
    print_step("Testing user data isolation")
    
    # Get user 1's data
    print_info(f"Getting data for {user1_email}")
    history1 = test_analysis_history(token1, user1_email)
    
    # Get user 2's data
    print_info(f"Getting data for {user2_email}")
    history2 = test_analysis_history(token2, user2_email)
    
    if history1 is not None and history2 is not None:
        # Check that histories are different
        ids1 = set(item['id'] for item in history1)
        ids2 = set(item['id'] for item in history2)
        
        overlap = ids1.intersection(ids2)
        
        if len(overlap) == 0:
            print_success("✓ User data isolation verified - no overlap between users")
            return True
        else:
            print_error(f"✗ Data isolation FAILED - {len(overlap)} shared analyses found!")
            return False
    else:
        print_error("Could not verify isolation - failed to get history")
        return False

def test_unauthorized_access(token1, user2_analysis_id):
    """Test that user 1 cannot access user 2's analysis"""
    print_step("Testing unauthorized access prevention")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/dashboard/reviews/{user2_analysis_id}",
            headers={"Authorization": f"Bearer {token1}"}
        )
        
        if response.status_code == 404:
            print_success("✓ Unauthorized access blocked correctly")
            return True
        else:
            print_error(f"✗ Security issue: Got status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing unauthorized access: {e}")
        return False

def run_complete_test():
    """Run complete authentication and session test"""
    print_header("AUTHENTICATION SYSTEM COMPLETE TEST")
    print_info(f"Backend: {BASE_URL}")
    print_info(f"Frontend: {FRONTEND_URL}")
    print_info(f"Test Product: Kitchen Bread Machine")
    print_info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    # Test 1: Register User 1
    print_header("TEST 1: Register User 1")
    token1, user1 = test_user_registration(user1_data)
    results["total"] += 1
    if token1:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("Cannot continue without user 1")
        return results
    
    # Test 2: Register User 2
    print_header("TEST 2: Register User 2")
    token2, user2 = test_user_registration(user2_data)
    results["total"] += 1
    if token2:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("Cannot continue without user 2")
        return results
    
    # Test 3: Login User 1
    print_header("TEST 3: Login User 1")
    login_token1, _ = test_user_login(user1_data['email'], user1_data['password'])
    results["total"] += 1
    if login_token1:
        results["passed"] += 1
        token1 = login_token1  # Use login token
    else:
        results["failed"] += 1
    
    # Test 4: Get Current User
    print_header("TEST 4: Get Current User Info")
    current_user = test_get_current_user(token1)
    results["total"] += 1
    if current_user:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Analyze Product (User 1)
    print_header("TEST 5: Analyze Product (User 1)")
    analysis1 = test_product_analysis(token1, user1_data['email'])
    results["total"] += 1
    if analysis1:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Get Dashboard Data (User 1)
    print_header("TEST 6: Get Dashboard Data (User 1)")
    dashboard1 = test_dashboard_data(token1, user1_data['email'])
    results["total"] += 1
    if dashboard1:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 7: Get Analysis History (User 1)
    print_header("TEST 7: Get Analysis History (User 1)")
    history1 = test_analysis_history(token1, user1_data['email'])
    results["total"] += 1
    if history1:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 8: Analyze Product (User 2)
    print_header("TEST 8: Analyze Product (User 2)")
    analysis2 = test_product_analysis(token2, user2_data['email'])
    results["total"] += 1
    if analysis2:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 9: Get Dashboard Data (User 2)
    print_header("TEST 9: Get Dashboard Data (User 2)")
    dashboard2 = test_dashboard_data(token2, user2_data['email'])
    results["total"] += 1
    if dashboard2:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 10: Verify User Data Isolation
    print_header("TEST 10: Verify User Data Isolation")
    isolation_ok = test_user_isolation(token1, user1_data['email'], token2, user2_data['email'])
    results["total"] += 1
    if isolation_ok:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 11: Test Unauthorized Access
    print_header("TEST 11: Test Unauthorized Access Prevention")
    if history1 and len(history1) > 0:
        user2_analysis_id = history1[0]['id']  # Try to access user 1's analysis with user 2's token
        unauthorized_blocked = test_unauthorized_access(token2, user2_analysis_id)
        results["total"] += 1
        if unauthorized_blocked:
            results["passed"] += 1
        else:
            results["failed"] += 1
    else:
        print_info("Skipping unauthorized access test - no analyses found")
    
    # Final Results
    print_header("TEST RESULTS SUMMARY")
    print(f"\n{Colors.BOLD}Total Tests: {results['total']}{Colors.RESET}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.RESET}")
    
    success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.RESET}")
    
    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Authentication system working correctly{Colors.RESET}")
        print(f"{Colors.GREEN}✓ User session isolation verified{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Authorization checks working{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠ SOME TESTS FAILED{Colors.RESET}")
        print(f"{Colors.YELLOW}Please review the errors above{Colors.RESET}")
    
    print(f"\n{Colors.BLUE}Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")
    
    return results

if __name__ == "__main__":
    try:
        results = run_complete_test()
        exit(0 if results['failed'] == 0 else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Test interrupted by user{Colors.RESET}")
        exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        exit(1)
