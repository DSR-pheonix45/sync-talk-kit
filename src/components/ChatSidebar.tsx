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
  Briefcase,
  Plus,
  Folder
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";

interface ChatSidebarProps {
  onCreateWorkbench?: () => void;
  onCreateCompany?: () => void;
}

export function ChatSidebar({ onCreateWorkbench, onCreateCompany }: ChatSidebarProps) {
  const { state } = useSidebar();
  const isCollapsed = state === "collapsed";
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    companyInfo: true,
    workbench: true,
    history: false,
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const companyInfoItems = [
    { label: 'Tech Solutions Ltd.', href: '/company/tech-solutions' },
    { label: 'Global Industries Inc.', href: '/company/global-industries' },
  ];

  const workbenchItems = [
    { label: 'Financial Analysis.xlsx', href: '/workbench/financial' },
    { label: 'Market Research.pdf', href: '/workbench/market' },
    { label: 'Compliance Folder/', href: '/workbench/compliance' },
  ];

  const historyItems = [
    { label: 'Last 30 days', href: '/history/30days' },
    { label: 'Previous conversations', href: '/history/all' },
  ];
  return (
    <Sidebar collapsible="icon">
      <SidebarTrigger className="m-2 self-end" />

      <SidebarContent>
        {/* Logo */}
        <div className={cn("border-b border-border", isCollapsed ? "p-2" : "p-4")}>
          <div className="flex items-center gap-3">
            <div className="sidebar-icon-container w-8 h-8 rounded-lg bg-primary flex items-center justify-center flex-shrink-0">
              <Briefcase className="h-4 w-4 text-primary-foreground" />
            </div>
            {!isCollapsed && <h1 className="text-xl font-bold text-foreground">Dabby</h1>}
          </div>
        </div>

        {/* Action Buttons */}
        <div className={cn("space-y-2", isCollapsed ? "p-2" : "p-4")}>
          <Button 
            variant="default" 
            className={cn(
              "w-full bg-primary hover:bg-primary/90 text-primary-foreground font-medium",
              isCollapsed ? "justify-center px-2" : "justify-start gap-3"
            )}
          >
            <MessageSquarePlus className="h-4 w-4 flex-shrink-0" />
            {!isCollapsed && (
              <>
                New Chat
                <kbd className="ml-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                  ⌘N
                </kbd>
              </>
            )}
          </Button>
          
          {!isCollapsed && (
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
          )}
        </div>

        {/* Navigation Groups */}
        <ScrollArea className="flex-1">
          <div className="px-2 py-4 space-y-4">
            {/* Company Info Group */}
            <SidebarGroup>
              <SidebarGroupLabel 
                className="cursor-pointer flex items-center justify-between px-2 py-1 hover:bg-accent rounded-md"
                onClick={() => toggleSection('companyInfo')}
              >
                <div className="flex items-center gap-2">
                  <Building2 className="h-4 w-4" />
                  {!isCollapsed && <span>Company Info</span>}
                </div>
                {!isCollapsed && (
                  <ChevronDown className={cn(
                    "h-4 w-4 transition-transform",
                    expandedSections.companyInfo && "rotate-180"
                  )} />
                )}
              </SidebarGroupLabel>
              
              {!isCollapsed && expandedSections.companyInfo && (
                <SidebarGroupContent>
                  <SidebarMenu>
                    {companyInfoItems.map((item) => (
                      <SidebarMenuItem key={item.label}>
                        <SidebarMenuButton asChild>
                          <a href={item.href} className="text-sm text-muted-foreground hover:text-foreground">
                            {item.label}
                          </a>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    ))}
                  </SidebarMenu>
                </SidebarGroupContent>
              )}
            </SidebarGroup>

            {/* Workbench Group */}
            <SidebarGroup>
              <SidebarGroupLabel 
                className="cursor-pointer flex items-center justify-between px-2 py-1 hover:bg-accent rounded-md"
                onClick={() => toggleSection('workbench')}
              >
                <div className="flex items-center gap-2">
                  <Settings className="h-4 w-4" />
                  {!isCollapsed && <span>Workbench</span>}
                </div>
                {!isCollapsed && (
                  <>
                    <div className="flex items-center gap-2">
                      <span className="bg-primary text-primary-foreground text-xs px-1.5 py-0.5 rounded-full">3</span>
                      <ChevronDown className={cn(
                        "h-4 w-4 transition-transform",
                        expandedSections.workbench && "rotate-180"
                      )} />
                    </div>
                  </>
                )}
              </SidebarGroupLabel>
              
              {!isCollapsed && expandedSections.workbench && (
                <SidebarGroupContent>
                  <SidebarMenu>
                    {workbenchItems.map((item) => (
                      <SidebarMenuItem key={item.label}>
                        <SidebarMenuButton asChild>
                          <a href={item.href} className="text-sm text-muted-foreground hover:text-foreground flex items-center gap-2">
                            <Folder className="h-3 w-3" />
                            {item.label}
                          </a>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    ))}
                  </SidebarMenu>
                </SidebarGroupContent>
              )}
            </SidebarGroup>

            {/* History Group */}
            <SidebarGroup>
              <SidebarGroupLabel 
                className="cursor-pointer flex items-center justify-between px-2 py-1 hover:bg-accent rounded-md"
                onClick={() => toggleSection('history')}
              >
                <div className="flex items-center gap-2">
                  <History className="h-4 w-4" />
                  {!isCollapsed && <span>History</span>}
                </div>
                {!isCollapsed && (
                  <ChevronDown className={cn(
                    "h-4 w-4 transition-transform",
                    expandedSections.history && "rotate-180"
                  )} />
                )}
              </SidebarGroupLabel>
              
              {!isCollapsed && expandedSections.history && (
                <SidebarGroupContent>
                  <SidebarMenu>
                    {historyItems.map((item) => (
                      <SidebarMenuItem key={item.label}>
                        <SidebarMenuButton asChild>
                          <a href={item.href} className="text-sm text-muted-foreground hover:text-foreground">
                            {item.label}
                          </a>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    ))}
                  </SidebarMenu>
                </SidebarGroupContent>
              )}
            </SidebarGroup>
          </div>
        </ScrollArea>

        {/* Credits Section */}
        {!isCollapsed && (
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
                className="w-full gap-2 border-border hover:border-border/80"
              >
                <CreditCard className="h-3 w-3" />
                Upgrade Plan
              </Button>
            </div>
          </div>
        )}

        {/* User Profile */}
        <div className={cn("border-t border-border", isCollapsed ? "p-2" : "p-4")}>
          <div className="flex items-center gap-3">
            <div className="sidebar-icon-container w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
              <User className="h-4 w-4 text-primary-foreground" />
            </div>
            {!isCollapsed && (
              <>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">medhanshk10@gmail.com</p>
                  <p className="text-xs text-muted-foreground truncate">Professional Plan</p>
                </div>
                <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                  <Settings className="h-4 w-4" />
                </Button>
              </>
            )}
          </div>
        </div>
      </SidebarContent>
    </Sidebar>
  );
}