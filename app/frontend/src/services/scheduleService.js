import axios from 'axios';

const API_URL = 'http://localhost:8001/api';

const getSchedules = () => {
  return axios.get(`${API_URL}/schedules/`);
};

const getSchedule = (id) => {
  return axios.get(`${API_URL}/schedules/${id}`);
};

const createSchedule = (schedule) => {
  return axios.post(`${API_URL}/schedules/`, schedule);
};

const updateSchedule = (id, schedule) => {
  return axios.patch(`${API_URL}/schedules/${id}`, schedule);
};

const deleteSchedule = (id) => {
  return axios.delete(`${API_URL}/schedules/${id}`);
};

const scheduleService = {
  getSchedules,
  getSchedule,
  createSchedule,
  updateSchedule,
  deleteSchedule,
};

export default scheduleService;
