import express from 'express';
import {
  createQuestionController,
  deleteQuestionController,
  listQuestionsController,
  updateQuestionController,
} from "../controller/questions.controller.js";


const router = express.Router({ mergeParams: true });

router.post('/', createQuestionController);
router.put("/:questionId", updateQuestionController);
router.delete("/:questionId", deleteQuestionController);

// GET /sessions/:sessionId/questions → List questions
router.get('/', listQuestionsController);

export default router;
