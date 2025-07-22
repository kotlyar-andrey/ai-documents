import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

import { askAboutDocuments } from './api/chat';
import {
  deleteDocument,
  getDocuments,
  getSummary,
  sendDocument,
} from './api/documents';
import { ChatForm } from './components/ChatForm';
import { DocumentsList } from './components/DocumentsList';
import { LoadDocumentForm } from './components/LoadDocumentForm';

import type { LoadedDocument } from './models';
function App() {
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [loadedDocuments, setLoadedDocuments] = useState<LoadedDocument[]>([]);
  const [summary, setSummary] = useState<string>('');
  const [selectedDocumentName, setSelectedDocumentName] = useState<
    string | undefined
  >('');
  const [chatAnswer, setChatAnswer] = useState<string>('');

  const loadDocumentsFromServer = async () => {
    setLoading(true);
    setErrorMessage('');
    try {
      const documents = await getDocuments();
      setLoadedDocuments(documents);
    } catch (error: unknown) {
      setErrorMessage(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const sendDocumentToServer = async (formData: FormData) => {
    setLoading(true);
    setErrorMessage('');
    try {
      const data = await sendDocument(formData);
      setLoadedDocuments(prev => {
        return [...prev, data];
      });
    } catch (error: unknown) {
      setErrorMessage(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const deleteDocumentOnServer = async (document_id: string) => {
    setLoading(true);
    setErrorMessage('');
    try {
      await deleteDocument(document_id);
      setLoadedDocuments(prev => prev.filter(doc => doc.id !== document_id));
    } catch (error: unknown) {
      setErrorMessage(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const getSummaryAboutDocument = async (document_id: string) => {
    setLoading(true);
    setErrorMessage('');
    try {
      const message = await getSummary(document_id);
      setSummary(message);
      setSelectedDocumentName(
        loadedDocuments.find(doc => doc.id === document_id)?.name
      );
    } catch {
    } finally {
      setLoading(false);
    }
  };

  const getChatAnswer = async (message: string) => {
    if (!message) return;
    setLoading(true);
    setErrorMessage('');
    try {
      const answer = await askAboutDocuments(message);
      setChatAnswer(answer);
    } catch (error: unknown) {
      setErrorMessage(error instanceof Error ? error.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocumentsFromServer();
  }, []);

  return (
    <div className='bg-gray-800 min-h-screen text-gray-200'>
      <div className='mx-auto max-w-screen-lg'>
        <h1 className='text-center text-2xl border-b p-4'>
          Ai for working with documents
        </h1>
        {errorMessage && (
          <p className='text-xl text-red-400 text-center'>{errorMessage}</p>
        )}
        {loading && (
          <p className='text-xl text-gray-400 text-center'>загрузка...</p>
        )}
        <div className='p-2 justify-between md:grid md:grid-cols-2 gap-4'>
          <section>
            <h2 className='text-xl mb-2'>Документы </h2>

            <DocumentsList
              documents={loadedDocuments}
              loading={loading}
              deleteDocument={deleteDocumentOnServer}
              summaryDocument={getSummaryAboutDocument}
            />
            <LoadDocumentForm
              loading={loading}
              sendDocumentToServer={sendDocumentToServer}
            />
            <hr className='border-b my-10' />
            {loadedDocuments.length > 0 ? (
              <>
                <ChatForm loading={loading} sendQuestion={getChatAnswer} />
                {chatAnswer && (
                  <ReactMarkdown>{`Ответ:  ${chatAnswer}`}</ReactMarkdown>
                )}
              </>
            ) : (
              <p className='text-sm italic text-gray-400'>
                Загрузите хотя бы один документ, чтобы задавать вопросы
              </p>
            )}
          </section>
          <section>
            {selectedDocumentName && (
              <>
                <h2 className='text-xl mb-2'>"{selectedDocumentName}"</h2>
                <ReactMarkdown>{summary}</ReactMarkdown>
              </>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;
