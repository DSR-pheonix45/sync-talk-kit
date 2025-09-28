import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { FileText, Building2, Folder, Sparkles, CreditCard } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ReportModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  companies: Array<{ company_id: string; company_name: string; }>;
  workbenches: Array<{ id: string; name: string; company_id: string; }>;
  userCredits: number;
}

const reportTypes = [
  {
    id: 'financial_analysis',
    name: 'Financial Analysis Report',
    description: 'Comprehensive financial performance analysis with ratios and trends',
    cost: 10,
    category: 'Financial'
  },
  {
    id: 'audit_report',
    name: 'Audit Report',
    description: 'Detailed audit findings and compliance assessment',
    cost: 15,
    category: 'Audit'
  },
  {
    id: 'tax_summary',
    name: 'Tax Summary Report',
    description: 'Tax liability analysis and optimization recommendations',
    cost: 8,
    category: 'Tax'
  },
  {
    id: 'cash_flow',
    name: 'Cash Flow Analysis',
    description: 'Cash flow patterns and liquidity assessment',
    cost: 12,
    category: 'Financial'
  },
  {
    id: 'compliance_check',
    name: 'Compliance Report',
    description: 'Regulatory compliance status and gap analysis',
    cost: 10,
    category: 'Compliance'
  }
];

export function ReportModal({ open, onOpenChange, companies, workbenches, userCredits }: ReportModalProps) {
  const [selectedCompany, setSelectedCompany] = useState('');
  const [selectedWorkbench, setSelectedWorkbench] = useState('');
  const [selectedReportType, setSelectedReportType] = useState('');
  const [reportTitle, setReportTitle] = useState('');
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const filteredWorkbenches = workbenches.filter(wb => 
    !selectedCompany || wb.company_id === selectedCompany
  );

  const selectedReport = reportTypes.find(rt => rt.id === selectedReportType);
  const canGenerate = selectedCompany && selectedWorkbench && selectedReportType && reportTitle.trim();
  const hasEnoughCredits = selectedReport ? userCredits >= selectedReport.cost : false;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canGenerate || !hasEnoughCredits) return;

    setIsGenerating(true);
    try {
      // TODO: Implement report generation with credit deduction
      console.log('Generating report:', {
        company: selectedCompany,
        workbench: selectedWorkbench,
        reportType: selectedReportType,
        title: reportTitle,
        notes: additionalNotes,
        cost: selectedReport?.cost
      });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      onOpenChange(false);
    } catch (error) {
      console.error('Report generation failed:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Generate Financial Report
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="company">Company</Label>
              <Select value={selectedCompany} onValueChange={setSelectedCompany}>
                <SelectTrigger>
                  <SelectValue placeholder="Select company" />
                </SelectTrigger>
                <SelectContent>
                  {companies.map((company) => (
                    <SelectItem key={company.company_id} value={company.company_id}>
                      <div className="flex items-center gap-2">
                        <Building2 className="h-4 w-4" />
                        {company.company_name}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="workbench">Workbench</Label>
              <Select 
                value={selectedWorkbench} 
                onValueChange={setSelectedWorkbench}
                disabled={!selectedCompany}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select workbench" />
                </SelectTrigger>
                <SelectContent>
                  {filteredWorkbenches.map((workbench) => (
                    <SelectItem key={workbench.id} value={workbench.id}>
                      <div className="flex items-center gap-2">
                        <Folder className="h-4 w-4" />
                        {workbench.name}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div>
            <Label htmlFor="report-title">Report Title</Label>
            <Input
              id="report-title"
              value={reportTitle}
              onChange={(e) => setReportTitle(e.target.value)}
              placeholder="e.g., Q4 2024 Financial Analysis"
              required
            />
          </div>

          <div>
            <Label>Report Type</Label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
              {reportTypes.map((report) => (
                <Card
                  key={report.id}
                  className={cn(
                    "p-4 cursor-pointer transition-all duration-200 hover:border-primary/50",
                    selectedReportType === report.id 
                      ? "border-primary bg-primary/5" 
                      : "border-border"
                  )}
                  onClick={() => setSelectedReportType(report.id)}
                >
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium text-sm">{report.name}</h4>
                      <Badge variant="secondary" className="text-xs">
                        <CreditCard className="h-3 w-3 mr-1" />
                        {report.cost}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground">{report.description}</p>
                    <Badge variant="outline" className="text-xs">
                      {report.category}
                    </Badge>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          <div>
            <Label htmlFor="notes">Additional Notes (Optional)</Label>
            <Textarea
              id="notes"
              value={additionalNotes}
              onChange={(e) => setAdditionalNotes(e.target.value)}
              placeholder="Any specific requirements or focus areas..."
              rows={3}
            />
          </div>

          {selectedReport && (
            <div className="bg-surface-elevated rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary" />
                  <span className="font-medium">Report Generation Cost</span>
                </div>
                <div className="text-right">
                  <div className="font-bold text-lg">{selectedReport.cost} Credits</div>
                  <div className="text-sm text-muted-foreground">
                    Your balance: {userCredits} credits
                  </div>
                </div>
              </div>
              
              {!hasEnoughCredits && (
                <div className="text-sm text-destructive">
                  Insufficient credits. You need {selectedReport.cost - userCredits} more credits.
                </div>
              )}
            </div>
          )}

          <div className="flex justify-end gap-3">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button 
              type="submit" 
              disabled={!canGenerate || !hasEnoughCredits || isGenerating}
              className="gap-2"
            >
              {isGenerating ? (
                <>
                  <Sparkles className="h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <FileText className="h-4 w-4" />
                  Generate Report
                </>
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}