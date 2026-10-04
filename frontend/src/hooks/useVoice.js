import { useRef, useState, useCallback } from 'react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function useVoice() {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);

  const start = useCallback(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    streamRef.current = stream;
    const mr = new MediaRecorder(stream, { mimeType: 'audio/webm' });
    chunksRef.current = [];
    mr.ondataavailable = (e) => e.data.size && chunksRef.current.push(e.data);
    mr.start();
    mediaRecorderRef.current = mr;
    setRecording(true);
  }, []);

  const stop = useCallback(() => {
    return new Promise((resolve) => {
      const mr = mediaRecorderRef.current;
      if (!mr) return resolve(null);
      mr.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        streamRef.current?.getTracks().forEach((t) => t.stop());
        setRecording(false);
        const fd = new FormData();
        fd.append('file', blob, 'audio.webm');
        try {
          const res = await fetch(`${API}/stt`, { method: 'POST', body: fd });
          const data = await res.json();
          resolve(data.text);
        } catch (e) {
          console.error(e);
          resolve(null);
        }
      };
      mr.stop();
    });
  }, []);

  return { recording, start, stop };
}

export function playAudioBase64(b64) {
  if (!b64) return;
  const audio = new Audio(`data:audio/mpeg;base64,${b64}`);
  audio.play().catch((e) => console.warn('play failed', e));
}