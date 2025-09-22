import { toast } from "@/hooks/use-toast";

export const showSuccess = (message: string) => {
  console.log('✅ Success:', message);
  toast({
    title: "Success",
    description: message,
    variant: "default",
  });
};

export const showError = (message: string) => {
  console.error('❌ Error:', message);
  toast({
    title: "Error",
    description: message,
    variant: "destructive",
  });
};

export const showInfo = (message: string) => {
  console.log('ℹ️ Info:', message);
  toast({
    title: "Info",
    description: message,
    variant: "default",
  });
};

export const showWarning = (message: string) => {
  console.warn('⚠️ Warning:', message);
  toast({
    title: "Warning",
    description: message,
    variant: "default",
  });
};