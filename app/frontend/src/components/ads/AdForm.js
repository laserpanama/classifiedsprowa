import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import adService from '../../services/adService';

// In a real app, these would come from the backend or a config file
const provinces = ["Panamá", "Colón", "Chiriquí", "Bocas del Toro", "Coclé", "Darién", "Herrera", "Los Santos", "Veraguas"];
const categories = {
  "Contactos": ["Eróticos / Profesionales", "Relaciones Ocasionales", "Chico Busca Chica", "Chica Busca Chico"],
  "Servicios": ["Informática / Multimedia", "Belleza / Bienestar / Salud", "Terapias / Yoga / Masajes"]
  // Add other categories as needed
};

const AdForm = ({ onSubmit, accounts, initialData = null }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    province: '',
    category: '',
    subcategory: '',
    price: '',
    zone: '',
    account_id: ''
  });
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title || '',
        description: initialData.description || '',
        province: initialData.province || '',
        category: initialData.category || '',
        subcategory: initialData.subcategory || '',
        price: initialData.price || '',
        zone: initialData.zone || '',
        account_id: initialData.account_id || '',
      });
    } else {
      // Reset form for creation
      setFormData({
        title: '', description: '', province: '', category: '',
        subcategory: '', price: '', zone: '', account_id: ''
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
    if (name === 'category') {
      setFormData(prev => ({ ...prev, subcategory: '' }));
    }
  };

  const handleGenerateText = async () => {
    if (!formData.title) {
      alert("Please enter a title first to generate a description.");
      return;
    }
    setIsGenerating(true);
    try {
      const response = await adService.generateAdText(formData.title);
      setFormData(prev => ({ ...prev, description: response.data.generated_text }));
    } catch (error) {
      console.error("Error generating text:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 border rounded-md">
      <h3 className="text-lg font-medium">{initialData ? 'Edit Ad' : 'Create a New Ad'}</h3>

      <div className="space-y-2">
        <Label>Account</Label>
        <Select onValueChange={(value) => handleSelectChange('account_id', value)} value={formData.account_id} required>
          <SelectTrigger><SelectValue placeholder="Select account..." /></SelectTrigger>
          <SelectContent>
            {accounts.map(acc => <SelectItem key={acc.id} value={acc.id}>{acc.email}</SelectItem>)}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="title">Title</Label>
        <Input id="title" name="title" value={formData.title} onChange={handleChange} required />
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea id="description" name="description" value={formData.description} onChange={handleChange} rows={5} required />
        <Button type="button" variant="outline" size="sm" onClick={handleGenerateText} disabled={isGenerating}>
          {isGenerating ? 'Generating...' : 'Generate with AI'}
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Category</Label>
          <Select onValueChange={(value) => handleSelectChange('category', value)} value={formData.category} required>
            <SelectTrigger><SelectValue placeholder="Select category..." /></SelectTrigger>
            <SelectContent>
              {Object.keys(categories).map(cat => <SelectItem key={cat} value={cat}>{cat}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label>Subcategory</Label>
          <Select onValueChange={(value) => handleSelectChange('subcategory', value)} value={formData.subcategory} disabled={!formData.category} required>
            <SelectTrigger><SelectValue placeholder="Select subcategory..." /></SelectTrigger>
            <SelectContent>
              {formData.category && categories[formData.category] && categories[formData.category].map(sub => <SelectItem key={sub} value={sub}>{sub}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>Province</Label>
          <Select onValueChange={(value) => handleSelectChange('province', value)} value={formData.province} required>
            <SelectTrigger><SelectValue placeholder="Select province..." /></SelectTrigger>
            <SelectContent>
              {provinces.map(prov => <SelectItem key={prov} value={prov}>{prov}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label htmlFor="zone">Zone / Area</Label>
          <Input id="zone" name="zone" value={formData.zone} onChange={handleChange} />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="price">Price (optional)</Label>
        <Input id="price" name="price" type="number" value={formData.price} onChange={handleChange} />
      </div>

      <Button type="submit">{initialData ? 'Update Ad' : 'Create Ad'}</Button>
    </form>
  );
};

export default AdForm;
