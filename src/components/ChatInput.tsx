import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { 
  Send, 
  Paperclip, 
  Mic,
  Sparkles,
  Plus
} from 'lucide-react';
import { cn } from '@/lib/utils';

export function ChatInput() {
  const [message, setMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      // Handle message submission
      console.log('Sending message:', message);
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleSubmit(e);
    }
  };

  return (
    <div className="border-t border-border bg-surface p-4">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative">
          {/* Input Container */}
          <div className="relative bg-surface-elevated border border-input-border rounded-xl p-3 focus-within:border-ring focus-within:ring-2 focus-within:ring-ring/20 transition-all duration-200">
            {/* Action Buttons Row */}
            <div className="flex items-center gap-2 mb-3 pb-3 border-b border-border">
              <Button 
                type="button"
                variant="ghost" 
                size="sm" 
                className="gap-2 text-muted-foreground hover:text-foreground"
              >
                <Plus className="h-4 w-4" />
                Add
              </Button>
              
              <Button 
                type="button"
                variant="ghost" 
                size="sm" 
                className="gap-2 text-muted-foreground hover:text-foreground"
              >
                <Paperclip className="h-4 w-4" />
                Attach
              </Button>

              <div className="flex-1" />

              <Button 
                type="button"
                variant="ghost" 
                size="sm" 
                className={cn(
                  "gap-2 transition-colors",
                  isRecording 
                    ? "text-destructive hover:text-destructive" 
                    : "text-muted-foreground hover:text-foreground"
                )}
                onClick={() => setIsRecording(!isRecording)}
              >
                <Mic className={cn("h-4 w-4", isRecording && "animate-pulse")} />
                {isRecording ? 'Recording...' : 'Voice'}
              </Button>
            </div>

            {/* Text Input */}
            <div className="flex items-end gap-3">
              <div className="flex-1">
                <Textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Message Datalis (Consultant)... (Ctrl + K)"
                  className="min-h-[80px] resize-none border-0 bg-transparent p-0 focus-visible:ring-0 text-foreground placeholder:text-muted-foreground"
                  rows={3}
                />
              </div>
              
              {/* Send Button */}
              <Button 
                type="submit"
                disabled={!message.trim()}
                className={cn(
                  "h-10 w-10 p-0 rounded-lg transition-all duration-200",
                  message.trim() 
                    ? "bg-primary hover:bg-primary-hover text-primary-foreground glow-primary" 
                    : "bg-muted text-muted-foreground"
                )}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>

            {/* AI Indicator */}
            {message.trim() && (
              <div className="flex items-center gap-2 mt-3 pt-3 border-t border-border animate-slide-up">
                <Sparkles className="h-3 w-3 text-primary" />
                <span className="text-xs text-muted-foreground">
                  AI will analyze your query and provide specialized business insights
                </span>
              </div>
            )}
          </div>

          {/* Keyboard Shortcut Hint */}
          <div className="flex justify-between items-center mt-2 px-1">
            <div className="flex items-center gap-4 text-xs text-muted-foreground">
              <span>
                <kbd className="inline-flex items-center gap-1 rounded border bg-muted px-1.5 py-0.5 font-mono">
                  Ctrl
                </kbd>
                {' + '}
                <kbd className="inline-flex items-center gap-1 rounded border bg-muted px-1.5 py-0.5 font-mono">
                  Enter
                </kbd>
                {' to send'}
              </span>
            </div>
            
            <div className="text-xs text-muted-foreground">
              {message.length}/2000 characters
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}