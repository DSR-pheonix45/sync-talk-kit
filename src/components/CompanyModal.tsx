import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Building2 } from 'lucide-react';

interface CompanyModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CompanyModal({ open, onOpenChange }: CompanyModalProps) {
  const [formData, setFormData] = useState({
    company_name: '',
    gst_no: '',
    pan_no: '',
    registered_address: '',
    ca_name: '',
    ca_id: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement company registration
    console.log('Registering company:', formData);
    onOpenChange(false);
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Building2 className="h-5 w-5" />
            Register New Company
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="md:col-span-2">
              <Label htmlFor="company-name">Company Name</Label>
              <Input
                id="company-name"
                value={formData.company_name}
                onChange={(e) => handleInputChange('company_name', e.target.value)}
                placeholder="Enter company name"
                required
              />
            </div>

            <div>
              <Label htmlFor="gst-no">GST Number</Label>
              <Input
                id="gst-no"
                value={formData.gst_no}
                onChange={(e) => handleInputChange('gst_no', e.target.value)}
                placeholder="22AAAAA0000A1Z5"
              />
            </div>

            <div>
              <Label htmlFor="pan-no">PAN Number</Label>
              <Input
                id="pan-no"
                value={formData.pan_no}
                onChange={(e) => handleInputChange('pan_no', e.target.value)}
                placeholder="AAAAA0000A"
              />
            </div>

            <div className="md:col-span-2">
              <Label htmlFor="address">Registered Address</Label>
              <Textarea
                id="address"
                value={formData.registered_address}
                onChange={(e) => handleInputChange('registered_address', e.target.value)}
                placeholder="Enter complete registered address"
                rows={3}
              />
            </div>

            <div>
              <Label htmlFor="ca-name">CA Name</Label>
              <Input
                id="ca-name"
                value={formData.ca_name}
                onChange={(e) => handleInputChange('ca_name', e.target.value)}
                placeholder="Chartered Accountant name"
              />
            </div>

            <div>
              <Label htmlFor="ca-id">CA ID</Label>
              <Input
                id="ca-id"
                value={formData.ca_id}
                onChange={(e) => handleInputChange('ca_id', e.target.value)}
                placeholder="CA membership number"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={!formData.company_name.trim()}>
              Register Company
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}