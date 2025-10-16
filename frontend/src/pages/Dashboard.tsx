import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { showSuccess, showError } from "@/utils/toast";
import { API_CONFIG, buildApiUrl } from "@/config/api";

interface Recommendation {
  job_title: string;
  company: string;
  location: string;
  description: string;
  requirements: string[];
}

interface ConversationTurn {
  type: "user" | "ai";
  text: string;
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [recommendationSetId, setRecommendationSetId] = useState<string | null>(null);
  const [prompt, setPrompt] = useState("");
  const [isTuning, setIsTuning] = useState(false);
  const [conversation, setConversation] = useState<ConversationTurn[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [hasAssessment, setHasAssessment] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);
  const recommendationsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const checkAssessmentAndFetchRecommendations = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/auth");
        return;
      }

      setIsLoading(true);
      setError(null);

      try {
        // First, check if user has completed an assessment
        const assessmentResponse = await fetch("/api/v1/assessment/get-latest-assessment", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (assessmentResponse.status === 404) {
          // No assessment found - redirect to assessment page
          setHasAssessment(false);
          setIsLoading(false);
          navigate("/assessment");
          return;
        }

        if (!assessmentResponse.ok) {
          throw new Error("Failed to check assessment status");
        }

        // Assessment exists, now try to fetch recommendations
        setHasAssessment(true);
        
        const recommendationsResponse = await fetch("/api/v1/recommendation/get-latest-recommendations", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (recommendationsResponse.status === 404) {
          // Assessment exists but no recommendations yet - generate them
          setError("No recommendations found. Generating recommendations from your assessment...");
          
          const generateResponse = await fetch("/api/v1/recommendation/generate-recommendations", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          });

          if (generateResponse.ok) {
            const data = await generateResponse.json();
            setRecommendations(data.recommendations);
            setRecommendationSetId(data._id);
            setConversation([{ type: "ai", text: "Here are your initial recommendations based on your assessment. How can I help you refine them?" }]);
            setError(null);
          } else {
            setError("Failed to generate recommendations. Please try again.");
          }
        } else if (recommendationsResponse.ok) {
          // Recommendations exist - load them
          const data = await recommendationsResponse.json();
          setRecommendations(data.recommendations);
          setRecommendationSetId(data._id);
          setConversation([{ type: "ai", text: "Here are your recommendations. How can I help you refine them?" }]);
        } else {
          setError("Failed to fetch recommendations.");
        }

      } catch (error) {
        console.error("Dashboard error:", error);
        setError("An error occurred while loading your dashboard. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    checkAssessmentAndFetchRecommendations();
  }, [navigate]);

  const handleTune = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      showError("You must be logged in to tune recommendations.");
      return;
    }

    setIsTuning(true);
    const userPrompt = prompt;
    setConversation(prev => [...prev, { type: "user", text: userPrompt }]);
    setPrompt("");

    try {
      const response = await fetch(buildApiUrl(API_CONFIG.ENDPOINTS.AI_TUNE), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          recommendations: { recommendations },
          prompt: userPrompt,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setRecommendations(data.recommendations);
        setConversation(prev => [...prev, { type: "ai", text: "I've updated your recommendations based on your feedback." }]);
        showSuccess("Recommendations tuned successfully!");
        if (recommendationsRef.current) {
          recommendationsRef.current.scrollIntoView({ behavior: "smooth" });
        }
      } else {
        showError("Failed to tune recommendations.");
        setConversation(prev => [...prev, { type: "ai", text: "I'm sorry, I wasn't able to refine your recommendations. Please try again." }]);
      }
    } catch (error) {
      showError("An error occurred while tuning recommendations.");
      setConversation(prev => [...prev, { type: "ai", text: "I'm sorry, an error occurred. Please try again." }]);
    } finally {
      setIsTuning(false);
    }
  };

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-background text-foreground p-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-card text-card-foreground">
            <CardHeader>
              <CardTitle>Loading Your Dashboard...</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                <span className="ml-3">Checking your assessment and recommendations...</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Show error state
  if (error) {
    return (
      <div className="min-h-screen bg-background text-foreground p-8">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-card text-card-foreground">
            <CardHeader>
              <CardTitle>Dashboard</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                  <p className="text-yellow-800">{error}</p>
                </div>
                <Button onClick={() => window.location.reload()} className="mr-4">
                  Retry
                </Button>
                <Button variant="outline" onClick={() => navigate("/assessment")}>
                  Go to Assessment
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Show main dashboard
  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-4xl mx-auto">
        <Card ref={recommendationsRef} className="bg-card text-card-foreground">
          <CardHeader>
            <CardTitle>Your Career Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            {recommendations.length > 0 ? (
              <ul>
                {recommendations.map((rec, index) => (
                  <li key={index} className="mb-2">
                    <p><strong>{rec.job_title}</strong> at {rec.company} ({rec.location})</p>
                    <p>{rec.description}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-600 mb-4">No recommendations available yet.</p>
                <Button onClick={() => navigate("/assessment")}>
                  Complete Assessment
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {recommendations.length > 0 && (
          <Card className="mt-8 bg-card text-card-foreground">
            <CardHeader>
              <CardTitle>Tune Your Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  {conversation.map((turn, index) => (
                    <div key={index} className={`p-2 rounded-lg ${turn.type === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
                      <p><strong>{turn.type === 'user' ? 'You' : 'AI'}:</strong> {turn.text}</p>
                    </div>
                  ))}
                </div>
                <div>
                  <Label htmlFor="prompt">Your Prompt</Label>
                  <Textarea
                    id="prompt"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="e.g., 'I want something with more outdoor work'"
                    className="bg-input text-foreground"
                  />
                </div>
                <Button onClick={handleTune} disabled={isTuning}>
                  {isTuning ? "Tuning..." : "Tune"}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Dashboard;