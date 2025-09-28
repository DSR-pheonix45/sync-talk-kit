import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { 
  TrendingUp, 
  Target, 
  Calculator,
  BarChart3,
  PieChart,
  FileText,
  Lightbulb,
  Zap
} from 'lucide-react';

export function ChatWelcome() {
  const suggestions = [
    {
      icon: TrendingUp,
      text: 'What are our top revenue streams?',
      category: 'Revenue Analysis'
    },
    {
      icon: Target,
      text: 'Analyze our market position',
      category: 'Market Research'
    },
    {
      icon: Calculator,
      text: 'Create a financial forecast',
      category: 'Financial Planning'
    },
    {
      icon: BarChart3,
      text: 'Compare quarterly performance',
      category: 'Performance Analytics'
    },
    {
      icon: PieChart,
      text: 'Break down our customer segments',
      category: 'Customer Analysis'
    },
    {
      icon: FileText,
      text: 'Generate compliance report',
      category: 'Compliance'
    }
  ];

  const quickActions = [
    { icon: Lightbulb, label: 'Strategic Insights', count: '12 new' },
    { icon: Zap, label: 'Quick Analysis', count: 'Ready' },
    { icon: FileText, label: 'Report Builder', count: '3 templates' }
  ];

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full space-y-8 animate-fade-in">
        {/* Welcome Header */}
        <div className="text-center space-y-4">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-primary to-primary-hover flex items-center justify-center glow-primary">
            <BarChart3 className="h-8 w-8 text-primary-foreground" />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2">Welcome to Datalis</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Select an AI agent above to get started with specialized assistance for consulting, auditing, or taxation.
            </p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {quickActions.map((action, index) => (
            <Card key={action.label} className="p-4 bg-surface border-border hover:border-border-hover transition-all duration-200 cursor-pointer group">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                  <action.icon className="h-5 w-5 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="font-medium text-foreground">{action.label}</h3>
                  <p className="text-sm text-muted-foreground">{action.count}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Suggestion Prompts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {suggestions.map((suggestion, index) => (
            <Card 
              key={index} 
              className="suggestion-card p-4 cursor-pointer group"
            >
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                  <suggestion.icon className="h-5 w-5 text-primary" />
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded-full">
                      {suggestion.category}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                    {suggestion.text}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Help Text */}
        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            💡 <strong>Pro tip:</strong> Use natural language to describe your business questions. 
            The AI will guide you through the analysis process.
          </p>
        </div>
      </div>
    </div>
  );
}