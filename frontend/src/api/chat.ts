import { SERVER_URL } from './config';

export const askAboutDocuments = async (message: string): Promise<string> => {
  const response = await fetch(`${SERVER_URL}/chat`, {
    method: 'post',
    body: JSON.stringify({
      message,
    }),
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
  });
  if (response.ok) {
    const data: { message: string } = await response.json();
    return data.message;
  } else {
    const data: { detail: string } = await response.json();
    throw new Error(data.detail);
  }
};
