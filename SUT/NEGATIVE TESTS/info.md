)

👉 Purpose: Ensure system fails safely and predictably.

🔐 Authentication Negative Cases
Invalid username + valid password
Valid username + invalid password
Both fields empty
Only username provided
Only password provided
🚫 Security-Oriented Tests
SQL injection strings in username field
Script injection attempts (<script>alert()</script>)
Excessively long credentials (buffer stress)
⚠️ System Response Validation
Proper error message displayed
No crash or UI freeze
No sensitive data leakage