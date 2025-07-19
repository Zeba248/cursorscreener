#!/usr/bin/env python3
"""
Simple startup script for the Django Stock Screener
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and print status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Starting Django Stock Screener Setup...")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the Django project directory.")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python3 manage.py migrate", "Running database migrations"):
        sys.exit(1)
    
    # Update stock data
    if not run_command("python3 manage.py update_stocks", "Updating stock data"):
        print("⚠️  Warning: Stock data update failed, but continuing...")
    
    # Start the development server
    print("\n🎯 Starting Django development server...")
    print("📱 Open your browser and go to: http://127.0.0.1:8000/")
    print("🔧 Admin interface available at: http://127.0.0.1:8000/admin/")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run("python3 manage.py runserver", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Django server stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()