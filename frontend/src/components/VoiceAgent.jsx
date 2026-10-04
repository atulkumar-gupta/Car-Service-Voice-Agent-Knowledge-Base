import { useState, useRef, useEffect } from 'react';
import { useVoice, playAudioBase64 } from '../hooks/useVoice';
import Transcript from './Transcript';
import AssessmentCard from './AssessmentCard';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function VoiceAgent() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        "Hi, I'm AutoAssist. I'll help assess your car issue. What's going on with your vehicle today?",
    },
  ]);
  const [customerInfo, setCustomerInfo] = useState({});
  const [loading, setLoading] = useState(false);
  const [emergency, setEmergency] = useState(false);
  const { recording, start, stop } = useVoice();
  const historyRef = useRef(messages);

  useEffect(() => {
    historyRef.current = messages;
  }, [messages]);

  const sendText = async (text) => {
    if (!text?.trim()) return;
    const userMsg = { role: 'user', content: text };
    const newMsgs = [...messages, userMsg];
    setMessages(newMsgs);
    setLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          history: messages,
          user_text: text,
          customer_info: customerInfo,
        }),
      });
      const data = await res.json();
      setMessages([...newMsgs, { role: 'assistant', content: data.reply }]);
      if (data.audio_base64) playAudioBase64(data.audio_base64);
      if (data.emergency) setEmergency(true);
    } catch (e) {
      setMessages([
        ...newMsgs,
        { role: 'assistant', content: 'Sorry, something went wrong. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleMicClick = async () => {
    if (!recording) {
      await start();
    } else {
      const text = await stop();
      if (text) sendText(text);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>🚗 AutoAssist</h1>
        <p>AI Voice Agent for Car Service — Initial Assessment</p>
      </header>

      {emergency && (
        <div className="emergency">
          ⚠️ Safety emergency reported. Please stop safely and call roadside assistance.
        </div>
      )}

      <div className="layout">
        <div className="chat">
          <Transcript messages={messages} />
          {loading && <div className="loading">AutoAssist is thinking…</div>}
          <div className="controls">
            <button
              className={`mic ${recording ? 'recording' : ''}`}
              onClick={handleMicClick}
              disabled={loading}
            >
              {recording ? '⏹ Stop' : '🎤 Speak'}
            </button>
            <input
              type="text"
              placeholder="Or type your message…"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  sendText(e.target.value);
                  e.target.value = '';
                }
              }}
            />
          </div>
        </div>
        <AssessmentCard info={customerInfo} onSave={setCustomerInfo} />
      </div>
    </div>
  );
}