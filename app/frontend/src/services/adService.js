import axios from 'axios';

const API_URL = 'http://localhost:8001/api';

const getAds = () => {
  return axios.get(`${API_URL}/ads/`);
};

const getAd = (id) => {
  return axios.get(`${API_URL}/ads/${id}`);
};

const createAd = (ad) => {
  return axios.post(`${API_URL}/ads/`, ad);
};

const updateAd = (id, ad) => {
  return axios.patch(`${API_URL}/ads/${id}`, ad);
};

const deleteAd = (id) => {
  return axios.delete(`${API_URL}/ads/${id}`);
};

const generateAdText = (prompt) => {
  return axios.post(`${API_URL}/ads/generate-text`, { prompt });
};

const adService = {
  getAds,
  getAd,
  createAd,
  updateAd,
  deleteAd,
  generateAdText,
};

export default adService;
