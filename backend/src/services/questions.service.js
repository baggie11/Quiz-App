import {
  deleteQuestionById,
  deleteQuestionOptionsByQuestionId,
  getQuestionsBySession,
  insertQuestion,
  insertQuestionOptions,
  updateQuestionById,
} from "../db/questions.repo.js";
import {
  normalizeQuestionType,
  validateAndNormalizeOptions,
} from "../utils/questionPayload.js";

const buildQuestionRecord = ({
  session_id,
  question_text,
  question_type,
  order_index,
  image_url,
  explanation,
  options,
}) => ({
  session_id,
  question_text,
  question_type,
  options,
  order_index,
  image_url: image_url ?? null,
  explanation: explanation ?? null,
});

const syncQuestionOptionsTable = async (questionId, questionType, normalizedOptions) => {
  await deleteQuestionOptionsByQuestionId(questionId);

  if (questionType !== "mcq" && questionType !== "singlechoice") {
    return;
  }

  const optionRows = normalizedOptions.map((opt) => ({
    question_id: questionId,
    option_text: opt.option_text,
    is_correct: opt.is_correct,
  }));

  await insertQuestionOptions(optionRows);
};

const normalizeQuestionPayload = (payload) => {
  const questionType = normalizeQuestionType(payload.question_type);
  if (!questionType) {
    throw new Error("Invalid question_type. Use one of: mcq, singlechoice, open, rating.");
  }

  const normalizedOptions = validateAndNormalizeOptions(questionType, payload.options);

  return {
    question_text: String(payload.question_text ?? "").trim() || "Untitled Question",
    question_type: questionType,
    options: normalizedOptions,
    order_index: Number.isFinite(payload.order_index) ? payload.order_index : 0,
    image_url: payload.image_url ?? null,
    explanation: payload.explanation ?? null,
  };
};

/**
 * create a question with options
 */
export async function createQuestion(payload) {
  const normalized = normalizeQuestionPayload(payload);

  const question = await insertQuestion(
    buildQuestionRecord({
      session_id: payload.session_id,
      ...normalized,
    })
  );

  await syncQuestionOptionsTable(question.id, normalized.question_type, normalized.options);

  return question;
}

/**
 * update a question with options
 */
export async function updateQuestion(payload) {
  if (!payload.question_id) {
    throw new Error("question_id is required for update.");
  }

  const normalized = normalizeQuestionPayload(payload);

  const question = await updateQuestionById(
    payload.question_id,
    buildQuestionRecord({
      session_id: payload.session_id,
      ...normalized,
    })
  );

  await syncQuestionOptionsTable(question.id, normalized.question_type, normalized.options);

  return question;
}

/**
 * Get all questions in a session
 */
export async function listQuestions(sessionCode) {
  return await getQuestionsBySession(sessionCode);
}

export async function deleteQuestion(payload) {
  if (!payload.question_id) {
    throw new Error("question_id is required for delete.");
  }
  if (!payload.session_id) {
    throw new Error("session_id is required for delete.");
  }

  await deleteQuestionOptionsByQuestionId(payload.question_id);
  await deleteQuestionById(payload.question_id, payload.session_id);

  return { deleted: true };
}
