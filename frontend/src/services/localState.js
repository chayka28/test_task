const SESSION_KEY = "trendsee-session";
const FAVORITES_KEY = "trendsee-favorite-posts";
function readJson(key, fallbackValue) {
  try {
    const rawValue = window.localStorage.getItem(key);
    return rawValue ? JSON.parse(rawValue) : fallbackValue;
  } catch {
    return fallbackValue;
  }
}

export function loadSession() {
  const session = readJson(SESSION_KEY, null);

  if (!session) return null;

  return {
    accessToken: session.accessToken || session.token || session.access_token || null,
    tokenType: session.tokenType || session.token_type || "bearer",
    user: session.user || null,
    email: session.email || session.userEmail || null,
  };
}

export function saveSession(session) {
  window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearSession() {
  window.localStorage.removeItem(SESSION_KEY);
}

export function loadFavoritePostIds(userId) {
  if (!userId) return new Set();

  const favoriteMap = readJson(FAVORITES_KEY, {});
  return new Set(Array.isArray(favoriteMap[userId]) ? favoriteMap[userId] : []);
}

export function saveFavoritePostIds(userId, postIds) {
  if (!userId) return;

  const favoriteMap = readJson(FAVORITES_KEY, {});
  favoriteMap[userId] = [...postIds];
  window.localStorage.setItem(FAVORITES_KEY, JSON.stringify(favoriteMap));
}

export function clearFavoritePostIds(userId) {
  if (!userId) return;

  const favoriteMap = readJson(FAVORITES_KEY, {});
  delete favoriteMap[userId];
  window.localStorage.setItem(FAVORITES_KEY, JSON.stringify(favoriteMap));
}
