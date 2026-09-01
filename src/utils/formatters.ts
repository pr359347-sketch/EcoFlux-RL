export function formatCo2Value(value: number): string {
  return value.toFixed(1);
}

export function formatWaitTime(seconds: number): string {
  return `${seconds.toFixed(1)}s`;
}