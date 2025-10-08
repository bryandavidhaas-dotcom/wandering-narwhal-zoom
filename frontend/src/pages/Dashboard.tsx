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
  const recommendationsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchLatestRecommendations = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/auth");
        return;
      }

      try {
        const response = await fetch("/api/v1/get-latest-recommendations", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data) {
            setRecommendations(data.recommendations);
            setRecommendationSetId(data._id);
            setConversation([{ type: "ai", text: "Here are your initial recommendations. How can I help you refine them?" }]);
          }
        } else {
          showError("Failed to fetch latest recommendations.");
        }
      } catch (error) {
        showError("An error occurred while fetching latest recommendations.");
      }
    };

    fetchLatestRecommendations();
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
              <p>No recommendations found. Please complete your assessment.</p>
            )}
          </CardContent>
        </Card>

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
      </div>
    </div>
  );
};

export default Dashboard;