import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Upload, X, FileText, Folder } from 'lucide-react';
import { cn } from '@/lib/utils';

interface WorkbenchModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  companies: Array<{ company_id: string; company_name: string; }>;
}

export function WorkbenchModal({ open, onOpenChange, companies }: WorkbenchModalProps) {
  const [workbenchName, setWorkbenchName] = useState('');
  const [description, setDescription] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileUpload = (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    setUploadedFiles(prev => [...prev, ...fileArray]);
  };

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    handleFileUpload(files);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement workbench creation with file uploads
    console.log('Creating workbench:', {
      name: workbenchName,
      description,
      company: selectedCompany,
      files: uploadedFiles
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Folder className="h-5 w-5" />
            Create New Workbench
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div>
              <Label htmlFor="workbench-name">Workbench Name</Label>
              <Input
                id="workbench-name"
                value={workbenchName}
                onChange={(e) => setWorkbenchName(e.target.value)}
                placeholder="e.g., Q4 Financial Analysis"
                required
              />
            </div>

            <div>
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief description of the workbench purpose..."
                rows={3}
              />
            </div>

            <div>
              <Label htmlFor="company">Assign to Company</Label>
              <Select value={selectedCompany} onValueChange={setSelectedCompany}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a company" />
                </SelectTrigger>
                <SelectContent>
                  {companies.map((company) => (
                    <SelectItem key={company.company_id} value={company.company_id}>
                      {company.company_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* File Upload Area */}
          <div className="space-y-4">
            <Label>Upload Files</Label>
            <div
              className={cn(
                "border-2 border-dashed rounded-lg p-6 text-center transition-colors",
                isDragOver ? "border-primary bg-primary/5" : "border-border",
                "hover:border-primary/50 hover:bg-primary/5"
              )}
              onDrop={handleDrop}
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragOver(true);
              }}
              onDragLeave={() => setIsDragOver(false)}
            >
              <Upload className="h-10 w-10 mx-auto mb-4 text-muted-foreground" />
              <p className="text-sm text-muted-foreground mb-2">
                Drag and drop files here, or click to browse
              </p>
              <Button 
                type="button" 
                variant="outline" 
                onClick={() => document.getElementById('file-input')?.click()}
              >
                Browse Files
              </Button>
              <input
                id="file-input"
                type="file"
                multiple
                className="hidden"
                onChange={(e) => e.target.files && handleFileUpload(e.target.files)}
                accept=".pdf,.xlsx,.xls,.csv,.txt,.docx"
              />
            </div>

            {/* Uploaded Files List */}
            {uploadedFiles.length > 0 && (
              <div className="space-y-2">
                <Label>Uploaded Files ({uploadedFiles.length})</Label>
                <div className="max-h-32 overflow-y-auto space-y-1">
                  {uploadedFiles.map((file, index) => (
                    <div key={index} className="flex items-center gap-2 p-2 bg-surface rounded border">
                      <FileText className="h-4 w-4 text-muted-foreground" />
                      <span className="flex-1 text-sm truncate">{file.name}</span>
                      <span className="text-xs text-muted-foreground">
                        {(file.size / 1024 / 1024).toFixed(1)} MB
                      </span>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="h-6 w-6 p-0"
                        onClick={() => removeFile(index)}
                      >
                        <X className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-end gap-3">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={!workbenchName.trim()}>
              Create Workbench
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}