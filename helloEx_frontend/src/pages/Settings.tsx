import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ArrowLeft, User, Shield, Bell, Trash2, Download, HelpCircle } from "lucide-react";

const Settings = () => {
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
            <h1 className="text-2xl font-bold">Settings & Privacy</h1>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="space-y-6">
          {/* Account Section */}
          <Card className="p-6 hover-lift transition-all animate-scale-in">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-primary/10">
                <User className="h-5 w-5 text-primary" />
              </div>
              <h2 className="text-xl font-semibold">Account</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b">
                <div>
                  <p className="font-medium">Email</p>
                  <p className="text-sm text-muted-foreground">user@example.com</p>
                </div>
                <Button variant="outline" size="sm">Change</Button>
              </div>
              <div className="flex items-center justify-between py-3 border-b">
                <div>
                  <p className="font-medium">Password</p>
                  <p className="text-sm text-muted-foreground">••••••••</p>
                </div>
                <Button variant="outline" size="sm">Update</Button>
              </div>
            </div>
          </Card>

          {/* Privacy Section */}
          <Card className="p-6 hover-lift transition-all animate-scale-in" style={{ animationDelay: '0.1s' }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-primary/10">
                <Shield className="h-5 w-5 text-primary" />
              </div>
              <h2 className="text-xl font-semibold">Privacy & Data</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3">
                <div>
                  <p className="font-medium">Data Encryption</p>
                  <p className="text-sm text-muted-foreground">End-to-end encryption enabled</p>
                </div>
                <div className="px-3 py-1 bg-primary/10 text-primary text-xs rounded-full">Active</div>
              </div>
              <div className="flex items-center justify-between py-3 border-t">
                <div>
                  <p className="font-medium">Voice Cloning Consent</p>
                  <p className="text-sm text-muted-foreground">Allow AI to use voice samples</p>
                </div>
                <Button variant="outline" size="sm">Manage</Button>
              </div>
            </div>
          </Card>

          {/* Notifications Section */}
          <Card className="p-6 hover-lift transition-all animate-scale-in" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-primary/10">
                <Bell className="h-5 w-5 text-primary" />
              </div>
              <h2 className="text-xl font-semibold">Notifications</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b">
                <div>
                  <p className="font-medium">Email Notifications</p>
                  <p className="text-sm text-muted-foreground">Session summaries and updates</p>
                </div>
                <Button variant="outline" size="sm">Configure</Button>
              </div>
            </div>
          </Card>

          {/* Data Management Section */}
          <Card className="p-6 hover-lift transition-all animate-scale-in" style={{ animationDelay: '0.3s' }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-secondary/10">
                <Download className="h-5 w-5 text-secondary" />
              </div>
              <h2 className="text-xl font-semibold">Data Management</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between py-3 border-b">
                <div>
                  <p className="font-medium">Export Your Data</p>
                  <p className="text-sm text-muted-foreground">Download all conversations and memories</p>
                </div>
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </div>
              <div className="flex items-center justify-between py-3">
                <div>
                  <p className="font-medium text-destructive">Delete Account</p>
                  <p className="text-sm text-muted-foreground">Permanently remove all your data</p>
                </div>
                <Button variant="destructive" size="sm">
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete
                </Button>
              </div>
            </div>
          </Card>

          {/* Support Section */}
          <Card className="p-6 hover-lift transition-all animate-scale-in" style={{ animationDelay: '0.4s' }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-primary/10">
                <HelpCircle className="h-5 w-5 text-primary" />
              </div>
              <h2 className="text-xl font-semibold">Help & Support</h2>
            </div>
            <div className="space-y-3">
              <Button variant="ghost" className="w-full justify-start">
                Documentation & FAQs
              </Button>
              <Button variant="ghost" className="w-full justify-start">
                Crisis Resources
              </Button>
              <Button variant="ghost" className="w-full justify-start">
                Contact Support
              </Button>
              <Button variant="ghost" className="w-full justify-start">
                Terms of Service
              </Button>
              <Button variant="ghost" className="w-full justify-start">
                Privacy Policy
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Settings;
