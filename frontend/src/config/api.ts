/**
 * API Configuration
 *
 * Centralized configuration for API endpoints to avoid hardcoded URLs
 * and support different environments (development, production, etc.)
 */

// Get the API base URL from environment variables or use default
const getApiBaseUrl = (): string => {
  // Check for Vite environment variables first
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  
  // In production, this should be set via environment variables
  const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002';
  console.log(`[API Config] Using API Base URL: ${apiUrl}`);
  return apiUrl;
};

// Export the API configuration
export const API_CONFIG = {
  BASE_URL: getApiBaseUrl(),
  ENDPOINTS: {
    RECOMMENDATIONS: '/recommendation',
    HEALTH: '/health',
    AI_RECOMMENDATIONS: '/ai/recommendations',
    AI_TUNE: '/ai/tune',
  }
} as const;

// Helper function to build full API URLs
export const buildApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Export commonly used API URLs
export const API_URLS = {
  RECOMMENDATIONS: buildApiUrl(API_CONFIG.ENDPOINTS.RECOMMENDATIONS),
  HEALTH: buildApiUrl(API_CONFIG.ENDPOINTS.HEALTH),
} as const;

// Log the current API configuration in development
if (import.meta.env.DEV) {
  console.log('🔧 API Configuration:', {
    baseUrl: API_CONFIG.BASE_URL,
    recommendationsUrl: API_URLS.RECOMMENDATIONS,
    environment: import.meta.env.MODE
  });
}