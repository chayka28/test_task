export function formatDateTime(isoString) {
  if (!isoString) return "-";
  const date = new Date(isoString);

  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}
