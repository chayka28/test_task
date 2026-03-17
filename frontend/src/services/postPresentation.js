function seededValue(seed) {
  const safeSeed = Number.isFinite(seed) ? Math.abs(seed) : 1;
  return (safeSeed * 9301 + 49297) % 233280;
}

const mediaPalettes = [
  {
    start: "#a7936f",
    end: "#5f4637",
    accent: "#f7d9a1",
    glow: "rgba(255, 210, 170, 0.48)",
    surface: "rgba(52, 27, 16, 0.28)",
  },
  {
    start: "#1f2135",
    end: "#58364f",
    accent: "#f2d6eb",
    glow: "rgba(191, 153, 255, 0.35)",
    surface: "rgba(20, 18, 31, 0.34)",
  },
  {
    start: "#324257",
    end: "#111827",
    accent: "#cfe4ff",
    glow: "rgba(98, 173, 255, 0.34)",
    surface: "rgba(13, 24, 41, 0.34)",
  },
  {
    start: "#65535d",
    end: "#261b23",
    accent: "#ffe0cf",
    glow: "rgba(255, 158, 158, 0.34)",
    surface: "rgba(39, 17, 22, 0.34)",
  },
];

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

export function buildPostMetricValues(postId) {
  const seed = seededValue(Number(postId || 1));
  const views = 60_000 + (seed % 3_200_000);
  const likes = Math.round(views * 0.17);
  const comments = Math.round(views * 0.036);
  const shares = Math.round(views * 0.011);

  return {
    views,
    likes,
    comments,
    shares,
  };
}

export function buildMediaPalette(postId) {
  return mediaPalettes[Math.abs(Number(postId || 0)) % mediaPalettes.length];
}

export function buildPostTopic(postId) {
  const topics = ["Базы данных", "ИИ", "Чат-боты", "Программирование", "Айти", "Макбук", "Кофе"];
  return topics[Math.abs(Number(postId || 0)) % topics.length];
}
