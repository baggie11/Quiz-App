import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CalendarClock, CheckCircle2, Radio } from "lucide-react";
import { type Session } from "../../types";
import SessionCard from "./SessionCard";
import LoadingSpinner from "../Shared/LoadingSpinner";
import { API } from "../../api/config";

interface AllSessionsPageProps {
  sessions: Session[];
  setSessions: React.Dispatch<React.SetStateAction<Session[]>>;
}

type StatusId = "all" | "draft" | "upcoming" | "livenow" | "completed" | "notscheduled";

const FILTERS: ReadonlyArray<{ id: StatusId; label: string }> = [
  { id: "all", label: "All" },
  { id: "draft", label: "Drafts" },
  { id: "upcoming", label: "Upcoming" },
  { id: "livenow", label: "Live Now" },
  { id: "completed", label: "Completed" },
  { id: "notscheduled", label: "Not Scheduled" },
];

const AllSessionsPage: React.FC<AllSessionsPageProps> = ({ sessions, setSessions }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<StatusId>("all");

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`${API.node}/api/session`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const json = await response.json();

        if (response.ok && json.success) {
          setSessions(json.sessions);
        } else {
          console.error("Failed to fetch sessions:", json.message);
        }
      } catch (err) {
        console.error("Error fetching sessions:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSessions();
  }, [setSessions]);

  const getSessionStatus = (session: Session) => {
    const now = new Date();
    const start = session.start_date ? new Date(session.start_date) : null;
    const end = session.end_date ? new Date(session.end_date) : null;

    if (session.draft) {
      return { text: "Draft", color: "bg-slate-100 text-slate-700", icon: "" };
    }
    if (!start) {
      return { text: "Not Scheduled", color: "bg-zinc-100 text-zinc-700", icon: "" };
    }
    if (end && now > end) {
      return { text: "Completed", color: "bg-emerald-100 text-emerald-700", icon: "" };
    }
    if (now >= start && (!end || now <= end)) {
      return { text: "Live Now", color: "bg-rose-100 text-rose-700", icon: "" };
    }
    if (now < start) {
      return { text: "Upcoming", color: "bg-amber-100 text-amber-700", icon: "" };
    }
    return { text: "Active", color: "bg-indigo-100 text-indigo-700", icon: "" };
  };

  const filteredSessions = sessions.filter((session) => {
    if (filterStatus === "all") return true;
    const status = getSessionStatus(session);
    return status.text.toLowerCase().replace(" ", "") === filterStatus;
  });

  const liveCount = sessions.filter((s) => getSessionStatus(s).text === "Live Now").length;
  const upcomingCount = sessions.filter((s) => getSessionStatus(s).text === "Upcoming").length;
  const completedCount = sessions.filter((s) => getSessionStatus(s).text === "Completed").length;

  const handleSessionClick = (sessionId: string) => {
    navigate(`/session/${sessionId}/questions`);
  };

  const handleDeleteSession = async (sessionId: string) => {
    const confirmed = window.confirm("Delete this session? This will remove its questions and participants.");
    if (!confirmed) return;

    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`${API.node}/api/session/${sessionId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (!response.ok || !data.success) {
        throw new Error(data.message || "Failed to delete session");
      }

      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
    } catch (error) {
      console.error("Delete session error:", error);
      alert("Failed to delete session. Please try again.");
    }
  };

  if (loading) return <LoadingSpinner message="Loading sessions..." />;

  if (!sessions.length) {
    return (
      <div className="mx-auto w-full max-w-7xl px-6 py-10">
        <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-16 text-center dark:border-slate-700 dark:bg-slate-900">
          <h2 className="text-xl font-semibold text-slate-900 dark:text-slate-100">No sessions yet</h2>
          <p className="mt-2 text-slate-500 dark:text-slate-400">Create your first session to get started.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-7xl px-6 py-8">
      <div className="mb-8">
        <div className="mb-5 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight text-slate-900 dark:text-slate-100">All Sessions</h1>
            <p className="mt-1 text-slate-500 dark:text-slate-400">
              {filteredSessions.length} visible of {sessions.length} total
            </p>
          </div>
        </div>

        <div className="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div className="rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm dark:border-slate-700 dark:bg-slate-900">
            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
              <Radio className="h-4 w-4 text-rose-600 dark:text-rose-300" />
              Live
            </div>
            <p className="mt-1 text-2xl font-semibold text-slate-900 dark:text-slate-100">{liveCount}</p>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm dark:border-slate-700 dark:bg-slate-900">
            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
              <CalendarClock className="h-4 w-4 text-amber-600 dark:text-amber-300" />
              Upcoming
            </div>
            <p className="mt-1 text-2xl font-semibold text-slate-900 dark:text-slate-100">{upcomingCount}</p>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm dark:border-slate-700 dark:bg-slate-900">
            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
              <CheckCircle2 className="h-4 w-4 text-emerald-600 dark:text-emerald-300" />
              Completed
            </div>
            <p className="mt-1 text-2xl font-semibold text-slate-900 dark:text-slate-100">{completedCount}</p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {FILTERS.map((status) => (
            <button
              key={status.id}
              onClick={() => setFilterStatus(status.id)}
              className={`rounded-full px-3.5 py-1.5 text-sm font-medium transition ${
                filterStatus === status.id
                  ? "bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
              }`}
            >
              {status.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        {filteredSessions.map((session) => (
          <div key={session.id} onClick={() => handleSessionClick(session.id)} className="cursor-pointer">
            <SessionCard
              session={session}
              onDelete={handleDeleteSession}
              getSessionStatus={getSessionStatus}
            />
          </div>
        ))}
      </div>

      {filteredSessions.length === 0 && sessions.length > 0 && (
        <div className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-white py-12 text-center dark:border-slate-700 dark:bg-slate-900">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
            <svg className="h-8 w-8 text-slate-400 dark:text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="mb-2 text-lg font-semibold text-slate-900 dark:text-slate-100">No sessions match this filter</h3>
          <p className="text-slate-500 dark:text-slate-400">Try selecting a different status.</p>
          <button
            onClick={() => setFilterStatus("all")}
            className="mt-4 rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            Clear filter
          </button>
        </div>
      )}
    </div>
  );
};

export default AllSessionsPage;
