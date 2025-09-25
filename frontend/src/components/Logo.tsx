import React from 'react';
import { Search } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  variant?: 'light' | 'dark';
}

export const Logo: React.FC<LogoProps> = ({ size = 'md', className, variant = 'light' }) => {
  const sizeClasses = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl'
  };

  const iconSizes = {
    sm: 'h-7 w-7',
    md: 'h-8 w-8',
    lg: 'h-10 w-10'
  };

  const textColor = variant === 'dark' ? 'text-white' : 'text-gray-900';

  return (
    <div className={cn('flex items-center space-x-2', className)}>
      <Search className={cn('text-blue-600', iconSizes[size])} strokeWidth={3} />
      <div className={cn('flex flex-col font-bold', textColor, sizeClasses[size])}>
        <span className="uppercase">
          C<span className="text-blue-600">A</span>REER
        </span>
        <span className="uppercase" style={{ marginLeft: '0.4rem' }}>
          F<span className="text-blue-600">I</span>NDER
        </span>
      </div>
    </div>
  );
};