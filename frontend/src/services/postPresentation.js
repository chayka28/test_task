function seededValue(seed) {
  const safeSeed = Number.isFinite(seed) ? Math.abs(seed) : 1;
  return (safeSeed * 9301 + 49297) % 233280;
}

export function formatCompactNumber(value) {
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(1).replace(".", ",")} млн`;
  }
  if (value >= 1000) {
    return `${Math.round(value / 100) / 10}k`;
  }
  return String(value);
}

export function buildHandle(userId) {
  const variants = ["@blogerich", "@trendmaker", "@socialpulse", "@viral.lab", "@contentforge"];
  return variants[Math.abs(Number(userId || 0)) % variants.length];
}

export function buildFollowers(userId) {
  const seed = seededValue(Number(userId || 1) + 17);
  const base = 120_000 + (seed % 380_000);
  return formatCompactNumber(base);
}

export function buildPostMetrics(postId) {
  const seed = seededValue(Number(postId || 1));
  const views = 60_000 + (seed % 3_200_000);
  const likes = Math.round(views * 0.17);
  const comments = Math.round(views * 0.036);
  const shares = Math.round(views * 0.011);
  const er = ((likes + comments + shares) / Math.max(views, 1)) * 100;

  return {
    views: formatCompactNumber(views),
    likes: formatCompactNumber(likes),
    comments: formatCompactNumber(comments),
    shares: formatCompactNumber(shares),
    er: `${er.toFixed(1).replace(".", ",")}%`,
  };
}
