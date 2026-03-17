const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/+$/, "");
const BASE_API_PATH = `${API_BASE_URL}/api/v1`;

async function request(path, { method = "GET", token, body } = {}) {
  const response = await fetch(`${BASE_API_PATH}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Ошибка запроса (${response.status}): ${errorText}`);
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
