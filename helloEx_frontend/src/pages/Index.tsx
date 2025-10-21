import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Heart, MessageCircle, Shield, Sparkles, Clock, Lock, Menu, X } from "lucide-react";
import { useState } from "react";

const Index = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen">
      {/* Floating Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass-effect animate-slide-up">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2 group">
              <div className="p-2 rounded-lg bg-gradient-hero group-hover:scale-110 transition-transform">
                <Heart className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold">helloEX</span>
            </Link>
            
            <div className="hidden md:flex items-center gap-6">
              <a href="#how-it-works" className="text-sm font-medium hover:text-primary transition-colors">How It Works</a>
              <a href="#features" className="text-sm font-medium hover:text-primary transition-colors">Features</a>
              <a href="#safety" className="text-sm font-medium hover:text-primary transition-colors">Safety</a>
              <Link to="/dashboard">
                <Button variant="ghost" size="sm">Sign In</Button>
              </Link>
              <Link to="/dashboard">
                <Button variant="hero" size="sm">Get Started</Button>
              </Link>
            </div>

            <Button 
              variant="ghost" 
              size="icon" 
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-4 pb-4 animate-scale-in">
              <div className="flex flex-col gap-3">
                <a href="#how-it-works" className="text-sm font-medium hover:text-primary transition-colors py-2">How It Works</a>
                <a href="#features" className="text-sm font-medium hover:text-primary transition-colors py-2">Features</a>
                <a href="#safety" className="text-sm font-medium hover:text-primary transition-colors py-2">Safety</a>
                <Link to="/dashboard">
                  <Button variant="outline" size="sm" className="w-full">Sign In</Button>
                </Link>
                <Link to="/dashboard">
                  <Button variant="hero" size="sm" className="w-full">Get Started</Button>
                </Link>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-warm pt-24">
        <div className="absolute inset-0 bg-gradient-hero opacity-10" />
        <div className="container relative mx-auto px-4 py-20 md:py-32">
          <div className="mx-auto max-w-4xl text-center animate-fade-in">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-sm text-primary hover-lift cursor-default">
              <Sparkles className="h-4 w-4 animate-pulse-soft" />
              <span>A safe space for emotional closure</span>
            </div>
            
            <h1 className="mb-6 text-5xl md:text-7xl font-bold tracking-tight">
              Find <span className="bg-gradient-hero bg-clip-text text-transparent">Peace</span> Through Conversation
            </h1>
            
            <p className="mb-8 text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              helloEX helps you process emotions and find closure by creating a safe, AI-powered space to continue conversations that matter.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/dashboard">
                <Button variant="hero" size="lg" className="group">
                  Start Your Journey
                  <Heart className="ml-2 h-5 w-5 group-hover:scale-110 transition-transform" />
                </Button>
              </Link>
              <Button variant="warm" size="lg">
                Learn More
              </Button>
            </div>
          </div>
        </div>
        
        {/* Floating orbs decoration */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '3s' }} />
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-background scroll-mt-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16 animate-fade-in">
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Three simple steps to begin your healing journey
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                icon: MessageCircle,
                title: "Share Your Memories",
                description: "Upload past conversations, photos, or voice notes to help create a meaningful connection.",
                step: "01"
              },
              {
                icon: Sparkles,
                title: "Personalized Experience",
                description: "Our AI creates a safe, empathetic space tailored to your emotional needs and communication style.",
                step: "02"
              },
              {
                icon: Heart,
                title: "Find Your Closure",
                description: "Engage in guided conversations designed to help you process emotions and move forward.",
                step: "03"
              }
            ].map((item, index) => (
              <Card key={index} className="p-8 hover-lift hover-glow transition-all duration-300 animate-scale-in border-2 relative overflow-hidden group cursor-default" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="absolute top-0 right-0 text-8xl font-bold text-muted/5 group-hover:text-muted/10 transition-colors duration-500">
                  {item.step}
                </div>
                <div className="relative">
                  <div className="mb-4 inline-flex p-3 rounded-xl bg-gradient-hero group-hover:scale-110 transition-transform duration-300">
                    <item.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold mb-3 group-hover:text-primary transition-colors">{item.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{item.description}</p>
                </div>
                <div className="absolute inset-0 bg-gradient-hero opacity-0 group-hover:opacity-5 transition-opacity duration-300" />
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-muted/30 scroll-mt-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Built with Care & Privacy</h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Your emotional wellbeing and data security are our top priorities
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {[
              {
                icon: Shield,
                title: "Complete Privacy",
                description: "End-to-end encryption ensures your conversations remain private and secure."
              },
              {
                icon: Lock,
                title: "Your Data, Your Control",
                description: "Export or delete your data anytime. Full transparency in how we use information."
              },
              {
                icon: Clock,
                title: "Take Your Time",
                description: "No pressure, no judgment. Process emotions at your own pace in a safe environment."
              },
              {
                icon: Heart,
                title: "Emotionally Intelligent",
                description: "AI trained to recognize and respond with empathy, not just accuracy."
              },
              {
                icon: Sparkles,
                title: "Guided Support",
                description: "Structured closure sessions with therapeutic prompts when you're ready."
              },
              {
                icon: MessageCircle,
                title: "Multiple Modes",
                description: "Choose from different conversation styles: nostalgia, closure, or reflection."
              }
            ].map((feature, index) => (
              <Card key={index} className="p-6 hover-lift hover:shadow-soft transition-all duration-300 group cursor-default" style={{ animationDelay: `${index * 0.05}s` }}>
                <div className="mb-4 inline-flex p-2 rounded-lg bg-primary/10 group-hover:bg-gradient-hero transition-all duration-300 group-hover:scale-110">
                  <feature.icon className="h-5 w-5 text-primary group-hover:text-white transition-colors" />
                </div>
                <h3 className="font-semibold mb-2 group-hover:text-primary transition-colors">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Safety Callout */}
      <section id="safety" className="py-20 bg-secondary/5 scroll-mt-20">
        <div className="container mx-auto px-4">
          <Card className="max-w-4xl mx-auto p-10 md:p-16 text-center border-2 border-secondary/20 shadow-glow hover-lift transition-all duration-500">
            <div className="inline-flex p-4 rounded-full bg-secondary/10 mb-6 animate-pulse-soft">
              <Shield className="h-12 w-12 text-secondary" />
            </div>
            <h2 className="text-3xl font-bold mb-4">Your Emotional Safety Matters</h2>
            <p className="text-muted-foreground text-lg mb-8 leading-relaxed max-w-2xl mx-auto">
              While helloEX can provide support and a space for processing, it's not a replacement for professional therapy. 
              We encourage seeking help from licensed mental health professionals for serious concerns.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/dashboard">
                <Button variant="secondary" size="lg">
                  Get Started
                </Button>
              </Link>
              <Button variant="outline" size="lg">
                Crisis Resources
              </Button>
            </div>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t bg-background">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="text-center md:text-left">
              <div className="flex items-center gap-2 justify-center md:justify-start mb-2">
                <div className="p-1.5 rounded-lg bg-gradient-hero">
                  <Heart className="h-4 w-4 text-white" />
                </div>
                <h3 className="text-xl font-bold">helloEX</h3>
              </div>
              <p className="text-sm text-muted-foreground">Find peace through conversation</p>
            </div>
            <div className="flex gap-6 text-sm text-muted-foreground">
              <a href="#" className="hover:text-primary transition-colors hover:underline">Privacy Policy</a>
              <a href="#" className="hover:text-primary transition-colors hover:underline">Terms of Service</a>
              <a href="#" className="hover:text-primary transition-colors hover:underline">Support</a>
            </div>
          </div>
          <div className="text-center mt-8 text-xs text-muted-foreground">
            <p>© 2024 helloEX. Not a replacement for professional therapy.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
