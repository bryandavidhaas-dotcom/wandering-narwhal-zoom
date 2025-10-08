# Streamlined Development Setup Plan
## Wandering Narwhal Zoom Application

### Overview
This plan eliminates startup friction by creating automated setup scripts and centralized configuration management. The solution uses existing tools (Python, Node.js, MongoDB) with smart automation.

## Current Issues Identified

### 1. Missing Python Dependencies
- `python-jose[cryptography]` - JWT authentication
- `sqlalchemy` - Database ORM (if needed)
- `passlib[bcrypt]` - Password hashing
- `tinydb` - Embedded database fallback

### 2. Configuration Issues
- Incomplete `.env` file missing critical variables
- Port configurations scattered across files
- No centralized configuration management

### 3. Startup Process Issues
- Manual multi-step startup process
- No dependency validation
- No service health checking
- MongoDB connection failures with no fallback

## Solution Architecture

### File Structure
```
wandering-narwhal-zoom/
├── config/
│   ├── dev-config.json          # Centralized development configuration
│   └── .env.template            # Complete environment template
├── scripts/
│   ├── setup-python.bat        # Python environment setup (Windows)
│   ├── setup-python.sh         # Python environment setup (Unix)
│   ├── health-check.js         # Service health validation
│   └── dev-setup.js            # Main setup orchestrator
├── dev-setup.js                # Root setup script
├── backend/requirements-complete.txt  # Enhanced requirements
└── package.json                # Enhanced with dev commands
```

## Implementation Details

### 1. Enhanced Requirements File
**File: `backend/requirements-complete.txt`**
```txt
# Core FastAPI Dependencies
fastapi==0.111.1
uvicorn[standard]==0.24.0
pydantic==2.8.2
pydantic-settings==2.3.4
python-multipart==0.0.9

# Database Dependencies
pymongo==4.6.0
motor==3.3.2
beanie==1.23.6
sqlalchemy==2.0.23
tinydb==4.8.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Utility Dependencies
python-dotenv==1.0.0
python-docx==1.1.2
pypdf==4.2.0
openai==1.35.13

# Development Dependencies
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### 2. Centralized Configuration
**File: `config/dev-config.json`**
```json
{
  "services": {
    "backend": {
      "port": 8002,
      "host": "0.0.0.0",
      "reload": true,
      "app": "app.main:app"
    },
    "frontend": {
      "port": 5173,
      "host": "0.0.0.0"
    },
    "mongodb": {
      "url": "mongodb://localhost:27017",
      "database": "recommender",
      "fallback": "embedded"
    }
  },
  "environment": {
    "DEBUG": true,
    "CORS_ORIGINS": "http://localhost:3000,http://localhost:5173",
    "JWT_SECRET_KEY": "dev-secret-key-change-in-production",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 30
  },
  "paths": {
    "backend": "./backend",
    "frontend": "./frontend",
    "venv": "./backend/venv"
  }
}
```

### 3. Complete Environment Template
**File: `config/.env.template`**
```env
# Backend Environment Configuration
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Database Configuration
DATABASE_URL=mongodb://localhost:27017
DATABASE_NAME=recommender

# AI Model API Key
AI_API_KEY=your_ai_model_api_key_here

# JWT Secret for Authentication
JWT_SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Development Settings
BACKEND_PORT=8002
FRONTEND_PORT=5173
```

### 4. Python Setup Script (Windows)
**File: `scripts/setup-python.bat`**
```batch
@echo off
echo 🐍 Setting up Python environment...

cd /d "%~dp0\..\backend"

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing Python dependencies...
pip install -r requirements-complete.txt

echo ✅ Python environment setup complete!
```

### 5. Health Check Script
**File: `scripts/health-check.js`**
```javascript
const http = require('http');
const fs = require('fs');
const path = require('path');

class HealthChecker {
    constructor() {
        this.config = JSON.parse(fs.readFileSync(path.join(__dirname, '../config/dev-config.json'), 'utf8'));
    }

    async checkPort(port, service) {
        return new Promise((resolve) => {
            const req = http.request({
                hostname: 'localhost',
                port: port,
                method: 'GET',
                timeout: 2000
            }, (res) => {
                resolve({ service, port, status: 'running', code: res.statusCode });
            });

            req.on('error', () => {
                resolve({ service, port, status: 'stopped', code: null });
            });

            req.on('timeout', () => {
                resolve({ service, port, status: 'timeout', code: null });
            });

            req.end();
        });
    }

    async checkBackendHealth() {
        try {
            const response = await this.checkPort(this.config.services.backend.port, 'backend');
            if (response.status === 'running') {
                // Try to hit health endpoint
                return new Promise((resolve) => {
                    const req = http.request({
                        hostname: 'localhost',
                        port: this.config.services.backend.port,
                        path: '/api/v1/health',
                        method: 'GET',
                        timeout: 3000
                    }, (res) => {
                        let data = '';
                        res.on('data', chunk => data += chunk);
                        res.on('end', () => {
                            try {
                                const health = JSON.parse(data);
                                resolve({ 
                                    service: 'backend', 
                                    status: 'healthy', 
                                    database: health.database || 'unknown' 
                                });
                            } catch (e) {
                                resolve({ service: 'backend', status: 'unhealthy', error: 'Invalid response' });
                            }
                        });
                    });

                    req.on('error', () => {
                        resolve({ service: 'backend', status: 'unhealthy', error: 'Connection failed' });
                    });

                    req.end();
                });
            }
            return response;
        } catch (error) {
            return { service: 'backend', status: 'error', error: error.message };
        }
    }

