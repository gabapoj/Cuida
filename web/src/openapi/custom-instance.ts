import axios from 'axios';

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true,
});

export const customInstance = async <T>(
  url: string,
  config?: RequestInit,
): Promise<T> => {
  const response = await instance({
    url,
    method: (config?.method ?? 'GET') as string,
    headers: config?.headers as Record<string, string>,
    data: config?.body,
  });
  return {
    data: response.data,
    status: response.status,
    headers: response.headers as unknown as Headers,
  } as T;
};

export default customInstance;
export { instance };
