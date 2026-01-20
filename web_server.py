#!/usr/bin/env python3
"""
Simple HTTP server for the web frontend
Runs on port 3000 by default, connects to backend API on port 8000
"""
import http.server
import socketserver
import os
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).parent
WEB_DIR = BASE_DIR / "web"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Normalize path
        path = self.path.split('?')[0]  # Remove query string
        
        # Serve index.html for root path
        if path == '/' or path == '':
            self.path = '/templates/index.html'
        # Static files are already correctly referenced in HTML
        # The SimpleHTTPRequestHandler will serve them from WEB_DIR/static/
        elif path.startswith('/static/'):
            # Path is already correct, just serve it
            pass
        elif path.startswith('/templates/'):
            # Templates should be accessible
            pass
        else:
            # For any other path, try to serve it
            pass
        
        super().do_GET()
    
    def log_message(self, format, *args):
        # Custom logging - show requests
        if not self.path.startswith('/static/'):
            print(f"📄 {self.path}")

if __name__ == "__main__":
    PORT = int(os.getenv("WEB_PORT", 3000))
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
    
    if not WEB_DIR.exists():
        print(f"❌ Error: Web directory not found at {WEB_DIR}")
        exit(1)
    
    print("=" * 60)
    print(f"🌐 Starting web server on http://localhost:{PORT}")
    print(f"🔌 Backend API should be running on http://localhost:{BACKEND_PORT}")
    print(f"📱 Open your browser: http://localhost:{PORT}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
