import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { 
  Send, 
  Paperclip,
  Sparkles,
  Plus
} from 'lucide-react';
import { cn } from '@/lib/utils';

export function ChatInput() {
  const [message, setMessage] = useState('');

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
    <div className="bg-surface">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative">
          {/* Input Container */}
          <div className="relative bg-surface-elevated border border-input-border rounded-lg p-2 focus-within:border-ring focus-within:ring-1 focus-within:ring-ring/20 transition-all duration-200">
            {/* Text Input */}
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <Textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Message Dabby Consultant... (Ctrl + K)"
                  className="min-h-[40px] resize-none border-0 bg-transparent p-2 focus-visible:ring-0 text-foreground placeholder:text-muted-foreground text-sm"
                  rows={1}
                />
              </div>
              
              {/* Action Buttons */}
              <div className="flex items-center gap-1">
                <Button 
                  type="button"
                  variant="ghost" 
                  size="sm" 
                  className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground"
                >
                  <Paperclip className="h-4 w-4" />
                </Button>
                
                {/* Send Button */}
                <Button 
                  type="submit"
                  disabled={!message.trim()}
                  size="sm"
                  className={cn(
                    "h-8 w-8 p-0 rounded-md transition-all duration-200",
                    message.trim() 
                      ? "bg-primary hover:bg-primary/90 text-primary-foreground" 
                      : "bg-muted text-muted-foreground"
                  )}
                >
                  <Send className="h-3 w-3" />
                </Button>
              </div>
            </div>
          </div>

          {/* Keyboard Shortcut Hint */}
          <div className="flex justify-between items-center mt-1 px-2">
            <div className="text-xs text-muted-foreground">
              Press Ctrl + Enter to send • Shift + Enter for new line
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}