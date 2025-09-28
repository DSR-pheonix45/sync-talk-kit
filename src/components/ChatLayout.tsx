import { useState } from 'react';
import { ChatSidebar } from './ChatSidebar';
import { ChatHeader } from './ChatHeader';
import { ChatWelcome } from './ChatWelcome';
import { ChatInput } from './ChatInput';
import { WorkbenchModal } from './WorkbenchModal';
import { CompanyModal } from './CompanyModal';
import { ReportModal } from './ReportModal';

export function ChatLayout() {
  const [showWorkbenchModal, setShowWorkbenchModal] = useState(false);
  const [showCompanyModal, setShowCompanyModal] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);

  // Mock data - replace with real data from Supabase
  const companies = [
    { company_id: '1', company_name: 'Tech Solutions Ltd.' },
    { company_id: '2', company_name: 'Global Industries Inc.' }
  ];

  const workbenches = [
    { id: '1', name: 'Q4 Financial Analysis', company_id: '1' },
    { id: '2', name: 'Audit Preparation', company_id: '2' }
  ];

  const userCredits = 50; // Mock credit balance

  return (
    <>
      <div className="flex h-screen bg-background">
        {/* Sidebar */}
        <ChatSidebar 
          onCreateWorkbench={() => setShowWorkbenchModal(true)}
          onCreateCompany={() => setShowCompanyModal(true)}
          onGenerateReport={() => setShowReportModal(true)}
        />
        
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

      {/* Modals */}
      <WorkbenchModal 
        open={showWorkbenchModal}
        onOpenChange={setShowWorkbenchModal}
        companies={companies}
      />
      
      <CompanyModal 
        open={showCompanyModal}
        onOpenChange={setShowCompanyModal}
      />
      
      <ReportModal 
        open={showReportModal}
        onOpenChange={setShowReportModal}
        companies={companies}
        workbenches={workbenches}
        userCredits={userCredits}
      />
    </>
  );
}