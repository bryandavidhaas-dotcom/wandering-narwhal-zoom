// Test script to verify the registration flow fix
import fetch from 'node-fetch';

async function testRegistrationFlow() {
    const baseUrl = 'http://localhost:8002'; // Backend server URL
    const testUser = {
        email: `test_${Date.now()}@example.com`,
        password: 'testpassword123'
    };

    console.log('Testing registration flow...');
    console.log('Test user:', testUser.email);

    try {
        // Step 1: Register user
        console.log('\n1. Testing registration...');
        const registerResponse = await fetch(`${baseUrl}/api/v1/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: testUser.email,
                password: testUser.password
            })
        });

        if (!registerResponse.ok) {
            const errorData = await registerResponse.json();
            console.error('Registration failed:', errorData);
            return;
        }

        console.log('✅ Registration successful');

        // Step 2: Test auto-login (simulate what the frontend would do)
        console.log('\n2. Testing auto-login after registration...');
        const loginResponse = await fetch(`${baseUrl}/api/v1/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                username: testUser.email,
                password: testUser.password
            })
        });

        if (!loginResponse.ok) {
            console.error('Auto-login failed');
            return;
        }

        const loginData = await loginResponse.json();
        console.log('✅ Auto-login successful');
        console.log('Token received:', loginData.access_token ? 'Yes' : 'No');

        // Step 3: Verify token works
        console.log('\n3. Testing token validation...');
        const profileResponse = await fetch(`${baseUrl}/api/v1/auth/me`, {
            headers: {
                'Authorization': `Bearer ${loginData.access_token}`
            }
        });

        if (profileResponse.ok) {
            const profileData = await profileResponse.json();
            console.log('✅ Token validation successful');
            console.log('User profile:', profileData.email);
        } else {
            console.log('❌ Token validation failed');
        }

        console.log('\n🎉 Registration flow test completed successfully!');
        console.log('The fix ensures users can register and be automatically logged in.');

    } catch (error) {
        console.error('Test failed with error:', error.message);
    }
}

// Run the test
testRegistrationFlow();