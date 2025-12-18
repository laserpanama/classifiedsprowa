import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const ScheduleForm = ({ onSubmit, ads, initialData = null }) => {
  const [formData, setFormData] = useState({
    ad_id: '',
    republish_interval_hours: 24,
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        ad_id: initialData.ad_id || '',
        republish_interval_hours: initialData.republish_interval_hours || 24,
      });
    } else {
      setFormData({ ad_id: '', republish_interval_hours: 24 });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-md">
      <h3 className="text-lg font-medium">{initialData ? 'Edit Schedule' : 'Create a New Schedule'}</h3>

      <div className="space-y-2">
        <Label>Ad to Republish</Label>
        <Select
          onValueChange={(value) => handleSelectChange('ad_id', value)}
          value={formData.ad_id}
          required
          disabled={!!initialData} // Don't allow changing the ad on an existing schedule
        >
          <SelectTrigger><SelectValue placeholder="Select an ad..." /></SelectTrigger>
          <SelectContent>
            {ads.map(ad => <SelectItem key={ad.id} value={ad.id}>{ad.title} ({ad.id.slice(0,8)}...)</SelectItem>)}
          </SelectContent>
        </Select>
        {initialData && <p className="text-xs text-muted-foreground">The ad for a schedule cannot be changed.</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="republish_interval_hours">Republish Every (hours)</Label>
        <Input
          id="republish_interval_hours"
          name="republish_interval_hours"
          type="number"
          min="1"
          value={formData.republish_interval_hours}
          onChange={handleChange}
          required
        />
      </div>

      <Button type="submit">{initialData ? 'Update Schedule' : 'Create Schedule'}</Button>
    </form>
  );
};

export default ScheduleForm;