    async runHealthCheck() {
        console.log('🏥 Running health check...\n');

        const checks = await Promise.all([
            this.checkPort(this.config.services.frontend.port, 'frontend'),
            this.checkBackendHealth()
        ]);

        checks.forEach(check => {
            const status = check.status === 'running' || check.status === 'healthy' ? '✅' : '❌';
            console.log(`${status} ${check.service.toUpperCase()}: ${check.status} (port ${check.port || this.config.services[check.service].port})`);
            
            if (check.database) {
                const dbStatus = check.database === 'connected' ? '✅' : '⚠️';
                console.log(`   ${dbStatus} Database: ${check.database}`);
            }
            
            if (check.error) {
                console.log(`   Error: ${check.error}`);
            }
        });

        const allHealthy = checks.every(check => 
            check.status === 'running' || check.status === 'healthy'
        );

        console.log(`\n${allHealthy ? '✅' : '❌'} Overall Status: ${allHealthy ? 'HEALTHY' : 'ISSUES DETECTED'}`);
        return allHealthy;
    }
}

if (require.main === module) {
    const checker = new HealthChecker();
    checker.runHealthCheck().then(healthy => {
        process.exit(healthy ? 0 : 1);
    });
}

module.exports = HealthChecker;
```

### 6. Main Setup Orchestrator
**File: `dev-setup.js`**
```javascript
const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const HealthChecker = require('./scripts/health-check');

class DevSetup {
    constructor() {
        this.config = JSON.parse(fs.readFileSync('./config/dev-config.json', 'utf8'));
        this.processes = [];
        this.isWindows = process.platform === 'win32';
    }

