import React from 'react';
import { Search } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Logo: React.FC<LogoProps> = ({ size = 'md', className }) => {
  const sizeClasses = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl'
  };

  const iconSizes = {
    sm: 'h-5 w-5',
    md: 'h-6 w-6', 
    lg: 'h-8 w-8'
  };

  return (
    <div className={cn('flex items-center space-x-2', className)}>
      <Search className={cn('text-blue-600', iconSizes[size])} />
      <span className={cn('font-semibold text-gray-900', sizeClasses[size])}>
        Career Discovery
      </span>
    </div>
  );
};