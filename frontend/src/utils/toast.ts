// Simple toast utility functions
// In a real app, you might use react-hot-toast or similar

export const showSuccess = (message: string) => {
  console.log('✅ Success:', message);
  // You can implement actual toast notifications here
  // For now, we'll just log to console
};

export const showError = (message: string) => {
  console.error('❌ Error:', message);
  // You can implement actual toast notifications here
  // For now, we'll just log to console
};

export const showInfo = (message: string) => {
  console.log('ℹ️ Info:', message);
  // You can implement actual toast notifications here
  // For now, we'll just log to console
};

export const showWarning = (message: string) => {
  console.warn('⚠️ Warning:', message);
  // You can implement actual toast notifications here
  // For now, we'll just log to console
};