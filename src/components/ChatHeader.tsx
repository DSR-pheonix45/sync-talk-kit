import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  MoreHorizontal, 
  Sparkles, 
  Download,
  Settings,
  ChevronDown
} from 'lucide-react';

interface ChatHeaderProps {
  onGenerateReport?: () => void;
}

export function ChatHeader({ onGenerateReport }: ChatHeaderProps = {}) {
  return (
    <header className="flex items-center justify-between p-4 border-b border-border bg-surface">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
            <Sparkles className="h-4 w-4 text-primary" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-foreground">Chat with Dabby Consultant</h1>
            <p className="text-xs text-muted-foreground">AI-powered business intelligence</p>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Consultant Selection */}
        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-elevated border border-border">
          <div className="w-2 h-2 rounded-full bg-success"></div>
          <span className="text-sm font-medium text-foreground">Dabby Consultant</span>
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        </div>

        {/* Generate Report Button */}
        <Button 
          variant="default" 
          className="gap-2 bg-primary hover:bg-primary-hover text-primary-foreground"
          onClick={onGenerateReport}
        >
          <Download className="h-4 w-4" />
          Generate Report
        </Button>

        {/* More Options */}
        <Button variant="ghost" size="sm" className="h-9 w-9 p-0">
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}