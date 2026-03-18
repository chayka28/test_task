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

function normalizeErrorMessage(message, status) {
  if (!message) {
    return status >= 500 ? "Внутренняя ошибка сервера. Попробуйте позже." : `Ошибка запроса (${status}).`;
  }

  return ERROR_MESSAGE_MAP[message] || message;
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

  return response.json();
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
