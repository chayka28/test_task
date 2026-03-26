const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/+$/, "");
const BASE_API_PATH = `${API_BASE_URL}/api/v1`;

const ERROR_MESSAGE_MAP = {
  "Invalid email or password.": "Неверный email или пароль.",
  "User with this email already exists.": "Пользователь с таким email уже существует.",
  "Token belongs to a deleted user.": "Сессия больше недействительна. Войдите снова.",
  "Could not validate credentials.": "Сессия истекла. Войдите в аккаунт повторно.",
  "Not authenticated": "Войдите в аккаунт, чтобы продолжить.",
  "User not found.": "Пользователь не найден.",
  "Post not found.": "Публикация не найдена.",
  "You can edit only your own posts.": "Можно изменять только свои публикации.",
  "You can delete only your own posts.": "Можно удалять только свои публикации.",
};

const FALLBACK_NAMES = ["Aleksandra", "Alyona", "Nika", "Vlada", "Irina", "blogerich"];
const FALLBACK_TITLES = [
  "Рассуждения на тему правильности и неправильности",
  "500 000 лайков на ютубе делаем, бля буду скидываю",
  "Почему ролик удержал внимание с первых секунд",
  "Как собрать вирусный сюжет из бытовой проблемы",
  "Монтаж без перегруза: где держится внимание",
];
const FALLBACK_TEXTS = [
  "Чтобы выиграть в этой игре нужно быть настоящим психопатом... Еще",
  "500 000 лайков на ютубе делаем, бля буду скидываю 😂😂",
  "Тащить матрас по лестнице: читать этикетки, которые не можешь произнести.",
  "Разбор монтажа, хука и удержания: почему ролик работает на повторных просмотрах.",
  "Показываем проблему, быстро даем решение и закрепляем мысль финальным CTA.",
];

function normalizeErrorMessage(message, status) {
  if (!message) {
    return status >= 500 ? "Внутренняя ошибка сервера. Попробуйте позже." : `Ошибка запроса (${status}).`;
  }

  return ERROR_MESSAGE_MAP[message] || message;
}

function decodeMojibake(value) {
  if (!value) return "";

  const source = String(value).replace(/\u0085/g, "...").replace(/\u0090/g, "");

  if (!/[ÐÑ]/.test(source)) {
    return source;
  }

  try {
    const decoded = decodeURIComponent(escape(source));
    return decoded || source;
  } catch {
    return source;
  }
}

function isBrokenText(value) {
  const text = String(value || "").trim();
  if (!text) return true;

  if (/�/.test(text)) {
    return true;
  }

  const questionMarks = (text.match(/\?/g) || []).length;
  if (questionMarks >= 3 && questionMarks / Math.max(text.length, 1) > 0.18) {
    return true;
  }

  return /^[?\s.,:;!\-()]+$/.test(text);
}

function fallbackName(seed) {
  return FALLBACK_NAMES[Math.abs(Number(seed || 0)) % FALLBACK_NAMES.length];
}

function fallbackTitle(seed) {
  return FALLBACK_TITLES[Math.abs(Number(seed || 0)) % FALLBACK_TITLES.length];
}

function fallbackText(seed) {
  return FALLBACK_TEXTS[Math.abs(Number(seed || 0)) % FALLBACK_TEXTS.length];
}

function sanitizeText(value, fallback) {
  const decoded = decodeMojibake(value);
  return isBrokenText(decoded) ? fallback : decoded;
}

function normalizeUser(user) {
  if (!user || typeof user !== "object") return user;

  return {
    ...user,
    name: sanitizeText(user.name, fallbackName(user.id)),
  };
}

function normalizePost(post) {
  if (!post || typeof post !== "object") return post;

  return {
    ...post,
    user_name: sanitizeText(post.user_name, fallbackName(post.user_id || post.id)),
    title: sanitizeText(post.title, fallbackTitle(post.id)),
    text: sanitizeText(post.text, fallbackText(post.id)),
  };
}

