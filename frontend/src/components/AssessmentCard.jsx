export default function AssessmentCard({ info, onSave }) {
  const fields = [
    ['name', 'Full name'],
    ['phone', 'Phone'],
    ['email', 'Email'],
    ['make_model', 'Make & Model'],
    ['year', 'Year'],
    ['registration', 'Reg / VIN'],
    ['mileage', 'Mileage'],
    ['complaint', 'Primary complaint'],
    ['started', 'When it started'],
    ['frequency', 'Constant / Intermittent'],
    ['warning_lights', 'Warning lights'],
    ['recent_service', 'Recent repair / accident'],
    ['drivable', 'Currently drivable?'],
    ['preferred', 'Preferred location/date'],
  ];
  return (
    <aside className="assessment">
      <h3>Customer & Vehicle Info</h3>
      {fields.map(([k, label]) => (
        <label key={k}>
          <span>{label}</span>
          <input
            value={info[k] || ''}
            onChange={(e) => onSave({ ...info, [k]: e.target.value })}
            placeholder="—"
          />
        </label>
      ))}
    </aside>
  );
}