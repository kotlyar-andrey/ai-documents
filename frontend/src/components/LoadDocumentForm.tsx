import { useState } from 'react';

export const LoadDocumentForm = ({
  sendDocumentToServer,
  loading,
}: {
  sendDocumentToServer: (formData: FormData) => void;
  loading: boolean;
}) => {
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!file || loading) return;

    const formData = new FormData();
    formData.append('file', file);

    sendDocumentToServer(formData);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  return (
    <form
      method='post'
      encType='multipart/form-data'
      className='items-center my-4 flex justify-start gap-2'
      onSubmit={handleSubmit}
    >
      <input
        type='file'
        name='file'
        className='py-2 px-3 border rounded-sm border-gray-600 cursor-pointer text-sm w-full'
        onChange={handleChange}
      />

      <input
        type='submit'
        value='Загрузить'
        className='cursor-pointer bg-green-800 hover:bg-green-700 py-2 px-3 rounded-sm text-sm'
      />
    </form>
  );
};
