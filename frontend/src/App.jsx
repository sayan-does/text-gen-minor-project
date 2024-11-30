import React, { useState, useRef } from 'react';
import { FileUpload } from './components/FileUpload';
import { ChatSection } from './components/ChatSection';
import { PlagiarismModal } from './components/PlagiarismModal';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [showPlagCheck, setShowPlagCheck] = useState(false);
  const mediaRecorderRef = useRef(null);

  const handleNewMessage = (message) => {
    setMessages(prev => [...prev, message]);
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Upload failed');
      
      handleNewMessage({
        type: 'system',
        content: 'Document uploaded and processed successfully'
      });
    } catch (error) {
      console.error('Upload error:', error);
      handleNewMessage({
        type: 'error',
        content: 'Failed to upload document'
      });
    }
  };

  return (
    <div className="flex h-screen bg-gray-100 p-4">
      <div className="flex w-full gap-4">
        <ChatSection 
          messages={messages}
          onNewMessage={handleNewMessage}
          isRecording={isRecording}
          setIsRecording={setIsRecording}
          mediaRecorderRef={mediaRecorderRef}
          onPlagiarismCheck={() => setShowPlagCheck(true)}
        />
        <FileUpload onFileUpload={handleFileUpload} />
      </div>
      {showPlagCheck && (
        <PlagiarismModal 
          onClose={() => setShowPlagCheck(false)}
          lastMessage={messages[messages.length - 1]}
        />
      )}
    </div>
  );
}

export default App;