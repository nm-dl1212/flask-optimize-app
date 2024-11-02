import axios from 'axios';

const DUMMY_API_URL = 'http://localhost:5002';
const OPTIMIZE_API_URL = 'http://localhost:5003';

const authHeader = () => {
  const token = localStorage.getItem('token');
  return { Authorization: `Bearer ${token}` };
};

export const dummyCalculation = async (x1: number, x2: number) => {
  return axios.post(
    `${DUMMY_API_URL}/dummy`,
    { x1, x2 },
    { headers: authHeader() }
  );
};

export const optimize = async (initial_x1: number, initial_x2: number, n_trials: number) => {
  return axios.post(
    `${OPTIMIZE_API_URL}/optimize`,
    //{ initial_x1, initial_x2, n_trials },
    //{ headers: authHeader() }
  );
};
