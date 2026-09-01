interface StatusBadgeProps {
  status: string;
  isRunning: boolean;
}

export default function StatusBadge({ status, isRunning }: StatusBadgeProps) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: isRunning ? '#10b981' : '#ef4444' }}></div>
      <span style={{ color: isRunning ? '#34d399' : '#f87171', fontWeight: 600, fontSize: '14px', textTransform: 'uppercase' }}>
        {status}
      </span>
    </div>
  );
}