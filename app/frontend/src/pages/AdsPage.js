import React, { useState, useEffect, useCallback } from 'react';
import adService from '../services/adService';
import accountService from '../services/accountService';
import AdList from '../components/ads/AdList';
import AdForm from '../components/ads/AdForm';
import { Button } from '../components/ui/button';

const AdsPage = () => {
  const [ads, setAds] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [editingAd, setEditingAd] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const fetchAds = useCallback(async () => {
    try {
      const response = await adService.getAds();
      setAds(response.data);
    } catch (error) {
      console.error('Error fetching ads:', error);
    }
  }, []);

  const fetchAccounts = useCallback(async () => {
    try {
      const response = await accountService.getAccounts();
      setAccounts(response.data.filter(acc => acc.is_active)); // Only use active accounts
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  }, []);

  useEffect(() => {
    fetchAds();
    fetchAccounts();
  }, [fetchAds, fetchAccounts]);

  const handleFormSubmit = async (formData) => {
    try {
      if (editingAd) {
        await adService.updateAd(editingAd.id, formData);
      } else {
        await adService.createAd(formData);
      }
      await fetchAds();
      setEditingAd(null);
      setShowForm(false);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  const handleEdit = (ad) => {
    setEditingAd(ad);
    setShowForm(true);
  };

  const handleAddNew = () => {
    if (accounts.length === 0) {
      alert("Please add at least one active account before creating an ad.");
      return;
    }
    setEditingAd(null);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this ad?')) {
      try {
        await adService.deleteAd(id);
        await fetchAds();
      } catch (error) {
        console.error('Error deleting ad:', error);
      }
    }
  };

  const handlePublish = async (id) => {
    // This is a placeholder for now
    alert(`Publishing ad ${id}... (this will be implemented later)`);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">Ads Management</h2>
        <Button onClick={handleAddNew}>Add New Ad</Button>
      </div>

      {showForm && (
        <AdForm
          onSubmit={handleFormSubmit}
          accounts={accounts}
          initialData={editingAd}
        />
      )}

      <div className="mt-6">
        <AdList ads={ads} onEdit={handleEdit} onDelete={handleDelete} onPublish={handlePublish} />
      </div>
    </div>
  );
};

export default AdsPage;
