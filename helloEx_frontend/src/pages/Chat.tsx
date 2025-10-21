import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Send, Mic, Sparkles, Heart, Settings, Clock } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const Chat = () => {
  const { sessionId } = useParams();
  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  
  // Mock conversation data
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hey... it's good to hear from you. How have you been?",
      timestamp: new Date(Date.now() - 3600000)
    },
    {
      id: "2", 
      role: "user",
      content: "I've been thinking about us a lot lately. About the good times we had.",
      timestamp: new Date(Date.now() - 3000000)
    },
    {
      id: "3",
      role: "assistant", 
      content: "I remember those times too. Like that weekend we spent at the beach, watching the sunset. You always said those were your favorite moments.",
      timestamp: new Date(Date.now() - 2400000)
    }
  ]);

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages([...messages, newMessage]);
    setInputMessage("");
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "I understand what you're feeling. Those memories are precious to both of us.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-warm">
      {/* Header */}
      <header className="border-b glass-effect sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link to="/dashboard">
                <Button variant="ghost" size="icon">
                  <ArrowLeft className="h-5 w-5" />
                </Button>
              </Link>
              <div>
                <h2 className="text-lg font-semibold">Conversation with Alex</h2>
                <p className="text-sm text-muted-foreground">Nostalgic mode • Active</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon">
                <Settings className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto scrollbar-thin">
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <div className="space-y-6">
            {messages.map((message, index) => (
              <div
                key={message.id}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"} animate-scale-in`}
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className={`max-w-[80%] ${message.role === "user" ? "order-2" : "order-1"}`}>
                  <Card className={`p-4 hover-lift transition-all duration-300 ${
                    message.role === "user" 
                      ? "bg-gradient-hero text-white shadow-soft hover:shadow-glow" 
                      : "bg-card border-2 hover:border-primary/30"
                  }`}>
                    <p className="leading-relaxed">{message.content}</p>
                    <p className={`text-xs mt-2 flex items-center gap-1 ${
                      message.role === "user" ? "text-white/70" : "text-muted-foreground"
                    }`}>
                      <Clock className="h-3 w-3" />
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </Card>
                </div>
              </div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex justify-start animate-scale-in">
                <Card className="p-4 bg-card border-2">
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
                      <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                    </div>
                    <span className="text-sm text-muted-foreground">Typing...</span>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t glass-effect">
        <div className="container mx-auto px-4 py-6 max-w-4xl">
          {/* Mode Selector */}
          <div className="flex gap-2 mb-4 flex-wrap">
            <Button variant="warm" size="sm" className="gap-2 hover-lift">
              <Heart className="h-4 w-4 animate-pulse-soft" />
              Nostalgic
            </Button>
            <Button variant="ghost" size="sm" className="hover-lift">Closure</Button>
            <Button variant="ghost" size="sm" className="hover-lift">Reflective</Button>
          </div>

          {/* Input Form */}
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage();
                  }
                }}
                placeholder="Type your message..."
                className="min-h-[60px] resize-none pr-12 rounded-xl border-2 focus:border-primary/50 focus:shadow-soft transition-all"
              />
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-2 bottom-2 hover:scale-110 transition-transform"
              >
                <Mic className="h-5 w-5" />
              </Button>
            </div>
            <Button 
              onClick={handleSendMessage}
              disabled={!inputMessage.trim()}
              variant="hero"
              size="icon"
              className="h-[60px] w-[60px] rounded-xl hover:scale-105 transition-transform disabled:hover:scale-100"
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>

          {/* Quick Prompts */}
          <div className="flex gap-2 mt-4 flex-wrap">
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => setInputMessage("I miss the way we used to...")}
              className="text-xs gap-1 hover-lift hover:border-primary/50"
            >
              <Sparkles className="h-3 w-3 animate-pulse-soft" />
              I miss...
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => setInputMessage("Do you remember when...")}
              className="text-xs gap-1 hover-lift hover:border-primary/50"
            >
              <Sparkles className="h-3 w-3 animate-pulse-soft" />
              Remember when...
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => setInputMessage("I want to understand...")}
              className="text-xs gap-1 hover-lift hover:border-primary/50"
            >
              <Sparkles className="h-3 w-3 animate-pulse-soft" />
              Help me understand...
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
