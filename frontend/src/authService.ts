import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/'; 

// Função para login e obter o token
export const login = async (username: string, password: string) => {
    try {
        const response = await axios.post(`${API_URL}token/`, { username, password });
        const { access_token } = response.data;
        localStorage.setItem('token', access_token);  
        return access_token;
    } catch (error) {
        console.error('Error logging in:', error);
        throw error;
    }
};

// Função para obter dados de uma rota protegida
export const getProtectedData = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        throw new Error('No token found');
    }

    try {
        const response = await axios.get(`${API_URL}protected/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching protected data:', error);
        throw error;
    }
};
