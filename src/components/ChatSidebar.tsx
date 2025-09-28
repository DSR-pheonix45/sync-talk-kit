import { useState } from 'react';
import { 
  MessageSquarePlus, 
  Building2, 
  Settings, 
  History, 
  ChevronDown,
  User,
  CreditCard,
  HelpCircle,
  Sparkles,
  Briefcase,
  Plus,
  FileText,
  Folder
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';

interface ChatSidebarProps {
  className?: string;
  onCreateWorkbench?: () => void;
  onCreateCompany?: () => void;
  onGenerateReport?: () => void;
}

export function ChatSidebar({ className, onCreateWorkbench, onCreateCompany, onGenerateReport }: ChatSidebarProps) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    workbench: true,
    history: false,
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const navigationItems = [
    {
      icon: Building2,
      label: 'Company Info',
      href: '/company',
      badge: null,
    },
    {
      icon: Settings,
      label: 'Workbench',
      href: '/workbench',
      badge: '3',
      expandable: true,
      expanded: expandedSections.workbench,
      onToggle: () => toggleSection('workbench'),
      subItems: [
        { label: 'Financial Analysis', href: '/workbench/financial' },
        { label: 'Market Research', href: '/workbench/market' },
        { label: 'Compliance Check', href: '/workbench/compliance' },
      ]
    },
    {
      icon: History,
      label: 'History',
      href: '/history',
      expandable: true,
      expanded: expandedSections.history,
      onToggle: () => toggleSection('history'),
      subItems: [
        { label: 'Last 30 days', href: '/history/30days' },
        { label: 'Previous conversations', href: '/history/all' },
      ]
    }
  ];

  return (
    <div className={cn("flex flex-col h-full w-64 chat-sidebar", className)}>
      {/* Logo */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
            <Briefcase className="h-5 w-5 text-primary-foreground" />
          </div>
          <h1 className="text-xl font-bold text-foreground">Dabby</h1>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="p-4 space-y-2">
        <Button 
          variant="default" 
          className="w-full justify-start gap-3 bg-primary hover:bg-primary-hover text-primary-foreground font-medium"
        >
          <MessageSquarePlus className="h-4 w-4" />
          New Chat
          <kbd className="ml-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
            ⌘N
          </kbd>
        </Button>
        
        <div className="grid grid-cols-2 gap-2">
          <Button 
            variant="outline" 
            size="sm"
            className="gap-2"
            onClick={onCreateWorkbench}
          >
            <Plus className="h-3 w-3" />
            Workbench
          </Button>
          <Button 
            variant="outline" 
            size="sm"
            className="gap-2"
            onClick={onCreateCompany}
          >
            <Building2 className="h-3 w-3" />
            Company
          </Button>
        </div>
        
        <Button 
          variant="secondary" 
          size="sm"
          className="w-full gap-2"
          onClick={onGenerateReport}
        >
          <FileText className="h-3 w-3" />
          Generate Report
        </Button>
      </div>

      {/* Navigation */}
      <ScrollArea className="flex-1 px-2">
        <nav className="py-4 space-y-1">
          {navigationItems.map((item) => (
            <div key={item.label}>
              <Button
                variant="ghost"
                className={cn(
                  "w-full justify-start gap-3 sidebar-nav-item h-10 px-3",
                  "text-foreground hover:text-foreground hover:bg-accent-hover"
                )}
                onClick={item.expandable ? item.onToggle : undefined}
              >
                <item.icon className="h-4 w-4" />
                <span className="flex-1 text-left">{item.label}</span>
                {item.badge && (
                  <span className="bg-primary text-primary-foreground text-xs px-1.5 py-0.5 rounded-full">
                    {item.badge}
                  </span>
                )}
                {item.expandable && (
                  <ChevronDown className={cn(
                    "h-4 w-4 transition-transform",
                    item.expanded && "rotate-180"
                  )} />
                )}
              </Button>
              
              {/* Sub-items */}
              {item.expandable && item.expanded && item.subItems && (
                <div className="ml-7 mt-1 space-y-1 animate-slide-up">
                  {item.subItems.map((subItem) => (
                    <Button
                      key={subItem.label}
                      variant="ghost"
                      className="w-full justify-start text-sm text-muted-foreground hover:text-foreground h-8 px-3"
                    >
                      {subItem.label}
                    </Button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
      </ScrollArea>

      {/* Credits Section */}
      <div className="p-4 border-t border-border">
        <div className="bg-surface-elevated rounded-lg p-3 space-y-3">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-success"></div>
            <span className="text-sm font-medium text-success">50 Credits</span>
            <HelpCircle className="h-3 w-3 text-muted-foreground ml-auto" />
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>10 prompts until deduction</span>
              <span>0/10</span>
            </div>
            <div className="w-full bg-muted rounded-full h-1.5">
              <div className="bg-primary h-1.5 rounded-full w-0 transition-all duration-300"></div>
            </div>
          </div>
          
          <Button 
            size="sm" 
            variant="outline" 
            className="w-full gap-2 border-border hover:border-border-hover"
          >
            <CreditCard className="h-3 w-3" />
            Upgrade Plan
          </Button>
        </div>
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
            <User className="h-4 w-4 text-primary-foreground" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-foreground truncate">medhanshk10@gmail.com</p>
            <p className="text-xs text-muted-foreground truncate">Professional Plan</p>
          </div>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}