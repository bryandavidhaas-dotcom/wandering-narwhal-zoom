import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Heart, ExternalLink } from "lucide-react";

interface DonationContainerProps {
  className?: string;
}

const DonationContainer = ({ className = "" }: DonationContainerProps) => {
  const handleVenmoClick = () => {
    window.open('https://venmo.com/code?user_id=3869666086749484258&created=1758346609', '_blank', 'noopener,noreferrer');
  };

  const handlePayPalClick = () => {
    window.open('https://www.paypal.me/BHaas', '_blank', 'noopener,noreferrer');
  };

  return (
    <Card className={`border-2 border-pink-200 bg-gradient-to-r from-pink-50 to-red-50 ${className}`}>
      <CardContent className="p-6">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <Heart className="h-8 w-8 text-pink-600 mr-2 fill-current animate-pulse" />
            <h3 className="text-xl font-semibold text-gray-900">Support Our Mission</h3>
          </div>
          
          <p className="text-gray-700 mb-6 text-lg leading-relaxed">
            If you'd like to help me keep building, a small contribution goes a long way.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              variant="outline"
              size="sm"
              onClick={handlePayPalClick}
              className="border-blue-500 text-blue-600 hover:bg-blue-50"
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              PayPal Donation
            </Button>
            
            <Button
              variant="outline"
              size="sm"
              onClick={handleVenmoClick}
              className="border-blue-500 text-blue-600 hover:bg-blue-50"
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              Venmo Donation
            </Button>
          </div>
          
          <div className="mt-6 text-sm text-gray-600">
            <p>Your support helps maintain and improve this free career discovery platform.</p>
            <p className="mt-1">Thank you for considering a donation! 🙏</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default DonationContainer;