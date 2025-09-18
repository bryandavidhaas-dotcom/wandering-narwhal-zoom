import React from 'react';
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing";
import Auth from "./pages/Auth";
import Assessment from "./pages/Assessment";
import Dashboard from "./pages/Dashboard";
import CareerDetail from "./pages/CareerDetail";
import SystemCheck from "./pages/SystemCheck";
import CareerTemplateCheck from "./pages/CareerTemplateCheck";
import SystemTest from "./pages/SystemTest";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      refetchOnWindowFocus: false,
    },
  },
});

const App = () => {
  console.log('🚀 App component rendering...');
  console.log('📍 Current URL:', window.location.href);
  
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/assessment" element={<Assessment />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/career/:careerType" element={<CareerDetail />} />
            <Route path="/system-check" element={<SystemCheck />} />
            <Route path="/career-template-check" element={<CareerTemplateCheck />} />
            <Route path="/system-test" element={<SystemTest />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;