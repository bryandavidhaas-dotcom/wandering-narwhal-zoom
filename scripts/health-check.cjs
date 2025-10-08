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