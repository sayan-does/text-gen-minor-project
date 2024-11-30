import React, { useEffect } from 'react';
import { Mic, MicOff, Send } from 'lucide-react';

export function ChatSection({
  messages,
  onNewMessage,
  isRecording,
  setIsRecording,
  mediaRecorderRef,
  onPlagiarismCheck
}) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = async () => {
          const base64Audio = reader.result.split(',')[1];
          await sendMessage('', base64Audio);
        };
      };

      recorder.start();
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
    } catch (err) {
      console.error('Error accessing microphone:', err);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const sendMessage = async (text = '', audioData = null) => {
    if (!text && !audioData) return;

    onNewMessage({ type: 'user', content: text || 'Audio message' });

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          audio_data: audioData
        })
      });

      const data = await response.json();
      onNewMessage({ type: 'bot', content: data.response });
    } catch (err) {
      console.error('Error sending message:', err);
      onNewMessage({ type: 'error', content: 'Failed to send message' });
    }
  };

  return (
    <div className="flex flex-col flex-grow bg-white rounded-lg shadow-lg p-4">
      <div className="flex-grow overflow-y-auto mb-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`mb-4 p-3 rounded-lg ${
              msg.type === 'user' 
                ? 'bg-blue-100 ml-auto mr-2'
                : msg.type === 'bot'
                ? 'bg-gray-100 mr-auto ml-2'
                : 'bg-gray-50 text-center'
            } max-w-[70%]`}
          >
            {msg.content}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="flex gap-2 items-center">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className="p-2 rounded-full bg-blue-500 hover:bg-blue-600 text-white"
        >
          {isRecording ? <MicOff size={24} /> : <Mic size={24} />}
        </button>
        
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              sendMessage(inputText);
              setInputText('');
            }
          }}
          className="flex-grow p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Type your message..."
        />
        
        <button
          onClick={() => {
            sendMessage(inputText);
            setInputText('');
          }}
          className="p-2 rounded-full bg-blue-500 hover:bg-blue-600 text-white"
        >
          <Send size={24} />
        </button>
        
        <button
          onClick={onPlagiarismCheck}
          className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg"
        >
          Check AI Content
        </button>
      </div>
    </div>
  );
}