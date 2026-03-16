const SESSION_KEY = "trendsee-session";
const LIKES_KEY = "trendsee-liked-posts";

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
  };
}

export function saveSession(session) {
  window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearSession() {
  window.localStorage.removeItem(SESSION_KEY);
}

export function loadLikedPostIds() {
  return new Set(readJson(LIKES_KEY, []));
}

export function saveLikedPostIds(postIds) {
  window.localStorage.setItem(LIKES_KEY, JSON.stringify([...postIds]));
}
