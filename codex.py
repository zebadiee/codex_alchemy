#!/usr/bin/env python3
"""
Codex Alchemy System Orchestrator
Unified script for managing the complete Codex system
"""

import asyncio
import subprocess
import sys
import time
import os
from pathlib import Path
from datetime import datetime

class CodexOrchestrator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.frontend_process = None
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def run_command(self, command: str, cwd: str = None, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command"""
        self.log(f"Running: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd or str(self.project_root),
                capture_output=True,
                text=True,
                check=check
            )
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e}", "ERROR")
            if e.stderr:
                print(f"Error: {e.stderr}")
            raise
    
    async def check_database(self) -> bool:
        """Check if database exists and has data"""
        try:
            # Try to import and check database
            sys.path.append(str(self.project_root / "backend"))
            from backend.db import async_session_maker
            from backend.models import Glyph, SigilMetadata
            from sqlalchemy import select
            
            async with async_session_maker() as session:
                result = await session.execute(select(Glyph))
                glyph_count = len(result.scalars().all())
                
                result = await session.execute(select(SigilMetadata))
                sigil_count = len(result.scalars().all())
                
                self.log(f"Database check: {glyph_count} glyphs, {sigil_count} sigil metadata")
                return glyph_count > 0 and sigil_count > 0
                
        except Exception as e:
            self.log(f"Database check failed: {e}", "ERROR")
            return False
    
    async def run_migration(self) -> bool:
        """Run the vault to SQL migration"""
        self.log("🔄 Starting vault to SQL migration...")
        try:
            result = self.run_command("python scripts/migrate_vault_to_sql.py")
            if result.returncode == 0:
                self.log("✅ Migration completed successfully")
                return True
            else:
                self.log("❌ Migration failed", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Migration error: {e}", "ERROR")
            return False
    
    def start_backend(self) -> bool:
        """Start the FastAPI backend server"""
        self.log("🚀 Starting FastAPI backend...")
        try:
            # Kill any existing processes on port 8000
            self.run_command("lsof -ti:8000 | xargs kill -9", check=False)
            
            # Start backend
            self.backend_process = subprocess.Popen(
                ["python", "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000"],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to start
            time.sleep(3)
            
            # Test if backend is responding
            try:
                result = subprocess.run(
                    ["curl", "-s", "http://localhost:8000/docs"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    self.log("✅ Backend started successfully")
                    return True
                else:
                    self.log("❌ Backend not responding", "ERROR")
                    return False
            except Exception as e:
                self.log(f"❌ Backend test failed: {e}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Failed to start backend: {e}", "ERROR")
            return False
    
    def start_frontend(self) -> bool:
        """Start the Next.js frontend"""
        self.log("🎨 Starting Next.js frontend...")
        try:
            # Kill any existing processes on port 3004
            self.run_command("lsof -ti:3004 | xargs kill -9", check=False)
            
            # Start frontend
            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=str(self.project_root / "frontend"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for frontend to start
            time.sleep(5)
            
            # Test if frontend is responding
            try:
                result = subprocess.run(
                    ["curl", "-s", "http://localhost:3004"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and "Spiral Codex Dashboard" in result.stdout:
                    self.log("✅ Frontend started successfully")
                    return True
                else:
                    self.log("❌ Frontend not responding", "ERROR")
                    return False
            except Exception as e:
                self.log(f"❌ Frontend test failed: {e}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Failed to start frontend: {e}", "ERROR")
            return False
    
    async def validate_system(self) -> bool:
        """Validate the complete system"""
        self.log("🔍 Validating system...")
        
        # Test backend endpoints
        try:
            # Test vault endpoint
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8000/api/vault/glyphs"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                glyphs = result.stdout.strip()
                if glyphs and glyphs != "[]":
                    self.log(f"✅ Vault endpoint working - found glyphs")
                else:
                    self.log("⚠️ Vault endpoint working but no glyphs found", "WARN")
            else:
                self.log("❌ Vault endpoint failed", "ERROR")
                return False
            
            # Test stats endpoint
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8000/api/gene/stats"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.log("✅ Stats endpoint working")
            else:
                self.log("❌ Stats endpoint failed", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ System validation failed: {e}", "ERROR")
            return False
        
        return True
    
    def open_browser(self):
        """Open the frontend in browser"""
        self.log("🌐 Opening frontend in browser...")
        try:
            subprocess.run(["open", "http://localhost:3004"], check=False)
            self.log("✅ Browser opened")
        except Exception as e:
            self.log(f"⚠️ Could not open browser: {e}", "WARN")
    
    async def run_full_system(self):
        """Run the complete Codex system"""
        self.log("🧿 Codex Alchemy System Startup")
        self.log("=" * 50)
        
        try:
            # Step 1: Check database
            self.log("📊 Checking database status...")
            db_has_data = await self.check_database()
            
            if not db_has_data:
                self.log("🔄 Database empty, running migration...")
                if not await self.run_migration():
                    self.log("❌ Migration failed, aborting", "ERROR")
                    return False
            else:
                self.log("✅ Database has data, skipping migration")
            
            # Step 2: Start backend
            if not self.start_backend():
                self.log("❌ Backend startup failed, aborting", "ERROR")
                return False
            
            # Step 3: Start frontend
            if not self.start_frontend():
                self.log("❌ Frontend startup failed, aborting", "ERROR")
                return False
            
            # Step 4: Validate system
            if not await self.validate_system():
                self.log("❌ System validation failed", "ERROR")
                return False
            
            # Step 5: Open browser
            self.open_browser()
            
            self.log("=" * 50)
            self.log("🎉 Codex system is ready!")
            self.log("📱 Frontend: http://localhost:3004")
            self.log("🔧 Backend: http://localhost:8000/docs")
            self.log("💡 Press Ctrl+C to stop the system")
            
            # Keep running
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                self.log("🛑 Shutting down Codex system...")
                self.cleanup()
                
        except Exception as e:
            self.log(f"❌ System startup failed: {e}", "ERROR")
            self.cleanup()
            return False
    
    def cleanup(self):
        """Clean up processes"""
        if self.backend_process:
            self.backend_process.terminate()
            self.log("🛑 Backend stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            self.log("🛑 Frontend stopped")

async def main():
    """Main entry point"""
    orchestrator = CodexOrchestrator()
    await orchestrator.run_full_system()

if __name__ == "__main__":
    asyncio.run(main()) 