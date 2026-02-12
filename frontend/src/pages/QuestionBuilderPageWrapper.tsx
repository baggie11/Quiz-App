// Replace your current QuestionBuilderPage with this version
import React, {
  useState,
  useEffect,
  useCallback,
  useMemo,
} from 'react';
import { useNavigate } from 'react-router-dom'; // Add this import
import { ArrowLeft, AlertCircle } from 'lucide-react'; // Add ArrowLeft import
import { API } from '../api/config';
import {
  DB_TYPE_TO_QTYPE,
  formatQuestionPayload,
  validateQuestionForSave,
} from "../utils/questionPayload";

import type {
  Question,
  QType,
  QuestionBuilderProps,
  SaveState,
} from '../types';

import { QuestionHeader } from '../components/Questions/QuestionHeader';
import { QuestionPalette } from '../components/Questions/QuestionPalette';
import { QuestionEditor } from '../components/Questions/QuestionEditor';
import { QuestionPreview } from '../components/Questions/QuestionPreview';
import { useParams } from "react-router-dom";

// Helpers
const uid = (prefix = "q"): string =>
  `${prefix}_${Date.now().toString(36)}_${Math.floor(Math.random() * 1000)}`;

const defaultOption = (n = 1): string => `Option ${n}`;

export const QuestionBuilderPage: React.FC<QuestionBuilderProps> = ({
  sessionId: propSessionId,
  onPreview,
  initialQuestions = [],
}) => {
  const navigate = useNavigate(); // Add navigate hook
  const [questions, setQuestions] = useState<Question[]>(initialQuestions);
  const [paletteOpen, setPaletteOpen] = useState(true);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [sessionCode, setSessionCode] = useState<string | null>(null);
  const [filter, setFilter] = useState<"all" | QType | "drafts">("all");
  const [currentQuestionId, setCurrentQuestionId] = useState<string | null>(
    initialQuestions[0]?.id || null
  );
  const [loading, setLoading] = useState<boolean>(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [saveState, setSaveState] = useState<SaveState>({
    isSaving: false,
    lastSaved: null,
    hasUnsavedChanges: false,
    autoSaveEnabled: false,
    saveError: null,
  });

  const { sessionId: paramSessionId } = useParams<{ sessionId?: string }>();
  const sessionId = paramSessionId || propSessionId;

  // Handle back button click
  const handleBackClick = useCallback(() => {
    navigate(-1); // Go back to previous page
  }, [navigate]);

  // Load existing questions from the database
  // Replace the loadExistingQuestions function in your code with this version:

// Load existing questions from the database
const loadExistingQuestions = useCallback(async () => {
  if (!sessionId) {
    setLoading(false);
    return;
  }

  setLoading(true);
  setLoadError(null);

  try {
    const token = localStorage.getItem("token");
    
    const response = await fetch(
      `${API.node}/api/sessions/${sessionId}/questions`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(errText || "Failed to load questions");
    }

    const result = await response.json();
    console.log("Loaded questions from server:", result);

    // Extract questions from the response format
    // Response format: {"status":"ok","data":[...]}
    const questionsData = result.data || [];
    
    if (!Array.isArray(questionsData)) {
      console.warn("Expected questions data to be an array, got:", questionsData);
      setQuestions([]);
      setLoading(false);
      return;
    }

    // Transform API data to local Question format
    const loadedQuestions: Question[] = questionsData.map((item: any, index: number) => {
      const normalizedType = String(item.question_type || "").toLowerCase();
      const legacyTypeMap: Record<string, QType> = {
        multiple_choice: "multi",
        msq: "multi",
        multiple_select: "multi",
        single_choice: "quiz",
        quiz: "quiz",
        open_ended: "open",
      };
      const questionType =
        DB_TYPE_TO_QTYPE[normalizedType as keyof typeof DB_TYPE_TO_QTYPE] ||
        legacyTypeMap[normalizedType] ||
        "quiz";
      
      let options: string[] | undefined;
      let correctAnswer: number | undefined;
      let multiAnswers: number[] | undefined;
      let ratingMin: number | undefined;
      let ratingMax: number | undefined;
      let ratingLabels: string[] | undefined;

      const optionsFromJson = Array.isArray(item.options) ? item.options : null;
      const optionsFromRelation = Array.isArray(item.question_options) ? item.question_options : null;

      if (questionType === "quiz" || questionType === "multi") {
        const sourceOptions = optionsFromJson ?? optionsFromRelation ?? [];
        options = sourceOptions.map((opt: any) =>
          typeof opt === "string" ? opt : (opt.option_text || "").trim()
        );

        if (questionType === "quiz") {
          const correctIndex = sourceOptions.findIndex((opt: any) =>
            typeof opt === "string" ? false : !!opt.is_correct
          );
          if (correctIndex >= 0) correctAnswer = correctIndex;
        } else {
          multiAnswers = sourceOptions
            .map((opt: any, idx: number) =>
              typeof opt === "string" ? -1 : (opt.is_correct ? idx : -1)
            )
            .filter((idx: number) => idx >= 0);
        }

        if (!options?.length) {
          options = ["Option 1", "Option 2"];
        }
      }

      if (questionType === "rating") {
        const ratingPayload = item.options && typeof item.options === "object" ? item.options : {};
        ratingMin = ratingPayload.min || 1;
        ratingMax = ratingPayload.max || item.rating_max || item.max_rating || 5;
        ratingLabels = Array.isArray(ratingPayload.labels) ? ratingPayload.labels : undefined;
      }

      return {
        id: item.id || item.question_id || uid(),
        text: item.question_text || item.text || `Untitled Question ${index + 1}`,
        type: questionType,
        options,
        correctAnswer,
        multiAnswers,
        ratingMin,
        ratingMax,
        ratingLabels,
        meta: {
          draft: false, // Existing questions are already saved
          imageUrl: item.image_url || item.imageUrl || undefined,
          explanation: item.explanation || undefined,
          updatedAt: item.updated_at || item.updatedAt || undefined,
          createdAt: item.created_at || item.createdAt || undefined,
        },
      };
    });

    console.log("Transformed questions:", loadedQuestions);
    setQuestions(loadedQuestions);
    
    if (loadedQuestions.length > 0) {
      setCurrentQuestionId(loadedQuestions[0].id);
    } else {
      setCurrentQuestionId(null);
    }
    
    // Update save state with last saved time
    if (loadedQuestions.length > 0) {
      // Find the most recent update time
      const timestamps = loadedQuestions
        .map(q => q.meta?.updatedAt)
        .filter(Boolean)
        .sort();
      
      const lastSaved = timestamps.length > 0 
        ? timestamps[timestamps.length - 1] 
        : null;
      
      setSaveState(prev => ({
        ...prev,
        lastSaved,
        hasUnsavedChanges: false,
      }));
    }

  } catch (error: any) {
    console.error("Failed to load questions:", error);
    setLoadError(error.message || "Failed to load questions from server");
    setQuestions([]);
  } finally {
    setLoading(false);
  }
}, [sessionId]);

const loadSessionCode = useCallback(async () => {
  if (!sessionId) return;

  try {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API.node}/api/session/${sessionId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });

    if (!response.ok) return;
    const result = await response.json();
    const code = result?.data?.join_code;
    if (code) {
      setSessionCode(String(code));
    }
  } catch (error) {
    console.warn("Failed to load session code:", error);
  }
}, [sessionId]);
  // Load questions on component mount
  useEffect(() => {
    loadExistingQuestions();
  }, [loadExistingQuestions]);

  useEffect(() => {
    loadSessionCode();
  }, [loadSessionCode]);

  // Save a single question to the server
  const saveSingleQuestion = useCallback(
    async (question: Question): Promise<boolean> => {
      setSaveState(prev => ({ ...prev, isSaving: true, saveError: null }));

      try {
        const validation = validateQuestionForSave(question);
        if (!validation.valid) {
          throw new Error(validation.message);
        }

        const token = localStorage.getItem("token");
        const formatted = formatQuestionPayload(question);

        const payload = {
          question_text: formatted.question_text,
          question_type: formatted.question_type,
          options: formatted.options,
          order_index: questions.findIndex(q => q.id === question.id),
          image_url: question.meta?.imageUrl ?? null,
          explanation: question.meta?.explanation ?? null,
        };

        console.log("Saving question with payload:", payload);

        const response = await fetch(
          `${API.node}/api/sessions/${sessionId}/questions/${question.id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) {
          const errText = await response.text();
          throw new Error(errText || "Failed to save question");
        }

        // Mark as saved (not draft)
        setQuestions(prev =>
          prev.map(q =>
            q.id === question.id
              ? { 
                  ...q, 
                  meta: { 
                    ...q.meta, 
                    draft: false,
                    updatedAt: new Date().toISOString() 
                  } 
                }
              : q
          )
        );

        setSaveState(prev => ({
          ...prev,
          isSaving: false,
          hasUnsavedChanges: questions.some(q => q.id !== question.id && q.meta?.draft),
          lastSaved: new Date().toISOString(),
          saveError: null,
        }));

        return true;
      } catch (error: any) {
        console.error("Failed to save question:", error);
        setSaveState(prev => ({
          ...prev,
          isSaving: false,
          saveError: error.message || "Save failed",
        }));
        return false;
      }
    },
    [sessionId, questions]
  );

  // Mark question as dirty when changed (but don't auto-save)
  const updateQuestion = useCallback(
    (id: string, patch: Partial<Question>) => {
      setQuestions(prev => {
        const updated = prev.map(q => 
          q.id === id 
            ? { 
                ...q, 
                ...patch, 
                meta: { 
                  ...q.meta, 
                  draft: true,
                  updatedAt: new Date().toISOString() 
                } 
              }
            : q
        );
        
        setSaveState(prevState => ({
          ...prevState,
          hasUnsavedChanges: true,
        }));
        
        return updated;
      });
    },
    []
  );

  // Add option and mark as draft
  const addOption = useCallback((questionId: string) => {
    setQuestions(prev => {
      const updated = prev.map(q => {
        if (q.id !== questionId) return q;
        const opts = [...(q.options || [])];
        opts.push(defaultOption(opts.length + 1));
        return { 
          ...q, 
          options: opts, 
          meta: { 
            ...q.meta, 
            draft: true,
            updatedAt: new Date().toISOString() 
          } 
        };
      });
      
      setSaveState(prevState => ({
        ...prevState,
        hasUnsavedChanges: true,
      }));
      
      return updated;
    });
  }, []);

  // Update option and mark as draft
  const updateOption = useCallback(
    (questionId: string, idx: number, value: string) => {
      setQuestions(prev => {
        const updated = prev.map(q => {
          if (q.id !== questionId) return q;
          const opts = [...(q.options || [])];
          opts[idx] = value;
          return { 
            ...q, 
            options: opts, 
            meta: { 
              ...q.meta, 
              draft: true,
              updatedAt: new Date().toISOString() 
            } 
          };
        });
        
        setSaveState(prevState => ({
          ...prevState,
          hasUnsavedChanges: true,
        }));
        
        return updated;
      });
    },
    []
  );

  // Remove option and mark as draft
  const removeOption = useCallback(
    (questionId: string, idx: number) => {
      setQuestions(prev => {
        const updated = prev.map(q => {
          if (q.id !== questionId) return q;
          const opts = (q.options || []).filter((_, i) => i !== idx);
          let correctAnswer = q.correctAnswer;
          if (correctAnswer != null && correctAnswer >= idx) {
            correctAnswer = correctAnswer > idx ? correctAnswer - 1 : null;
          }
          const multiAnswers = (q.multiAnswers || [])
            .filter(i => i !== idx)
            .map(i => (i > idx ? i - 1 : i));
          return { 
            ...q, 
            options: opts, 
            correctAnswer, 
            multiAnswers, 
            meta: { 
              ...q.meta, 
              draft: true,
              updatedAt: new Date().toISOString() 
            } 
          };
        });
        
        setSaveState(prevState => ({
          ...prevState,
          hasUnsavedChanges: true,
        }));
        
        return updated;
      });
    },
    []
  );

  // Add new question
  const addQuestion = useCallback(
    async (type: QType = "quiz") => {
      if (loading) {
        console.warn("Still loading existing questions, please wait");
        return;
      }

      const tempId = uid();
      const newQuestion: Question = {
        id: tempId,
        text: "",
        type,
        options: type === "quiz" || type === "multi"
          ? [defaultOption(1), defaultOption(2)]
          : undefined,
        ratingMax: type === "rating" ? 5 : undefined,
        ratingMin: type === "rating" ? 1 : undefined,
        ratingLabels: type === "rating" ? ["Low", "High"] : undefined,
        correctAnswer: type === "quiz" ? 0 : undefined,
        multiAnswers: type === "multi" ? [0] : undefined,
        meta: { 
          draft: true,
          createdAt: new Date().toISOString() 
        },
      };

      setQuestions(prev => [...prev, newQuestion]);
      setCurrentQuestionId(tempId);
      setSaveState(prev => ({ ...prev, hasUnsavedChanges: true }));

      try {
        const token = localStorage.getItem("token");
        const formatted = formatQuestionPayload({
          ...newQuestion,
          text: "Untitled Question",
        });

        const payload = {
          question_text: formatted.question_text,
          question_type: formatted.question_type,
          options: formatted.options,
          order_index: questions.length,
          image_url: null,
          explanation: null,
        };

        const response = await fetch(
          `${API.node}/api/sessions/${sessionId}/questions`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
          }
        );

        if (response.ok) {
          const data = await response.json();
          const realId = data.data?.id || data.id || data.question_id;
          if (realId) {
            setQuestions(prev =>
              prev.map(q => 
                q.id === tempId 
                  ? { 
                      ...q, 
                      id: realId,
                      meta: { ...q.meta, draft: false }
                    } 
                  : q
              )
            );
            setCurrentQuestionId(realId);
          }
        }
      } catch (err) {
        console.error("Failed to create question:", err);
      }
    },
    [sessionId, questions.length, loading]
  );

  // Next Question: Save current question first, then add new
  const handleNextQuestion = useCallback(async () => {
    if (loading) return;

    if (!currentQuestionId) {
      await addQuestion("quiz");
      return;
    }

    const currentQuestion = questions.find(q => q.id === currentQuestionId);
    if (!currentQuestion) {
      await addQuestion("quiz");
      return;
    }

    // Only save if it's a draft (has unsaved changes)
    if (currentQuestion.meta?.draft) {
      const saved = await saveSingleQuestion(currentQuestion);
      if (!saved) {
        // Don't proceed if save failed
        return;
      }
    }

    // Add new question and set it as current
    await addQuestion("quiz");
  }, [currentQuestionId, questions, addQuestion, saveSingleQuestion, loading]);

  const deleteQuestion = useCallback(
    async (questionId: string) => {
      const target = questions.find((q) => q.id === questionId);
      if (!target) return;

      const confirmed = window.confirm("Delete this question? This cannot be undone.");
      if (!confirmed) return;

      const isTempQuestion = questionId.startsWith("q_");

      try {
        if (!isTempQuestion) {
          const token = localStorage.getItem("token");
          const response = await fetch(
            `${API.node}/api/sessions/${sessionId}/questions/${questionId}`,
            {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            }
          );

          if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || "Failed to delete question");
          }
        }

        setQuestions((prev) => {
          const next = prev.filter((q) => q.id !== questionId);
          return next;
        });

        setCurrentQuestionId((current) => {
          if (current !== questionId) return current;
          const remaining = questions.filter((q) => q.id !== questionId);
          return remaining[0]?.id || null;
        });

        setSaveState((prev) => ({
          ...prev,
          hasUnsavedChanges: questions
            .filter((q) => q.id !== questionId)
            .some((q) => !!q.meta?.draft),
        }));
      } catch (error: any) {
        console.error("Failed to delete question:", error);
        setSaveState((prev) => ({
          ...prev,
          saveError: error.message || "Delete failed",
        }));
      }
    },
    [questions, sessionId]
  );

  const onDropChangeType = useCallback(
    (e: React.DragEvent, questionId: string) => {
      e.preventDefault();
      const type = e.dataTransfer.getData("application/qtype") as QType;
      if (!type) return;

      const updates: Partial<Question> = { type };
      if (type === "quiz") {
        updates.options = [defaultOption(1), defaultOption(2)];
        updates.correctAnswer = 0;
        updates.multiAnswers = undefined;
        updates.ratingMin = undefined;
        updates.ratingMax = undefined;
        updates.ratingLabels = undefined;
      } else if (type === "multi") {
        updates.options = [defaultOption(1), defaultOption(2)];
        updates.correctAnswer = undefined;
        updates.multiAnswers = [0];
        updates.ratingMin = undefined;
        updates.ratingMax = undefined;
        updates.ratingLabels = undefined;
      } else if (type === "rating") {
        updates.options = undefined;
        updates.correctAnswer = undefined;
        updates.multiAnswers = undefined;
        updates.ratingMin = 1;
        updates.ratingMax = 5;
        updates.ratingLabels = ["Low", "High"];
      } else if (type === "open") {
        updates.options = undefined;
        updates.correctAnswer = undefined;
        updates.multiAnswers = undefined;
        updates.ratingMin = undefined;
        updates.ratingMax = undefined;
        updates.ratingLabels = undefined;
      }

      updateQuestion(questionId, updates);
    },
    [updateQuestion]
  );

  const onDragOver = (e: React.DragEvent) => e.preventDefault();

  const handlePreview = useCallback(() => {
    onPreview?.(questions);
    setPreviewOpen(true);
  }, [questions, onPreview]);

  const filteredQuestions = useMemo(
    () =>
      questions.filter((q) =>
        filter === "all"
          ? true
          : filter === "drafts"
          ? !!q.meta?.draft
          : q.type === filter
      ),
    [questions, filter]
  );

  const unsavedCount = useMemo(
    () => questions.filter(q => q.meta?.draft).length,
    [questions]
  );

  // Update current question when question list changes
  useEffect(() => {
    if (questions.length > 0 && !currentQuestionId && !loading) {
      setCurrentQuestionId(questions[0].id);
    }
  }, [questions, currentQuestionId, loading]);

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-2 border-slate-400 border-t-transparent"></div>
          <p className="mt-4 text-slate-600">Loading questions...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (loadError) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="max-w-md rounded-2xl border border-slate-200 bg-white p-6 text-center shadow-sm">
          <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto">
            <AlertCircle className="w-6 h-6 text-red-600" />
          </div>
          <h3 className="mt-4 text-lg font-semibold text-gray-900">Failed to load questions</h3>
          <p className="mt-2 text-gray-600">{loadError}</p>
          <div className="flex gap-3 mt-4">
            <button
              onClick={loadExistingQuestions}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium"
            >
              Retry
            </button>
            <button
              onClick={handleBackClick}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium"
            >
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="sticky top-0 z-40 border-b border-slate-200 bg-slate-50/95 backdrop-blur">
        <div className="mx-auto max-w-7xl px-6 py-4">
          <div className="mb-2 flex items-center gap-4">
            {/* Back Button */}
            <button
              onClick={handleBackClick}
              className="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3.5 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-100"
            >
              <ArrowLeft className="w-5 h-5" />
              <span className="font-medium">Back</span>
            </button>
            
            {/* Header Content */}
            <div className="flex-1">
              <QuestionHeader
                onPreview={handlePreview}
                saving={saveState.isSaving}
                questionsCount={questions.length}
                unsavedCount={unsavedCount}
                lastSaved={saveState.lastSaved}
                autoSaveEnabled={saveState.autoSaveEnabled}
                hasUnsavedChanges={saveState.hasUnsavedChanges}
                saveError={saveState.saveError}
                sessionCode={sessionCode ?? undefined}
                sessionId={sessionId}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto mt-4 max-w-7xl px-6">
        <div className="rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
          <div className="flex flex-wrap gap-2">
            {(["all", "quiz", "multi", "rating", "open", "drafts"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`rounded-md px-3.5 py-1.5 text-sm font-medium transition ${
                  filter === f
                    ? "bg-slate-900 text-white"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                {f.charAt(0).toUpperCase() + f.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="mx-auto mt-6 max-w-7xl px-6">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[280px_1fr]">
          <aside className="sticky top-32 self-start">
            <QuestionPalette
              isOpen={paletteOpen}
              onToggle={() => setPaletteOpen(!paletteOpen)}
              onDragStart={(e, t) => e.dataTransfer.setData("application/qtype", t)}
              onAddQuestion={addQuestion}
            />
          </aside>

          <main className="space-y-4">
            {filteredQuestions.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
                <h3 className="text-lg font-semibold">No questions</h3>
                <p className="mt-2 text-slate-500">Add one from the palette</p>
                <button
                  onClick={handleBackClick}
                  className="mt-4 rounded-lg border border-slate-300 px-4 py-2 font-medium hover:bg-slate-50"
                >
                  Go Back
                </button>
              </div>
            ) : (
              filteredQuestions.map((q, idx) => (
                <div 
                  key={q.id} 
                  data-question-id={q.id}
                  onClick={() => setCurrentQuestionId(q.id)}
                  className={currentQuestionId === q.id ? 'rounded-2xl ring-2 ring-slate-300' : ''}
                >
                  <QuestionEditor
                    question={q}
                    index={idx}
                    onUpdate={updateQuestion}
                    onAddOption={addOption}
                    onUpdateOption={updateOption}
                    onRemoveOption={removeOption}
                    onDragOver={onDragOver}
                    onDropChangeType={onDropChangeType}
                    onNextQuestion={handleNextQuestion}
                    onDeleteQuestion={deleteQuestion}
                    isSaving={saveState.isSaving && currentQuestionId === q.id}
                    isDraft={!!q.meta?.draft}
                  />
                </div>
              ))
            )}

            {filter === "all" && (
              <button
                onClick={() => addQuestion("quiz")}
                className="hidden w-full rounded-2xl border-2 border-dashed border-slate-300 py-5 font-medium text-slate-600 transition hover:bg-white lg:block"
              >
                + Add Question
              </button>
            )}
          </main>
        </div>
      </div>

      <QuestionPreview
        isOpen={previewOpen}
        questions={questions}
        onClose={() => setPreviewOpen(false)}
      />
    </div>
  );
};

export default QuestionBuilderPage;
