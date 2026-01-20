# Authentication System - Testing & Verification Guide

## ✅ Implementation Complete

### Backend Changes
- ✅ Database schema updated with users and password_reset_tokens tables
- ✅ Password hashing with SHA-256 + salt
- ✅ JWT authentication with 7-day expiration
- ✅ Email service configured (Gmail SMTP)
- ✅ All routes protected with @token_required decorator
- ✅ User data isolation by user_id

### Frontend Changes
- ✅ AuthContext created for global auth state
- ✅ LoginPage with email/password
- ✅ RegisterPage with full name, email, password
- ✅ ForgotPasswordPage for password reset requests
- ✅ ResetPasswordPage for setting new password
- ✅ Navbar updated with user menu and logout
- ✅ All API calls updated with authentication headers
- ✅ Responsive design with Lucide icons
- ✅ Complete CSS styling

## 🚀 Setup Instructions

### 1. Install Backend Dependencies
```bash
cd backend
pip install PyJWT==2.8.0 Flask-Mail==0.9.1
```

### 2. Configure Email (Gmail)
You need to set up a Gmail App Password:

1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Go to Security > App Passwords
4. Generate an app password for "Mail"
5. Set environment variable:

**Windows (PowerShell):**
```powershell
$env:MAIL_PASSWORD="your-app-password-here"
```

**Linux/Mac:**
```bash
export MAIL_PASSWORD="your-app-password-here"
```

