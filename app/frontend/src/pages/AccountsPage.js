import React, { useState, useEffect, useCallback } from 'react';
import accountService from '../services/accountService';
import AccountList from '../components/accounts/AccountList';
import AccountForm from '../components/accounts/AccountForm';
import { Button } from '../components/ui/button';

const AccountsPage = () => {
  const [accounts, setAccounts] = useState([]);
  const [editingAccount, setEditingAccount] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const fetchAccounts = useCallback(async () => {
    try {
      const response = await accountService.getAccounts();
      setAccounts(response.data);
    } catch (error) {
      console.error('Error fetching accounts:', error);
      // In a real app, show a toast notification
    }
  }, []);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  const handleFormSubmit = async (formData) => {
    try {
      if (editingAccount) {
        await accountService.updateAccount(editingAccount.id, formData);
      } else {
        await accountService.createAccount(formData);
      }
      await fetchAccounts();
      setEditingAccount(null);
      setShowForm(false);
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  const handleEdit = (account) => {
    setEditingAccount(account);
    setShowForm(true);
  };

  const handleAddNew = () => {
    setEditingAccount(null);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    // Optional: Add a confirmation dialog before deleting
    if (window.confirm('Are you sure you want to delete this account?')) {
      try {
        await accountService.deleteAccount(id);
        await fetchAccounts();
      } catch (error) {
        console.error('Error deleting account:', error);
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">Accounts Management</h2>
        <Button onClick={handleAddNew}>Add New Account</Button>
      </div>

      {showForm && (
        <AccountForm
          onSubmit={handleFormSubmit}
          initialData={editingAccount}
        />
      )}

      <div className="mt-6">
        <AccountList accounts={accounts} onEdit={handleEdit} onDelete={handleDelete} />
      </div>
    </div>
  );
};

export default AccountsPage;
