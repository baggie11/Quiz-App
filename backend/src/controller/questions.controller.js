import {
  createQuestion,
  deleteQuestion,
  listQuestions,
  updateQuestion,
} from "../services/questions.service.js";

/**
 * POST /questions
 */

export async function createQuestionController(req, res) {
  try {
    const { sessionId } = req.params;
    const question = await createQuestion({
      ...req.body,
      session_id: sessionId,
    });

    res.status(201).json({
      success: true,
      data: question,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: error.message,
    });
  }
}

export async function updateQuestionController(req, res) {
  try {
    const { sessionId, questionId } = req.params;
    const question = await updateQuestion({
      ...req.body,
      question_id: questionId,
      session_id: sessionId,
    });

    res.status(200).json({
      success: true,
      data: question,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: error.message,
    });
  }
}

export async function deleteQuestionController(req, res) {
  try {
    const { sessionId, questionId } = req.params;
    await deleteQuestion({
      session_id: sessionId,
      question_id: questionId,
    });

    res.status(200).json({
      success: true,
      data: { deleted: true, question_id: questionId },
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: error.message,
    });
  }
}


/** List all questions for a session
 * @param {Object} req
 * @param {Object} res
 * @returns {Object} response
 */
export async function listQuestionsController(req, res) {
  try {
    const { sessionId } = req.params;
    console.log('Listing questions for sessionId:', sessionId);

    const questions = await listQuestions(sessionId);

    console.log('Questions retrieved:', questions);

    return res.status(200).json({
      status: "ok",
      data: questions
    });

    

  } catch (err) {
    return res.status(500).json({
      status: "error",
      message: err.message
    });
  }
}
