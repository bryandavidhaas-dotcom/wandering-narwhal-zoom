import * as React from "react"
import { cn } from "@/lib/utils"

const MessageSquare = React.forwardRef<
  SVGSVGElement,
  React.SVGProps<SVGSVGElement>
>(({ className, ...props }, ref) => (
  <svg
    ref={ref}
    className={cn("h-4 w-4", className)}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a9.954 9.954 0 01-4.951-1.322A3.5 3.5 0 013 13.5V7a4 4 0 014-4h10a4 4 0 014 4v5z"
    />
  </svg>
))
MessageSquare.displayName = "MessageSquare"

export { MessageSquare }