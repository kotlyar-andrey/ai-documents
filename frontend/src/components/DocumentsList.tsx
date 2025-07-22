import clsx from 'clsx';

import type { LoadedDocument } from '../models';

export const DocumentsList = ({
  documents,
  loading: loading,
  deleteDocument,
  summaryDocument,
}: {
  documents: LoadedDocument[];
  loading: boolean;
  deleteDocument: (document_id: string) => void;
  summaryDocument: (document_id: string) => void;
}) => {
  return (
    <div>
      {documents.length > 0 ? (
        <ul>
          {documents.map(document => (
            <li
              key={document.id}
              className='flex justify-between p-2 bg-gray-900 rounded-sm mb-1'
            >
              <p>{document.name}</p>
              <div className='gap-4 flex'>
                <button
                  className={clsx('text-xs ', {
                    'text-red-700 hover:text-red-600 cursor-pointer': !loading,
                    'text-gray-700 hover:text-gray-600 cursor-not-allowed':
                      loading,
                  })}
                  onClick={() => {
                    if (!loading) deleteDocument(document.id);
                  }}
                >
                  удалить
                </button>
                <button
                  className={clsx('text-xs', {
                    'text-blue-500 hover:text-blue-400 cursor-pointer':
                      !loading,
                    'text-gray-700 hover:text-gray-600 cursor-not-allowed':
                      loading,
                  })}
                  onClick={() => {
                    if (!loading) summaryDocument(document.id);
                  }}
                >
                  краткое содержание
                </button>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className='text-sm italic text-gray-400'>
          Нет загруженных документов
        </p>
      )}
    </div>
  );
};
