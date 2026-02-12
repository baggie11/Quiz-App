import React, { useState } from "react";
import type { Question } from "../../types";
import {
  ArrowRight,
  Check,
  CheckCircle,
  Circle,
  ClipboardList,
  MessageSquare,
  Plus,
  Star,
  Trash2,
  Type,
} from "lucide-react";

interface QuestionEditorProps {
  question: Question;
  index: number;
  onUpdate: (id: string, patch: Partial<Question>) => void;
  onAddOption: (questionId: string) => void;
  onUpdateOption: (questionId: string, idx: number, value: string) => void;
  onRemoveOption: (questionId: string, idx: number) => void;
  onDragOver: (e: React.DragEvent) => void;
  onDropChangeType: (e: React.DragEvent, questionId: string) => void;
  onNextQuestion?: () => void;
  onDeleteQuestion?: (questionId: string) => void;
  isSaving?: boolean;
  isDraft?: boolean;
}

export const QuestionEditor: React.FC<QuestionEditorProps> = ({
  question,
  index,
  onUpdate,
  onAddOption,
  onUpdateOption,
  onRemoveOption,
  onDragOver,
  onDropChangeType,
  onNextQuestion,
  onDeleteQuestion,
  isSaving = false,
  isDraft = false,
}) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const getQuestionTypeIcon = (type: string) => {
    switch (type) {
      case "quiz":
        return <ClipboardList className="h-4 w-4" />;
      case "multi":
        return <CheckCircle className="h-4 w-4" />;
      case "rating":
        return <Star className="h-4 w-4" />;
      case "open":
        return <MessageSquare className="h-4 w-4" />;
      default:
        return <Type className="h-4 w-4" />;
    }
  };

  const getQuestionTypeLabel = (type: string) => {
    switch (type) {
      case "quiz":
        return "Single Choice";
      case "multi":
        return "MCQ";
      case "rating":
        return "Rating";
      case "open":
        return "Open Text";
      default:
        return type;
    }
  };

  const toggleCorrect = (optionIndex: number) => {
    if (question.type === "quiz") {
      onUpdate(question.id, {
        correctAnswer: question.correctAnswer === optionIndex ? null : optionIndex,
      });
    } else if (question.type === "multi") {
      const current = question.multiAnswers ?? [];
      const updated = current.includes(optionIndex)
        ? current.filter((i) => i !== optionIndex)
        : [...current, optionIndex];
      onUpdate(question.id, { multiAnswers: updated });
    }
  };

  const isCorrect = (idx: number): boolean => {
    if (question.type === "quiz") return question.correctAnswer === idx;
    if (question.type === "multi") return (question.multiAnswers ?? []).includes(idx);
    return false;
  };

  const options = question.options ?? [];

  return (
    <div
      className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
      onDragOver={onDragOver}
      onDrop={(e) => onDropChangeType(e, question.id)}
    >
      <div
        className="flex cursor-pointer items-center justify-between border-b border-slate-100 px-5 py-4 hover:bg-slate-50"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-sm font-semibold text-slate-700">
            {index + 1}
          </div>

          <div>
            <div className="mb-1.5 flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-xs font-medium text-slate-700">
                {getQuestionTypeIcon(question.type)}
                {getQuestionTypeLabel(question.type)}
              </span>
              {question.meta?.required && (
                <span className="rounded-full bg-rose-100 px-2.5 py-1 text-xs font-medium text-rose-700">
                  Required
                </span>
              )}
              {isDraft && (
                <span className="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-medium text-amber-700">
                  Draft
                </span>
              )}
              {isSaving && !isDraft && (
                <span className="rounded-full bg-blue-100 px-2.5 py-1 text-xs font-medium text-blue-700">
                  Saving
                </span>
              )}
            </div>

            <h3 className="text-base font-semibold text-slate-900">
              {question.text?.trim() || <span className="italic text-slate-400">Untitled question...</span>}
            </h3>
          </div>
        </div>

        <div className="text-sm font-semibold text-slate-400">{isExpanded ? "v" : ">"}</div>
      </div>

      {isExpanded && (
        <div className="px-5 pb-6">
          <div className="mt-5">
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Question Text <span className="text-red-500">*</span>
            </label>
            <textarea
              rows={3}
              value={question.text || ""}
              onChange={(e) => onUpdate(question.id, { text: e.target.value })}
              placeholder="Enter your question here..."
              className={`w-full resize-none rounded-xl border px-4 py-3 focus:border-slate-400 focus:outline-none ${
                !question.text?.trim() ? "border-amber-300 bg-amber-50" : "border-slate-300 bg-white"
              }`}
            />
          </div>

          {(question.type === "quiz" || question.type === "multi") && (
            <div className="mt-5 space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium text-slate-700">Answer Options</label>
                <button
                  onClick={() => onAddOption(question.id)}
                  disabled={options.length >= 10}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50"
                >
                  <Plus className="h-4 w-4" />
                  Add Option
                </button>
              </div>

              <div className="space-y-3">
                {options.map((option, idx) => (
                  <div key={idx} className="group flex items-center gap-3">
                    <button
                      onClick={() => toggleCorrect(idx)}
                      className={`flex h-10 w-10 items-center justify-center rounded-lg border ${
                        isCorrect(idx)
                          ? question.type === "quiz"
                            ? "border-emerald-500 bg-emerald-500 text-white"
                            : "border-indigo-600 bg-indigo-600 text-white"
                          : "border-slate-300 bg-white text-slate-500 hover:bg-slate-100"
                      }`}
                    >
                      {question.type === "quiz" ? (
                        isCorrect(idx) ? (
                          "•"
                        ) : (
                          <Circle className="h-5 w-5" />
                        )
                      ) : isCorrect(idx) ? (
                        <Check className="h-5 w-5" />
                      ) : (
                        <div className="h-5 w-5 rounded border-2 border-slate-400" />
                      )}
                    </button>

                    <input
                      type="text"
                      value={option}
                      onChange={(e) => onUpdateOption(question.id, idx, e.target.value)}
                      placeholder={`Option ${idx + 1}`}
                      className={`flex-1 rounded-lg border px-4 py-3 focus:border-slate-400 focus:outline-none ${
                        !option?.trim() ? "border-amber-300 bg-amber-50" : "border-slate-300 bg-white"
                      }`}
                    />

                    {options.length > 2 && (
                      <button
                        onClick={() => onRemoveOption(question.id, idx)}
                        className="rounded-lg p-2 text-slate-400 opacity-0 transition group-hover:opacity-100 hover:bg-red-50 hover:text-red-600"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {question.type === "rating" && (
            <div className="mt-5 space-y-5">
              <label className="block text-sm font-medium text-slate-700">Rating Scale</label>
              <div className="flex items-center justify-center gap-6">
                <input
                  type="number"
                  min="1"
                  max="9"
                  value={question.ratingMin || 1}
                  onChange={(e) => {
                    const nextMin = Math.max(1, Math.min(9, parseInt(e.target.value) || 1));
                    const nextMax = Math.max(nextMin + 1, question.ratingMax || 5);
                    onUpdate(question.id, { ratingMin: nextMin, ratingMax: nextMax });
                  }}
                  className="w-20 rounded-xl border border-slate-300 px-4 py-3 text-center text-lg font-medium focus:border-slate-400 focus:outline-none"
                />
                <input
                  type="number"
                  min="2"
                  max="10"
                  value={question.ratingMax || 5}
                  onChange={(e) => {
                    const min = question.ratingMin || 1;
                    const nextMax = Math.max(min + 1, Math.min(10, parseInt(e.target.value) || 5));
                    onUpdate(question.id, { ratingMax: nextMax });
                  }}
                  className="w-20 rounded-xl border border-slate-300 px-4 py-3 text-center text-lg font-medium focus:border-slate-400 focus:outline-none"
                />
                <span className="text-slate-500">Min / Max</span>
              </div>
            </div>
          )}

          {question.type === "open" && (
            <div className="mt-5">
              <label className="mb-2 block text-sm font-medium text-slate-700">
                Model Answer <span className="text-slate-500">(Optional)</span>
              </label>
              <textarea
                rows={5}
                value={question.modelAnswer || ""}
                onChange={(e) => onUpdate(question.id, { modelAnswer: e.target.value })}
                placeholder="Optional expected answer for reference..."
                className="w-full resize-none rounded-xl border border-slate-300 p-4 focus:border-slate-400 focus:outline-none"
              />
            </div>
          )}

          <div className="mt-8 flex items-center justify-between">
            <button
              onClick={() => onDeleteQuestion?.(question.id)}
              className="inline-flex items-center gap-2 rounded-lg border border-red-200 px-4 py-2.5 text-sm font-medium text-red-700 hover:bg-red-50"
            >
              <Trash2 className="h-4 w-4" />
              Delete Question
            </button>

            <button
              onClick={onNextQuestion}
              disabled={isSaving}
              className={`inline-flex items-center gap-2 rounded-lg px-5 py-2.5 text-sm font-medium ${
                isSaving ? "cursor-not-allowed bg-slate-200 text-slate-500" : "bg-slate-900 text-white hover:bg-slate-800"
              }`}
            >
              {isSaving ? "Saving current question..." : "Next Question"}
              {!isSaving && <ArrowRight className="h-4 w-4" />}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuestionEditor;