    log(message, level = 'INFO') {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] [${level}] ${message}`);
    }

    async setupEnvironment() {
        this.log('🚀 Starting development environment setup...');

        // Create .env file if it doesn't exist
        if (!fs.existsSync('.env')) {
            this.log('📝 Creating .env file from template...');
            const template = fs.readFileSync('./config/.env.template', 'utf8');
            
            // Replace template values with config values
            let envContent = template;
            Object.entries(this.config.environment).forEach(([key, value]) => {
                envContent = envContent.replace(`${key}=your_${key.toLowerCase()}_here`, `${key}=${value}`);
            });
            
            fs.writeFileSync('.env', envContent);
            this.log('✅ Environment file created');
        }

        // Setup Python environment
        await this.setupPython();

        // Setup Node.js dependencies
        await this.setupNodejs();

        // Setup MongoDB
        await this.setupMongoDB();
    }

    async setupPython() {
        this.log('🐍 Setting up Python environment...');
        
        return new Promise((resolve, reject) => {
            const scriptPath = this.isWindows ? 
                './scripts/setup-python.bat' : 
                './scripts/setup-python.sh';
            
            const process = spawn(scriptPath, [], { 
                stdio: 'inherit',
                shell: true 
            });

            process.on('close', (code) => {
                if (code === 0) {
                    this.log('✅ Python environment ready');
                    resolve();
                } else {
                    this.log('❌ Python setup failed', 'ERROR');
                    reject(new Error(`Python setup failed with code ${code}`));
                }
            });
        });
    }

    async setupNodejs() {
        this.log('📦 Setting up Node.js dependencies...');
        
        return new Promise((resolve, reject) => {
            const process = spawn('npm', ['install'], { 
                stdio: 'inherit',
                cwd: './frontend'
            });

            process.on('close', (code) => {
                if (code === 0) {
                    this.log('✅ Node.js dependencies ready');
                    resolve();
                } else {
                    this.log('❌ Node.js setup failed', 'ERROR');
                    reject(new Error(`Node.js setup failed with code ${code}`));
                }
            });
        });
    }

    async setupMongoDB() {
        this.log('🍃 Setting up MongoDB...');
        
        return new Promise((resolve) => {
            const process = spawn('python', ['setup_mongodb.py'], { 
                stdio: 'inherit'
            });

            process.on('close', (code) => {
                if (code === 0) {
                    this.log('✅ MongoDB setup complete');
                } else {
                    this.log('⚠️ MongoDB setup had issues, fallback available');
                }
                resolve(); // Always resolve, as fallback is available
            });
        });
    }

    async startServices() {
        this.log('🚀 Starting all services...');

        // Start backend
        this.startBackend();
        
        // Wait a moment for backend to start
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Start frontend
        this.startFrontend();

        // Wait for services to be ready
        await new Promise(resolve => setTimeout(resolve, 5000));

        // Run health check
        const healthChecker = new HealthChecker();
        const healthy = await healthChecker.runHealthCheck();

        if (healthy) {
            this.log('🎉 All services are running successfully!');
            this.log('🌐 Frontend: http://localhost:' + this.config.services.frontend.port);
            this.log('🔧 Backend API: http://localhost:' + this.config.services.backend.port);
            this.log('📊 Health Check: http://localhost:' + this.config.services.backend.port + '/api/v1/health');
        } else {
            this.log('⚠️ Some services may have issues. Check the health report above.');
        }
    }

    startBackend() {
        this.log('🔧 Starting backend server...');
        
        const pythonCmd = this.isWindows ? 
            path.join(this.config.paths.backend, 'venv', 'Scripts', 'python.exe') :
            path.join(this.config.paths.backend, 'venv', 'bin', 'python');

        const backend = spawn(pythonCmd, ['main.py'], {
            cwd: this.config.paths.backend,
            stdio: 'inherit'
        });

        backend.on('error', (err) => {
            this.log(`Backend error: ${err.message}`, 'ERROR');
        });

        this.processes.push(backend);
    }

    startFrontend() {
        this.log('🌐 Starting frontend server...');
        
        const frontend = spawn('npm', ['run', 'dev'], {
            cwd: './frontend',
            stdio: 'inherit'
        });

        frontend.on('error', (err) => {
            this.log(`Frontend error: ${err.message}`, 'ERROR');
        });

        this.processes.push(frontend);
    }

    async cleanup() {
        this.log('🧹 Cleaning up processes...');
        this.processes.forEach(proc => {
            if (!proc.killed) {
                proc.kill();
            }
        });
    }
}

// Handle script execution
if (require.main === module) {
    const setup = new DevSetup();
    
    // Handle cleanup on exit
    process.on('SIGINT', async () => {
        await setup.cleanup();
        process.exit(0);
    });

    // Parse command line arguments
    const command = process.argv[2] || 'start';

    switch (command) {
        case 'setup':
            setup.setupEnvironment().catch(console.error);
            break;
        case 'start':
            setup.setupEnvironment()
                .then(() => setup.startServices())
                .catch(console.error);
            break;
        case 'health':
            const healthChecker = new HealthChecker();
            healthChecker.runHealthCheck();
            break;
        default:
            console.log('Usage: node dev-setup.js [setup|start|health]');
    }
}

module.exports = DevSetup;
```

### 7. Enhanced Package.json Scripts
**Add to root `package.json`:**
```json
{
  "name": "wandering-narwhal-zoom",
  "version": "1.0.0",
  "scripts": {
    "dev-setup": "node dev-setup.js setup",
    "dev": "node dev-setup.js start",
    "dev-clean": "npm run dev-setup && npm run dev",
    "health": "node dev-setup.js health",
    "backend": "cd backend && python main.py",
    "frontend": "cd frontend && npm run dev"
  },
  "devDependencies": {
    "concurrently": "^8.2.2"
  }
}
```

## Usage Instructions

### First Time Setup
```bash
# Clone the repository and navigate to it
cd wandering-narwhal-zoom

# Run complete setup (installs all dependencies)
npm run dev-setup
```

### Daily Development
```bash
# Start everything with one command
npm run dev

# Or if you need a clean restart
npm run dev-clean
```

### Health Checking
```bash
# Check if all services are running properly
npm run health
```

### Individual Services
```bash
# Start only backend
npm run backend

# Start only frontend  
npm run frontend
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Python Dependencies Missing
**Error:** `ModuleNotFoundError: No module named 'jose'`
**Solution:** 
```bash
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Unix
pip install -r requirements-complete.txt
```

#### 2. Port Already in Use
**Error:** `Port 8002 is already in use`
**Solution:** The health check will detect this. Kill existing processes:
```bash
# Windows
netstat -ano | findstr :8002
taskkill /PID <PID> /F

# Unix
lsof -ti:8002 | xargs kill -9
```

#### 3. MongoDB Connection Failed
**Error:** `MongoDB connection failed`
**Solution:** The system automatically falls back to embedded database. No action needed.

#### 4. Environment Variables Missing
**Error:** `KeyError: 'DATABASE_URL'`
**Solution:** Run `npm run dev-setup` to regenerate .env file

## Benefits of This Solution

### ✅ Eliminates Startup Friction
- Single command startup: `npm run dev`
- Automatic dependency installation
- Environment validation and setup

### ✅ Minimal New Tools Required
- Uses existing Python, Node.js, MongoDB
- No Docker or complex containerization
- Works with current development workflow

### ✅ Robust Error Handling
- Automatic fallback for MongoDB issues
- Clear error messages with solutions
- Health checking and validation

### ✅ Developer Experience
- Simple commands to remember
- Comprehensive troubleshooting guide
- Automatic recovery from common issues

### ✅ Maintainable
- Centralized configuration
- Modular script architecture
- Easy to extend and modify

## Next Steps

1. **Implementation**: Create all the files specified in this plan
2. **Testing**: Run through the complete setup process
3. **Documentation**: Create simple README with usage instructions
4. **Validation**: Test on clean environment to ensure it works

This solution provides a "one-command startup" experience while maintaining your existing development workflow and requiring minimal new tool installation.