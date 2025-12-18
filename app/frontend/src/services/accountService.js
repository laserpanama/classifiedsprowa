import axios from 'axios';

// A default API URL for local development.
// In a real app, this would be configured via .env files for different environments.
const API_URL = 'http://localhost:8001/api';

const getAccounts = () => {
  return axios.get(`${API_URL}/accounts/`);
};

const getAccount = (id) => {
  return axios.get(`${API_URL}/accounts/${id}`);
};

const createAccount = (account) => {
  return axios.post(`${API_URL}/accounts/`, account);
};

const updateAccount = (id, account) => {
  return axios.patch(`${API_URL}/accounts/${id}`, account);
};

const deleteAccount = (id) => {
  return axios.delete(`${API_URL}/accounts/${id}`);
};

const accountService = {
  getAccounts,
  getAccount,
  createAccount,
  updateAccount,
  deleteAccount,
};

export default accountService;
