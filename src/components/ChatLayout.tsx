import { ChatSidebar } from './ChatSidebar';
import { ChatHeader } from './ChatHeader';
import { ChatWelcome } from './ChatWelcome';
import { ChatInput } from './ChatInput';

export function ChatLayout() {
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <ChatSidebar />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <ChatHeader />
        
        {/* Chat Area */}
        <div className="flex-1 chat-message-area overflow-hidden">
          <ChatWelcome />
        </div>
        
        {/* Input */}
        <ChatInput />
      </div>
    </div>
  );
}