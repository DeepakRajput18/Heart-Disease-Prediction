#!/usr/bin/env python3
"""
Standalone server using only Python standard library
No external dependencies required
"""

import http.server
import socketserver
import json
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import threading

PORT = 8000

class HeartDiseaseHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for Heart Disease Prediction System"""

    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # API endpoints
        if path == '/api/health':
            self.send_json_response({
                "status": "healthy",
                "message": "Heart Disease Prediction API is running",
                "version": "1.0.0"
            })
            return

        elif path == '/api/status':
            self.send_json_response({
                "backend": "online",
                "database": "supabase",
                "frontend": "served"
            })
            return

        # Serve frontend files
        elif path == '/' or path == '':
            self.serve_file('frontend/index.html', 'text/html')
            return

        elif path == '/index.html':
            self.serve_file('frontend/index.html', 'text/html')
            return

        elif path.startswith('/css/'):
            file_path = f'frontend{path}'
            self.serve_file(file_path, 'text/css')
            return

        elif path.startswith('/js/'):
            file_path = f'frontend{path}'
            self.serve_file(file_path, 'application/javascript')
            return

        # Default fallback
        else:
            super().do_GET()

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON")
            return

        # Mock login endpoint
        if path == '/api/auth/login':
            email = data.get('email', '')
            password = data.get('password', '')

            # Mock users
            users = {
                "admin@heartpredict.com": {
                    "password": "admin123",
                    "role": "admin",
                    "name": "System Administrator"
                },
                "dr.smith@heartpredict.com": {
                    "password": "doctor123",
                    "role": "doctor",
                    "name": "Dr. John Smith"
                }
            }

            if email in users and users[email]['password'] == password:
                self.send_json_response({
                    "access_token": f"mock_token_{email}",
                    "token_type": "bearer",
                    "user": {
                        "email": email,
                        "role": users[email]['role'],
                        "name": users[email]['name']
                    }
                })
            else:
                self.send_error_response(401, "Invalid credentials")
            return

        # Mock prediction endpoint
        elif path == '/api/predictions/predict':
            # Return mock prediction
            self.send_json_response({
                "prediction": "low_risk",
                "probability": 0.23,
                "risk_level": "Low Risk",
                "recommendations": [
                    "Maintain healthy lifestyle",
                    "Regular checkups recommended",
                    "Continue current exercise routine"
                ]
            })
            return

        else:
            self.send_error_response(404, "Endpoint not found")

    def serve_file(self, file_path, content_type):
        """Serve a file with proper content type"""
        try:
            full_path = Path(__file__).parent / file_path
            if full_path.exists() and full_path.is_file():
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                with open(full_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, f"File not found: {file_path}")
        except Exception as e:
            self.send_error(500, f"Error serving file: {e}")

    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))

    def send_error_response(self, status, message):
        """Send error response"""
        self.send_json_response({
            "error": message,
            "status": status
        }, status=status)

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    """Start the server"""
    print("=" * 60)
    print("🫀 Heart Disease Prediction System - Standalone Server")
    print("=" * 60)
    print(f"✅ Python version: {os.sys.version.split()[0]}")
    print(f"📁 Serving from: {Path(__file__).parent}")
    print(f"🌐 Server starting on port {PORT}...")
    print()

    # Check if frontend exists
    frontend_path = Path(__file__).parent / "frontend" / "index.html"
    if frontend_path.exists():
        print(f"✅ Frontend found: {frontend_path}")
    else:
        print(f"⚠️  Frontend not found at: {frontend_path}")
        print("   Server will still run but some pages may not work")

    print()
    print("🚀 Server is running!")
    print("-" * 60)
    print(f"🌐 Open your browser: http://localhost:{PORT}")
    print(f"🏥 Health check:      http://localhost:{PORT}/api/health")
    print(f"📊 Status:            http://localhost:{PORT}/api/status")
    print()
    print("🔐 Demo Credentials:")
    print("   Admin:  admin@heartpredict.com / admin123")
    print("   Doctor: dr.smith@heartpredict.com / doctor123")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 60)

    try:
        with socketserver.TCPServer(("", PORT), HeartDiseaseHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n")
        print("🛑 Server stopped by user")
        print("✅ Shutdown complete")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Error: Port {PORT} is already in use")
            print(f"💡 Try stopping other servers or use a different port")
            print(f"   You can modify the PORT variable in this script")
        else:
            print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
