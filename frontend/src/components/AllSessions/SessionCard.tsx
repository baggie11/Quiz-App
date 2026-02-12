import React from "react";
import { ArrowRight, Calendar, Edit3, Trash2 } from "lucide-react";
import { type Session } from "../../types";

interface SessionCardProps {
  session: Session;
  onDelete: (sessionId: string) => void;
  getSessionStatus: (session: Session) => {
    text: string;
    color: string;
    icon: string;
  };
}

const SessionCard: React.FC<SessionCardProps> = ({ session, onDelete, getSessionStatus }) => {
  const status = getSessionStatus(session);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <article className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md dark:border-slate-700 dark:bg-slate-900 dark:hover:border-slate-500">
      <header className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h3 className="line-clamp-2 text-lg font-semibold text-slate-900 transition group-hover:text-slate-700 dark:text-slate-100 dark:group-hover:text-slate-200">
            {session.title || "Untitled Session"}
          </h3>
          <div className={`mt-2 inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${status.color}`}>
            {status.text}
          </div>
        </div>
        <ArrowRight className="mt-1 h-4 w-4 text-slate-500 transition group-hover:translate-x-0.5 group-hover:text-slate-700 dark:text-slate-300 dark:group-hover:text-slate-100" />
      </header>

      <div className="space-y-2.5">
        {session.start_date && (
          <div className="flex items-center text-sm text-slate-600 dark:text-slate-300">
            <Calendar className="mr-2 h-4 w-4 text-slate-500 dark:text-slate-300" />
            <span className="mr-1 font-medium text-slate-700 dark:text-slate-200">Starts:</span>
            <span>{formatDate(session.start_date)}</span>
          </div>
        )}
        {session.end_date && (
          <div className="flex items-center text-sm text-slate-600 dark:text-slate-300">
            <Calendar className="mr-2 h-4 w-4 text-slate-500 dark:text-slate-300" />
            <span className="mr-1 font-medium text-slate-700 dark:text-slate-200">Ends:</span>
            <span>{formatDate(session.end_date)}</span>
          </div>
        )}
      </div>

      <footer className="mt-5 flex items-center justify-between border-t border-slate-100 pt-4 dark:border-slate-700">
        <div className="text-xs text-slate-500 dark:text-slate-400">
          Session Code{" "}
          <span className="font-mono text-slate-700 dark:text-slate-200">
            {session.join_code || `${session.id.substring(0, 8)}...`}
          </span>
        </div>
        <div className="inline-flex items-center gap-1 text-sm font-medium text-slate-600 dark:text-slate-300">
          <Edit3 className="h-4 w-4 dark:text-slate-200" />
          Edit Questions
        </div>
      </footer>

      <div className="mt-3">
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(session.id);
          }}
          className="inline-flex items-center gap-1.5 rounded-lg border border-red-200 px-3 py-1.5 text-xs font-medium text-red-700 hover:bg-red-50 dark:border-red-400/40 dark:bg-red-950/20 dark:text-red-300 dark:hover:bg-red-950/40"
        >
          <Trash2 className="h-3.5 w-3.5 dark:text-red-300" />
          Delete Session
        </button>
      </div>
    </article>
  );
};

export default SessionCard;
