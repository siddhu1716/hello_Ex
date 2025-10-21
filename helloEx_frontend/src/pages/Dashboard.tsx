import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Plus, MessageCircle, Heart, Clock, Settings, LogOut, TrendingUp } from "lucide-react";

const Dashboard = () => {
  // Mock data for sessions
  const sessions = [
    {
      id: "1",
      title: "Conversation with Alex",
      lastMessage: "I've been thinking about our last summer together...",
      timestamp: "2 hours ago",
      mood: "nostalgic",
      messageCount: 24
    },
    {
      id: "2", 
      title: "Closure Session",
      lastMessage: "I think I'm finally ready to move forward...",
      timestamp: "Yesterday",
      mood: "healing",
      messageCount: 12
    }
  ];

  const moodColors: Record<string, string> = {
    nostalgic: "bg-primary/10 text-primary border-primary/30",
    healing: "bg-secondary/10 text-secondary border-secondary/30",
    reflective: "bg-accent/10 text-accent border-accent/30"
  };

  return (
    <div className="min-h-screen bg-gradient-warm">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/">
              <h1 className="text-2xl font-bold">helloEX</h1>
            </Link>
            <div className="flex items-center gap-2">
              <Link to="/settings">
                <Button variant="ghost" size="icon">
                  <Settings className="h-5 w-5" />
                </Button>
              </Link>
              <Button variant="ghost" size="icon">
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-12 animate-fade-in">
          <h2 className="text-4xl font-bold mb-2">Welcome back</h2>
          <p className="text-muted-foreground text-lg">Continue your journey toward emotional clarity</p>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <Card className="p-8 hover-lift hover-glow transition-all duration-300 cursor-pointer group border-2 border-dashed border-primary/30 hover:border-primary/50 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-hero opacity-0 group-hover:opacity-5 transition-opacity" />
            <div className="relative flex items-center gap-4">
              <div className="p-4 rounded-xl bg-gradient-hero group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <Plus className="h-8 w-8 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-1 group-hover:text-primary transition-colors">Start New Session</h3>
                <p className="text-sm text-muted-foreground">Begin a new conversation or closure session</p>
              </div>
            </div>
          </Card>

          <Link to="/memory/new">
            <Card className="p-8 hover-lift hover-glow transition-all duration-300 cursor-pointer group border-2 border-dashed border-secondary/30 hover:border-secondary/50 relative overflow-hidden">
              <div className="absolute inset-0 bg-secondary opacity-0 group-hover:opacity-5 transition-opacity" />
              <div className="relative flex items-center gap-4">
                <div className="p-4 rounded-xl bg-secondary group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                  <Heart className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-1 group-hover:text-secondary transition-colors">Create Memory</h3>
                  <p className="text-sm text-muted-foreground">Upload conversations, photos, or voice notes</p>
                </div>
              </div>
            </Card>
          </Link>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          {[
            { label: "Active Sessions", value: "2", icon: MessageCircle, change: "+1" },
            { label: "Total Conversations", value: "36", icon: MessageCircle, change: "+12" },
            { label: "Hours Reflected", value: "8.5", icon: Clock, change: "+2.5" },
            { label: "Emotional Insights", value: "12", icon: Heart, change: "+3" }
          ].map((stat, index) => (
            <Card key={index} className="p-6 text-center hover-lift hover:shadow-soft transition-all group cursor-default animate-scale-in" style={{ animationDelay: `${index * 0.05}s` }}>
              <div className="relative">
                <stat.icon className="h-6 w-6 mx-auto mb-2 text-primary group-hover:scale-110 transition-transform" />
                <div className="absolute -top-1 -right-1 text-xs font-semibold text-green-600 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                  <TrendingUp className="h-3 w-3" />
                  {stat.change}
                </div>
              </div>
              <div className="text-3xl font-bold mb-1 group-hover:text-gradient transition-all">{stat.value}</div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </Card>
          ))}
        </div>

        {/* Recent Sessions */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold">Your Sessions</h3>
            <Button variant="outline">View All</Button>
          </div>

          <div className="grid gap-4">
            {sessions.map((session, index) => (
              <Link key={session.id} to={`/chat/${session.id}`}>
                <Card className="p-6 hover-lift hover:shadow-soft transition-all duration-300 cursor-pointer group animate-scale-in relative overflow-hidden" style={{ animationDelay: `${index * 0.1}s` }}>
                  <div className="absolute inset-0 bg-gradient-hero opacity-0 group-hover:opacity-5 transition-opacity" />
                  <div className="relative flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h4 className="text-lg font-semibold group-hover:text-primary transition-colors">{session.title}</h4>
                        <span className={`text-xs px-3 py-1 rounded-full border ${moodColors[session.mood]} transition-all group-hover:scale-105`}>
                          {session.mood}
                        </span>
                      </div>
                      <p className="text-muted-foreground mb-3 line-clamp-1 group-hover:text-foreground/80 transition-colors">{session.lastMessage}</p>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1 group-hover:text-primary transition-colors">
                          <MessageCircle className="h-4 w-4" />
                          {session.messageCount} messages
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          {session.timestamp}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-primary animate-pulse-soft opacity-0 group-hover:opacity-100 transition-opacity" />
                      <Button variant="ghost" size="icon" className="opacity-0 group-hover:opacity-100 transition-opacity">
                        <MessageCircle className="h-5 w-5" />
                      </Button>
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </div>

        {/* Empty State (if no sessions) */}
        {sessions.length === 0 && (
          <Card className="p-12 text-center border-2 border-dashed">
            <MessageCircle className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <h3 className="text-xl font-semibold mb-2">No sessions yet</h3>
            <p className="text-muted-foreground mb-6">Start your first conversation to begin your healing journey</p>
            <Button variant="hero">Create Your First Session</Button>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
