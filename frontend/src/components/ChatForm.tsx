import { useState } from 'react';

export const ChatForm = ({
  sendQuestion,
  loading,
}: {
  sendQuestion: (message: string) => void;
  loading: boolean;
}) => {
  const [message, setMessage] = useState<string>('');
  return (
    <form
      className='items-center my-4 flex justify-start gap-2'
      method='post'
      onSubmit={e => {
        e.preventDefault();
        if (loading || !message) return;

        sendQuestion(message);
      }}
    >
      <input
        placeholder='Вопрос по загруженным документам'
        name='message'
        value={message}
        className='py-2 px-3 border rounded-sm border-gray-600 cursor-pointer text-sm focus:border-gray-400 outline-0 w-full'
        onChange={e => setMessage(e.target.value)}
      />
      <input
        type='submit'
        value='Спросить'
        className='cursor-pointer bg-green-800 hover:bg-green-700 py-2 px-3 rounded-sm text-sm'
      />
    </form>
  );
};