function normalizePayload(payload) {
  if (Array.isArray(payload)) {
    return payload.map((item) => (item && typeof item === "object" && "title" in item ? normalizePost(item) : item));
  }

  if (!payload || typeof payload !== "object") {
    return payload;
  }

  if ("access_token" in payload && payload.user) {
    return {
      ...payload,
      user: normalizeUser(payload.user),
    };
  }

  if ("title" in payload && "text" in payload) {
    return normalizePost(payload);
  }

  if ("name" in payload && "created_at" in payload) {
    return normalizeUser(payload);
  }

  return payload;
}

async function buildRequestError(response) {
  const rawPayload = await response.text();

  if (!rawPayload) {
    return new Error(normalizeErrorMessage("", response.status));
  }

  try {
    const parsedPayload = JSON.parse(rawPayload);
    let detail = rawPayload;

    if (typeof parsedPayload?.detail === "string") {
      detail = parsedPayload.detail;
    } else if (Array.isArray(parsedPayload?.detail)) {
      detail = parsedPayload.detail
        .map((item) => item?.msg)
        .filter(Boolean)
        .join(" ");
    }

    return new Error(normalizeErrorMessage(detail, response.status));
  } catch {
    return new Error(normalizeErrorMessage(rawPayload, response.status));
  }
}

async function request(path, { method = "GET", token, body } = {}) {
  let response;

  try {
    response = await fetch(`${BASE_API_PATH}${path}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
  } catch {
    throw new Error("Не удалось связаться с сервером. Проверьте, что backend запущен.");
  }

  if (!response.ok) {
    throw await buildRequestError(response);
  }

  if (response.status === 204) {
    return null;
  }

  const payload = await response.json();
  return normalizePayload(payload);
}

export async function fetchPostsByUser({ userId, limit, offset }) {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });

  return request(`/posts/user/${userId}?${params.toString()}`);
}

export async function fetchFeedPosts({ limit, offset }) {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });

  return request(`/posts/feed?${params.toString()}`);
}

export async function registerUser({ name, email, password, avatarData }) {
  return request("/users", {
    method: "POST",
    body: {
      name,
      email,
      password,
      avatar_data: avatarData || null,
    },
  });
}

export async function loginUser({ email, password }) {
  return request("/users/login", {
    method: "POST",
    body: {
      email,
      password,
    },
  });
}

export async function fetchTokenByUserId(userId) {
  return request(`/users/${userId}/token`);
}

export async function updateUserName({ userId, name }) {
  return request(`/users/${userId}`, {
    method: "PATCH",
    body: {
      name,
    },
  });
}

export async function deleteUserById(userId) {
  return request(`/users/${userId}`, {
    method: "DELETE",
  });
}

export async function updateMyProfile({ token, name, avatarData }) {
  return request("/users/me/profile", {
    method: "PATCH",
    token,
    body: {
      name: name || null,
      avatar_data: avatarData || null,
    },
  });
}

export async function fetchDemoUser() {
  return request("/users/demo");
}

export async function createPost({ token, title, text, videoUrl, posterUrl, sourceUrl }) {
  return request("/posts", {
    method: "POST",
    token,
    body: {
      title,
      text,
      video_url: videoUrl || null,
      poster_url: posterUrl || null,
      source_url: sourceUrl || null,
    },
  });
}

export async function updatePost({ token, postId, title, text, videoUrl, posterUrl, sourceUrl }) {
  return request(`/posts/${postId}`, {
    method: "PATCH",
    token,
    body: {
      ...(title !== undefined ? { title } : {}),
      ...(text !== undefined ? { text } : {}),
      ...(videoUrl !== undefined ? { video_url: videoUrl || null } : {}),
      ...(posterUrl !== undefined ? { poster_url: posterUrl || null } : {}),
      ...(sourceUrl !== undefined ? { source_url: sourceUrl || null } : {}),
    },
  });
}

export async function deletePost({ token, postId }) {
  return request(`/posts/${postId}`, {
    method: "DELETE",
    token,
  });
}

export async function seedDemoPosts({ token, count = 12, append = false }) {
  const params = new URLSearchParams({
    count: String(count),
    append: String(append),
  });

  return request(`/posts/demo-seed?${params.toString()}`, {
    method: "POST",
    token,
  });
}
