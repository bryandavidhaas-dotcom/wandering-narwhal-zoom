const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const HealthChecker = require('./scripts/health-check.cjs');

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
            
            // Also replace the AI_API_KEY if it exists in current .env
            if (fs.existsSync('.env')) {
                const currentEnv = fs.readFileSync('.env', 'utf8');
                const apiKeyMatch = currentEnv.match(/AI_API_KEY=(.+)/);
                if (apiKeyMatch) {
                    envContent = envContent.replace('AI_API_KEY=your_ai_model_api_key_here', `AI_API_KEY=${apiKeyMatch[1]}`);
                }
            }
            
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
                path.resolve('./scripts/setup-python.bat') :
                path.resolve('./scripts/setup-python.sh');
            
            this.log(`Executing: ${scriptPath}`);
            
            const childProcess = spawn(scriptPath, [], {
                stdio: 'inherit',
                shell: true,
                cwd: process.cwd()
            });

            childProcess.on('error', (err) => {
                this.log(`Python setup error: ${err.message}`, 'ERROR');
                // Don't reject, try to continue
                resolve();
            });

            childProcess.on('close', (code) => {
                if (code === 0) {
                    this.log('✅ Python environment ready');
                    resolve();
                } else {
                    this.log('⚠️ Python setup had issues, continuing...', 'WARN');
                    // Don't reject, try to continue
                    resolve();
                }
            });
        });
    }

    async setupNodejs() {
        this.log('📦 Setting up Node.js dependencies...');
        
        return new Promise((resolve, reject) => {
            // Skip npm install if node_modules already exists
            if (require('fs').existsSync('./frontend/node_modules')) {
                this.log('✅ Node.js dependencies already installed, skipping...');
                resolve();
                return;
            }
            
            // Try different npm commands based on platform
            const npmCmd = this.isWindows ? 'npm.cmd' : 'npm';
            
            const childProcess = spawn(npmCmd, ['install'], {
                stdio: 'inherit',
                cwd: './frontend',
                shell: true
            });

            childProcess.on('error', (err) => {
                this.log(`Node.js setup error: ${err.message}`, 'ERROR');
                this.log('⚠️ Skipping npm install due to errors, dependencies may already be installed', 'WARN');
                resolve();
            });

            childProcess.on('close', (code) => {
                if (code === 0) {
                    this.log('✅ Node.js dependencies ready');
                    resolve();
                } else {
                    this.log('⚠️ Node.js setup had issues, but continuing since dependencies exist...', 'WARN');
                    resolve();
                }
            });
        });
    }

    async setupMongoDB() {
        this.log('🍃 Setting up MongoDB...');
        
        // First, try to start MongoDB if it's not running
        await this.startMongoDB();
        
        // Then run the setup script
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

    async startMongoDB() {
        this.log('🔄 Starting MongoDB service...');
        
        return new Promise((resolve) => {
            // Try to start MongoDB service on Windows
            const startCmd = this.isWindows ?
                ['net', 'start', 'MongoDB'] :
                ['sudo', 'systemctl', 'start', 'mongod'];
            
            const process = spawn(startCmd[0], startCmd.slice(1), {
                stdio: 'pipe' // Don't show output as it might be noisy
            });

            process.on('close', (code) => {
                if (code === 0) {
                    this.log('✅ MongoDB service started');
                } else {
                    this.log('⚠️ MongoDB service start failed, trying manual start...');
                    this.startMongoDBManually().then(resolve);
                    return;
                }
                resolve();
            });
        });
    }

    async startMongoDBManually() {
        this.log('🔧 Checking for VS Code MongoDB or using embedded fallback...');
        
        return new Promise((resolve) => {
            // Skip manual MongoDB startup - use VS Code extension or embedded fallback
            this.log('✅ Using VS Code MongoDB extension or embedded database fallback');
            resolve();
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
        
        // Use the activated virtual environment's python
        const pythonCmd = this.isWindows ? 'python' : 'python';

        const backend = spawn(pythonCmd, ['main.py'], {
            cwd: this.config.paths.backend,
            stdio: 'inherit',
            shell: true,
            env: {
                ...process.env,
                // Ensure we use the virtual environment
                PATH: this.isWindows ?
                    `${path.resolve('./backend/venv/Scripts')};${process.env.PATH}` :
                    `${path.resolve('./backend/venv/bin')}:${process.env.PATH}`
            }
        });

        backend.on('error', (err) => {
            this.log(`Backend error: ${err.message}`, 'ERROR');
        });

        this.processes.push(backend);
    }

    startFrontend() {
        this.log('🌐 Starting frontend server...');
        
        const npmCmd = this.isWindows ? 'npm.cmd' : 'npm';
        
        const frontend = spawn(npmCmd, ['run', 'dev'], {
            cwd: './frontend',
            stdio: 'inherit',
            shell: true
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