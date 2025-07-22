import type { LoadedDocument } from '../models';
import { SERVER_URL } from './config';

export const getDocuments = async (): Promise<LoadedDocument[]> => {
  const response = await fetch(`${SERVER_URL}/documents`, {
    credentials: 'include',
  });
  if (response.ok) {
    const data: { documents: LoadedDocument[] } = await response.json();
    return data.documents;
  } else {
    const data: { detail: string } = await response.json();
    throw new Error(data.detail);
  }
};

export const sendDocument = async (
  formData: FormData
): Promise<LoadedDocument> => {
  const response = await fetch(`${SERVER_URL}/documents`, {
    method: 'post',
    body: formData,
    credentials: 'include',
  });
  if (response.ok) {
    const data: LoadedDocument = await response.json();
    return data;
  } else {
    const data: { detail: string } = await response.json();
    throw new Error(data.detail);
  }
};

export const deleteDocument = async (document_id: string): Promise<void> => {
  const response = await fetch(`${SERVER_URL}/documents/${document_id}`, {
    method: 'delete',
    credentials: 'include',
  });
  if (!response.ok) {
    throw new Error('Server error');
  }
};

export const getSummary = async (document_id: string): Promise<string> => {
  const response = await fetch(
    `${SERVER_URL}/documents/${document_id}/summary`,
    {
      method: 'get',
      credentials: 'include',
    }
  );
  if (response.ok) {
    const data: { message: string } = await response.json();
    return data.message;
  } else {
    const data: { detail: string } = await response.json();
    throw new Error(data.detail);
  }
};
