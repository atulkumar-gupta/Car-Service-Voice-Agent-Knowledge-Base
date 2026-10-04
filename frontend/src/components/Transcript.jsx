export default function Transcript({ messages }) {
  return (
    <div className="transcript">
      {messages.length === 0 && (
        <p className="empty">Press the mic and describe your car issue…</p>
      )}
      {messages.map((m, i) => (
        <div key={i} className={`bubble ${m.role}`}>
          <span className="who">{m.role === 'user' ? 'You' : 'AutoAssist'}</span>
          <p>{m.content}</p>
        </div>
      ))}
    </div>
  );
}