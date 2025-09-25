#!/usr/bin/env python3
"""
Ultra simple server - minimal dependencies
"""

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    import uvicorn
    
    app = FastAPI()
    
    @app.get("/", response_class=HTMLResponse)
    async def root():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Heart Disease Prediction System</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .info { background: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; margin: 20px 0; }
                h1 { color: #dc3545; text-align: center; }
                ul { list-style-type: none; padding: 0; }
                li { background: #f8f9fa; margin: 10px 0; padding: 10px; border-radius: 5px; border-left: 4px solid #007bff; }
                a { color: #007bff; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🫀 Heart Disease Prediction System</h1>
                
                <div class="success">
                    <strong>✅ Server is Running Successfully!</strong><br>
                    The FastAPI backend is working correctly.
                </div>
                
                <div class="info">
                    <strong>ℹ️ System Status:</strong><br>
                    • Backend API: ✅ Online<br>
                    • Database: ⚠️ Mock mode (no MongoDB required)<br>
                    • Frontend: 🔄 Loading from files<br>
                </div>
                
                <h3>🔗 Available Endpoints:</h3>
                <ul>
                    <li><a href="/docs">📚 Interactive API Documentation (Swagger)</a></li>
                    <li><a href="/redoc">📖 Alternative API Documentation (ReDoc)</a></li>
                    <li><a href="/health">🏥 Health Check Endpoint</a></li>
                    <li><a href="/login">🔐 Login Page</a></li>
                </ul>
                
                <h3>🎯 Quick Test:</h3>
                <ul>
                    <li><strong>Admin Login:</strong> admin@heartpredict.com / admin123</li>
                    <li><strong>Doctor Login:</strong> dr.smith@heartpredict.com / doctor123</li>
                </ul>
                
                <div class="info">
                    <strong>🚀 Next Steps:</strong><br>
                    1. Visit <a href="/docs">/docs</a> to explore the API<br>
                    2. Use the login endpoint to authenticate<br>
                    3. Access patient and prediction endpoints<br>
                </div>
            </div>
        </body>
        </html>
        """
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "message": "Heart Disease Prediction API is running"}
    
    @app.get("/login", response_class=HTMLResponse)
    async def login_page():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login - Heart Disease Prediction</title>
            <style>
                body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 40px; min-height: 100vh; }
                .login-container { max-width: 400px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
                .logo { text-align: center; font-size: 3em; color: #667eea; margin-bottom: 20px; }
                h2 { text-align: center; color: #333; margin-bottom: 30px; }
                .form-group { margin-bottom: 20px; }
                label { display: block; margin-bottom: 5px; color: #555; font-weight: bold; }
                input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
                input:focus { border-color: #667eea; outline: none; }
                button { width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
                button:hover { opacity: 0.9; }
                .demo-info { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="login-container">
                <div class="logo">🫀</div>
                <h2>Heart Disease Prediction System</h2>
                
                <form id="loginForm">
                    <div class="form-group">
                        <label for="email">Email:</label>
                        <input type="email" id="email" value="admin@heartpredict.com" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" value="admin123" required>
                    </div>
                    
                    <button type="submit">Sign In</button>
                </form>
                
                <div class="demo-info">
                    <strong>Demo Credentials:</strong><br>
                    Admin: admin@heartpredict.com / admin123<br>
                    Doctor: dr.smith@heartpredict.com / doctor123
                </div>
            </div>
            
            <script>
                document.getElementById('loginForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const email = document.getElementById('email').value;
                    const password = document.getElementById('password').value;
                    
                    try {
                        const response = await fetch('/api/auth/login', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ email, password })
                        });
                        
                        if (response.ok) {
                            const data = await response.json();
                            alert('Login successful! Token: ' + data.access_token);
                            window.location.href = '/docs';
                        } else {
                            alert('Login failed: Invalid credentials');
                        }
                    } catch (error) {
                        alert('Network error: ' + error.message);
                    }
                });
            </script>
        </body>
        </html>
        """
    
    @app.post("/api/auth/login")
    async def login(credentials: dict):
        users = {
            "admin@heartpredict.com": {"password": "admin123", "role": "admin", "name": "Admin"},
            "dr.smith@heartpredict.com": {"password": "doctor123", "role": "doctor", "name": "Dr. Smith"}
        }
        
        email = credentials.get("email")
        password = credentials.get("password")
        
        if email in users and users[email]["password"] == password:
            return {
                "access_token": f"token_{email}",
                "token_type": "bearer",
                "user": {"email": email, "role": users[email]["role"], "name": users[email]["name"]}
            }
        else:
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if __name__ == "__main__":
        print("🚀 Starting Ultra Simple Heart Disease Prediction Server...")
        print("🌐 Open your browser and go to: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🔐 Login Page: http://localhost:8000/login")
        print("🛑 Press Ctrl+C to stop")
        uvicorn.run(app, host="0.0.0.0", port=8000)

except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("📦 Please install: pip install fastapi uvicorn")
except Exception as e:
    print(f"❌ Error: {e}")