export const QUESTION_TYPE_MAP = {
  MCQ: "mcq",
  "Single Choice": "singlechoice",
  "Open Text": "open",
  Rating: "rating",
};

const ALLOWED_TYPES = new Set(["mcq", "singlechoice", "open", "rating"]);

const TYPE_ALIASES = {
  mcq: "mcq",
  multiple_choice: "mcq",
  msq: "mcq",
  multi: "mcq",
  "multiple choice": "mcq",
  "single choice": "singlechoice",
  singlechoice: "singlechoice",
  quiz: "singlechoice",
  rating: "rating",
  open: "open",
  open_ended: "open",
  "open text": "open",
};

const normalizeOptionObject = (option) => {
  if (typeof option === "string") {
    return {
      option_text: option.trim(),
      is_correct: false,
    };
  }

  return {
    option_text: String(option?.option_text ?? "").trim(),
    is_correct: Boolean(option?.is_correct),
  };
};

export const normalizeQuestionType = (value) => {
  const raw = String(value || "").trim();
  if (!raw) return null;

  if (QUESTION_TYPE_MAP[raw]) {
    return QUESTION_TYPE_MAP[raw];
  }

  const alias = TYPE_ALIASES[raw.toLowerCase()];
  if (alias && ALLOWED_TYPES.has(alias)) {
    return alias;
  }

  return null;
};

export const validateAndNormalizeOptions = (questionType, options) => {
  if (questionType === "open") {
    if (options == null) return null;
    if (Array.isArray(options) && options.length === 0) return null;
    throw new Error("Open Text questions must have null or empty options.");
  }

  if (questionType === "rating") {
    if (!options || typeof options !== "object" || Array.isArray(options)) {
      throw new Error("Rating questions need options object: { min, max, labels? }.");
    }

    const min = Number(options.min);
    const max = Number(options.max);

    if (!Number.isFinite(min) || !Number.isFinite(max) || max <= min) {
      throw new Error("Rating options must include numeric min and max where max > min.");
    }

    const normalized = { min, max };
    if (Array.isArray(options.labels)) {
      normalized.labels = options.labels.map((label) => String(label).trim()).filter(Boolean);
    }

    return normalized;
  }

  if (!Array.isArray(options)) {
    throw new Error("Choice questions require options as an array.");
  }

  const normalizedOptions = options
    .map(normalizeOptionObject)
    .filter((opt) => opt.option_text);

  if (normalizedOptions.length < 2) {
    throw new Error("Choice questions require at least 2 options.");
  }

  if (questionType === "singlechoice") {
    const correctCount = normalizedOptions.filter((opt) => opt.is_correct).length;
    if (correctCount !== 1) {
      throw new Error("Single Choice questions must have exactly one correct option.");
    }
  }

  return normalizedOptions;
};
