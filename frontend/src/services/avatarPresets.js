export const avatarPresets = [
  {
    id: "preset:midnight",
    label: "Midnight",
    background: "linear-gradient(160deg, #2f3b59 0%, #111827 100%)",
  },
  {
    id: "preset:violet",
    label: "Violet",
    background: "linear-gradient(160deg, #6c4dff 0%, #2e34b5 100%)",
  },
  {
    id: "preset:peach",
    label: "Peach",
    background: "linear-gradient(160deg, #f4b08f 0%, #a65d58 100%)",
  },
  {
    id: "preset:mint",
    label: "Mint",
    background: "linear-gradient(160deg, #76d7d1 0%, #2c6fa6 100%)",
  },
];

export function resolveAvatarVisual(avatarValue, seed = 1) {
  if (typeof avatarValue === "string" && avatarValue.startsWith("data:")) {
    return {
      kind: "image",
      value: avatarValue,
    };
  }

  if (avatarValue) {
    const preset = avatarPresets.find((item) => item.id === avatarValue);
    if (preset) {
      return {
        kind: "gradient",
        value: preset.background,
      };
    }
  }

  const fallbackPreset = avatarPresets[Math.abs(Number(seed || 1)) % avatarPresets.length];
  return {
    kind: "gradient",
    value: fallbackPreset.background,
  };
}
