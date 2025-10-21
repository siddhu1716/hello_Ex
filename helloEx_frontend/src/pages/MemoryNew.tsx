import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ArrowLeft, Upload, MessageSquare, Image, Mic, FileText } from "lucide-react";

const MemoryNew = () => {
  return (
    <div className="min-h-screen bg-gradient-warm">
      {/* Header */}
      <header className="border-b glass-effect sticky top-0 z-10 animate-slide-up">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <Link to="/dashboard">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <div>
              <h1 className="text-2xl font-bold">Create New Memory</h1>
              <p className="text-sm text-muted-foreground">Upload content to build your persona</p>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Instructions */}
        <Card className="p-6 mb-8 bg-primary/5 border-primary/20">
          <h3 className="font-semibold mb-2">Building Your Persona</h3>
          <p className="text-sm text-muted-foreground">
            Upload past conversations, photos, or voice notes to help create a more authentic and meaningful experience. 
            All data is encrypted and stored securely. You can review and manage uploaded content at any time.
          </p>
        </Card>

        {/* Upload Options */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card className="p-8 hover-lift hover-glow transition-all duration-300 cursor-pointer group border-2 border-dashed hover:border-primary/50 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-hero opacity-0 group-hover:opacity-5 transition-opacity" />
            <div className="relative text-center">
              <div className="p-4 rounded-xl bg-gradient-hero inline-flex mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <MessageSquare className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Chat History</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Upload WhatsApp, iMessage, or Telegram exports
              </p>
              <Button variant="outline" className="w-full">
                <Upload className="h-4 w-4 mr-2" />
                Select Files
              </Button>
            </div>
          </Card>

          <Card className="p-8 hover-lift hover-glow transition-all duration-300 cursor-pointer group border-2 border-dashed hover:border-secondary/50 relative overflow-hidden">
            <div className="absolute inset-0 bg-secondary opacity-0 group-hover:opacity-5 transition-opacity" />
            <div className="relative text-center">
              <div className="p-4 rounded-xl bg-secondary inline-flex mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <Image className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Photos</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Add meaningful photos and visual memories
              </p>
              <Button variant="outline" className="w-full">
                <Upload className="h-4 w-4 mr-2" />
                Upload Photos
              </Button>
            </div>
          </Card>

          <Card className="p-8 hover-lift hover-glow transition-all duration-300 cursor-pointer group border-2 border-dashed hover:border-accent/50 relative overflow-hidden">
            <div className="absolute inset-0 bg-accent opacity-0 group-hover:opacity-5 transition-opacity" />
            <div className="relative text-center">
              <div className="p-4 rounded-xl bg-accent inline-flex mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <Mic className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Voice Notes</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Upload voice recordings for tone analysis
              </p>
              <Button variant="outline" className="w-full">
                <Upload className="h-4 w-4 mr-2" />
                Add Audio
              </Button>
            </div>
          </Card>

          <Card className="p-8 hover-lift hover-glow transition-all duration-300 cursor-pointer group border-2 border-dashed hover:border-primary/50 relative overflow-hidden">
            <div className="absolute inset-0 bg-primary opacity-0 group-hover:opacity-5 transition-opacity" />
            <div className="relative text-center">
              <div className="p-4 rounded-xl bg-primary inline-flex mb-4 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">
                <FileText className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Text Samples</h3>
              <p className="text-sm text-muted-foreground mb-4">
                Paste or type memorable conversations
              </p>
              <Button variant="outline" className="w-full">
                <Upload className="h-4 w-4 mr-2" />
                Add Text
              </Button>
            </div>
          </Card>
        </div>

        {/* Uploaded Content Preview */}
        <Card className="p-8 border-2 border-dashed">
          <div className="text-center text-muted-foreground">
            <Upload className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p className="text-sm">No content uploaded yet</p>
            <p className="text-xs mt-1">Select an upload option above to get started</p>
          </div>
        </Card>

        {/* Action Buttons */}
        <div className="flex gap-4 mt-8">
          <Link to="/dashboard" className="flex-1">
            <Button variant="outline" className="w-full">Cancel</Button>
          </Link>
          <Button variant="hero" className="flex-1" disabled>
            Continue Setup
          </Button>
        </div>
      </div>
    </div>
  );
};

export default MemoryNew;
