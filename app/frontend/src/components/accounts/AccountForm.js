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

const AccountForm = ({ onSubmit, initialData = null }) => {
  const [formData, setFormData] = useState({
    email: '',
    wanuncios_password: '',
    captcha_solving_method: 'api',
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        email: initialData.email || '',
        wanuncios_password: '', // Always clear password for security
        captcha_solving_method: initialData.captcha_solving_method || 'api',
      });
    } else {
      setFormData({ email: '', wanuncios_password: '', captcha_solving_method: 'api' });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (value) => {
    setFormData(prev => ({ ...prev, captcha_solving_method: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dataToSubmit = { ...formData };
    if (!dataToSubmit.wanuncios_password) {
      delete dataToSubmit.wanuncios_password;
    }
    onSubmit(dataToSubmit);
    if (!initialData) {
        setFormData({ email: '', wanuncios_password: '', captcha_solving_method: 'api' });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-md">
      <h3 className="text-lg font-medium">{initialData ? 'Edit Account' : 'Create a New Account'}</h3>

      <div className="space-y-2">
        <Label htmlFor="email">Account Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="user@example.com"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="wanuncios_password">wanuncios.com Password</Label>
        <Input
          id="wanuncios_password"
          name="wanuncios_password"
          type="password"
          value={formData.wanuncios_password}
          onChange={handleChange}
          placeholder="••••••••"
          required={!initialData}
        />
        {initialData && <p className="text-xs text-muted-foreground">Leave blank to keep the current password.</p>}
      </div>

      <div className="space-y-2">
        <Label>CAPTCHA Solving Method</Label>
        <Select onValueChange={handleSelectChange} value={formData.captcha_solving_method}>
          <SelectTrigger><SelectValue /></SelectTrigger>
          <SelectContent>
            <SelectItem value="api">API (2captcha)</SelectItem>
            <SelectItem value="manual">Manual</SelectItem>
            <SelectItem value="script" disabled>Script (Not Implemented)</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Button type="submit">{initialData ? 'Update Account' : 'Create Account'}</Button>
    </form>
  );
};

export default AccountForm;
