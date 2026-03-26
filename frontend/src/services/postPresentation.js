function seededValue(seed) {
  const safeSeed = Number.isFinite(seed) ? Math.abs(seed) : 1;
  return (safeSeed * 9301 + 49297) % 233280;
}

const mediaPalettes = [
  {
    start: "#b59d77",
    end: "#6f5442",
    accent: "#f6dcc1",
    glow: "rgba(255, 223, 197, 0.46)",
    surface: "rgba(48, 23, 15, 0.58)",
  },
  {
    start: "#1f2235",
    end: "#5a3a54",
    accent: "#f3d8e9",
    glow: "rgba(183, 149, 255, 0.36)",
    surface: "rgba(14, 15, 26, 0.6)",
  },
  {
    start: "#384f66",
    end: "#151822",
    accent: "#cae6ff",
    glow: "rgba(110, 176, 255, 0.32)",
    surface: "rgba(13, 24, 41, 0.58)",
  },
  {
    start: "#8d7f5c",
    end: "#3a2b2c",
    accent: "#f2d7c9",
    glow: "rgba(255, 199, 168, 0.34)",
    surface: "rgba(42, 20, 18, 0.58)",
  },
];

const showcaseBadges = [
  { label: "Просмотры", tone: "views" },
  { label: "Лайки", tone: "likes" },
  { label: "Комментарии", tone: "comments" },
  null,
];

const topics = ["Базы данных", "ИИ", "Чат-боты", "Программирование", "Айти", "Макбук", "Кофе"];

export function formatCompactNumber(value, options = {}) {
  const { upperK = false } = options;

  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(1).replace(".", ",")} млн`;
  }

  if (value >= 1000) {
    return `${Math.round(value / 100) / 10}${upperK ? "K" : "k"}`;
  }

  return String(value);
}

export function buildHandle(userId) {
  const variants = ["@blogerich", "@trendmaker", "@socialpulse", "@viral.lab", "@contentforge"];
  return variants[Math.abs(Number(userId || 0)) % variants.length];
}

export function buildUserHandle(userName, userId) {
  const normalized = String(userName || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "")
    .replace(/[^\p{L}\p{N}_.]+/gu, "");

  if (normalized) {
    return `@${normalized}`;
  }

  return buildHandle(userId);
}

export function buildFollowers(userId) {
  const seed = seededValue(Number(userId || 1) + 17);
  const base = 10_500 + (seed % 420_000);
  const compact = formatCompactNumber(base, { upperK: true });
  return base < 100_000 ? `${compact} Подписчиков` : compact;
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
  return topics[Math.abs(Number(postId || 0)) % topics.length];
}

export function buildShowcaseBadge(postId) {
  return showcaseBadges[Math.abs(Number(postId || 0)) % showcaseBadges.length];
}