### 3. Start Backend
```bash
cd backend
python backend.py
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing Checklist

### Test 1: User Registration
1. Open http://localhost:3000
2. Should see Login page
3. Click "Sign up"
4. Fill in:
   - Full Name: Test User
   - Email: test@example.com
   - Password: testpass123
   - Confirm Password: testpass123
5. Click "Create Account"
6. ✅ Should redirect to home page
7. ✅ Should see user name in navbar
8. ✅ Token should be in localStorage

**Expected Result:** User created, logged in, redirected to analyzer

### Test 2: User Login
1. Logout (click user menu > Sign Out)
2. Should see Login page
3. Enter:
   - Email: test@example.com
   - Password: testpass123
4. Click "Sign In"
5. ✅ Should redirect to home page
6. ✅ Should see user name in navbar

**Expected Result:** Successful login

### Test 3: Invalid Login
1. Logout
2. Try login with wrong password
3. ✅ Should show error: "Invalid email or password"

**Expected Result:** Error message displayed

### Test 4: Password Reset Request
1. On login page, click "Forgot password?"
2. Enter email: test@example.com
3. Click "Send Reset Link"
4. ✅ Should show success message
5. ✅ Check email inbox for reset link

**Expected Result:** Email sent with reset link

### Test 5: Password Reset
1. Click link in email (or copy token from backend logs)
2. Should open Reset Password page
3. Enter new password (min 8 characters)
4. Confirm password
5. Click "Reset Password"
6. ✅ Should show success message
7. ✅ Should redirect to login after 3 seconds
8. Login with new password
9. ✅ Should work

**Expected Result:** Password changed successfully

### Test 6: Expired/Invalid Reset Token
1. Try to use an old reset token
2. ✅ Should show "Invalid or expired token"
3. ✅ Should offer to request new link

**Expected Result:** Token validation works

### Test 7: Product Analysis (Authenticated)
1. Login as test user
2. Go to Analyzer
3. Enter Walmart URL
4. Select category
5. Click "Analyze Reviews"
6. ✅ Should work and save to database
7. ✅ Analysis should be linked to user

**Expected Result:** Analysis saved with user_id

### Test 8: Dashboard (User Isolation)
1. Login as test user
2. Go to Dashboard
3. ✅ Should see only your analyses
4. Create second user account
5. Login as second user
6. Go to Dashboard
7. ✅ Should NOT see first user's data
8. ✅ Should see empty dashboard

**Expected Result:** Data isolated by user

### Test 9: Delete Analysis (Authorization)
1. Login as user 1
2. Note an analysis ID from dashboard
3. Logout and login as user 2
4. Try to delete user 1's analysis (via API or browser console)
5. ✅ Should fail with authorization error

**Expected Result:** Users can only delete their own data

### Test 10: Token Expiration
1. Login
2. Wait 7 days (or manually expire token in code for testing)
3. Try to access dashboard
4. ✅ Should redirect to login
5. ✅ Should show "Invalid or expired token"

**Expected Result:** Expired tokens handled correctly

### Test 11: Logout
1. Login
2. Click user menu in navbar
3. Click "Sign Out"
4. ✅ Should redirect to login page
5. ✅ Token should be removed from localStorage
6. ✅ Cannot access protected pages

**Expected Result:** Clean logout

### Test 12: Direct URL Access (Protected Routes)
1. Logout
2. Try to access http://localhost:3000 directly
3. ✅ Should redirect to login
4. Login
5. ✅ Should access home page

**Expected Result:** Protected routes require authentication

### Test 13: Responsive Design
1. Test on mobile viewport (375px)
2. ✅ Login form should be responsive
3. ✅ Register form should be responsive
4. ✅ User menu should adapt
5. ✅ All buttons should be accessible

**Expected Result:** Works on all screen sizes

### Test 14: Form Validation
1. Try to register with:
   - Empty fields ✅ Should show required
   - Short password (< 8 chars) ✅ Should show error
   - Mismatched passwords ✅ Should show error
   - Invalid email format ✅ Should show error
2. Try to login with empty fields ✅ Should show required

**Expected Result:** All validation works

### Test 15: Email Validation
1. Check email content:
   - ✅ Sender: analysiswalmart@gmail.com
   - ✅ Subject: "Password Reset Request - Sentilytics"
   - ✅ Contains reset link
   - ✅ HTML formatted
   - ✅ Expires in 1 hour message

**Expected Result:** Professional email template

## 🐛 Common Issues & Solutions

### Issue 1: Email Not Sending
**Symptom:** Password reset email not received
**Solution:**
- Check MAIL_PASSWORD environment variable is set
- Verify Gmail App Password is correct
- Check spam folder
- Check backend logs for email errors

### Issue 2: Token Invalid
**Symptom:** "Invalid or expired token" on every request
**Solution:**
- Check SECRET_KEY is consistent
- Clear localStorage and login again
- Verify token format in Authorization header

### Issue 3: Database Errors
**Symptom:** "No such column: user_id"
**Solution:**
- Delete scraped_data.db
- Restart backend to recreate tables
- Database schema will auto-update

### Issue 4: CORS Errors
**Symptom:** "CORS policy" errors in browser console
**Solution:**
- Verify Flask-CORS is installed
- Check backend is running on port 5000
- Check frontend is running on port 3000

### Issue 5: User Menu Not Showing
**Symptom:** No user menu in navbar after login
**Solution:**
- Check AuthContext is wrapping App
- Verify user object is populated
- Check browser console for errors

## 📊 Database Verification

### Check Users Table
```sql
SELECT * FROM users;
```
Should show:
- id, email, password_hash, full_name, created_at, last_login

### Check Password Reset Tokens
```sql
SELECT * FROM password_reset_tokens;
```
Should show:
- id, user_id, token, created_at, expires_at, used

### Check Products with User ID
```sql
SELECT id, user_id, category, product_url FROM products;
```
Should show user_id for each product

### Verify Data Isolation
```sql
SELECT user_id, COUNT(*) as product_count 
FROM products 
GROUP BY user_id;
```
Should show separate counts per user

## 🔒 Security Checklist

- ✅ Passwords hashed (never stored plain text)
- ✅ JWT tokens with expiration
- ✅ Authorization checks on all protected routes
- ✅ User data isolated by user_id
- ✅ Password reset tokens expire in 1 hour
- ✅ Reset tokens can only be used once
- ✅ Email validation
- ✅ Password minimum length (8 characters)
- ✅ HTTPS recommended for production
- ✅ Environment variables for sensitive data

## 🎯 Production Checklist

Before deploying to production:

1. ✅ Change SECRET_KEY to strong random value
2. ✅ Set MAIL_PASSWORD via environment variable
3. ✅ Update reset URL to production domain
4. ✅ Enable HTTPS
5. ✅ Set secure cookie flags
6. ✅ Add rate limiting
7. ✅ Add email verification on registration
8. ✅ Add CAPTCHA on login/register
9. ✅ Set up proper logging
10. ✅ Configure backup for database

## 📝 API Endpoints Summary

### Public Endpoints
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/forgot-password
- POST /api/auth/reset-password
- POST /api/auth/verify-reset-token

### Protected Endpoints (require Bearer token)
- GET /api/auth/me
- POST /api/analyze
- GET /api/dashboard
- POST /api/dashboard/clear
- GET /api/dashboard/history
- DELETE /api/dashboard/delete/<id>
- GET /api/dashboard/reviews/<id>
- GET /api/dashboard/export/<id>

## ✨ Features Implemented

1. **User Registration** - Full name, email, password
2. **User Login** - Email and password authentication
3. **Password Reset** - Email-based reset flow
4. **JWT Authentication** - Secure token-based auth
5. **User Sessions** - 7-day token expiration
6. **Data Isolation** - Each user sees only their data
7. **Authorization** - Users can only modify their own data
8. **Responsive Design** - Works on all devices
9. **Error Handling** - Clear error messages
10. **Loading States** - Visual feedback during operations

## 🎉 Success Criteria

All tests passing means:
- ✅ Users can register and login
- ✅ Password reset works via email
- ✅ Data is isolated per user
- ✅ Authorization prevents unauthorized access
- ✅ UI is responsive and user-friendly
- ✅ All security measures in place

## 📞 Support

If you encounter issues:
1. Check backend logs for errors
2. Check browser console for frontend errors
3. Verify environment variables are set
4. Ensure all dependencies are installed
5. Try clearing browser cache and localStorage

---

**System Status:** ✅ READY FOR TESTING

Start with Test 1 (User Registration) and work through all tests sequentially.
