import React, { useState, type ChangeEvent, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar as CalendarIcon, Tag } from 'lucide-react';
import { type Session } from '../../types';

interface CreateSessionFormProps {
  addSession?: (newSession: Session) => void;
  redirectToBuilder?: boolean; // New prop to control redirect behavior
}

const CreateSessionForm: React.FC<CreateSessionFormProps> = ({ 
  addSession, 
  redirectToBuilder = true // Default to redirect
}) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    sessionName: '',
    quizTopic: '',
    duration: '',
    maxParticipants: '',
    passmark: '',
    startDate: '',
    startTime: '',
    endDate: '',
    endTime: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear errors when user changes input
    if (error) {
      setError(null);
    }
  };

  const validateForm = (): boolean => {
    // Validate session name
    if (!formData.sessionName.trim()) {
      setError("Session name is required");
      return false;
    }

    // Validate quiz topic
    if (!formData.quizTopic.trim()) {
      setError("Quiz topic is required");
      return false;
    }

    // Validate dates
    if (!formData.startDate) {
      setError("Start date is required");
      return false;
    }

    if (!formData.endDate) {
      setError("End date is required");
      return false;
    }

    const startDate = new Date(formData.startDate);
    const endDate = new Date(formData.endDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Check if start date is valid
    if (startDate < today) {
      setError("Start date cannot be in the past");
      return false;
    }

    // Check if end date is after start date
    if (endDate < startDate) {
      setError("End date cannot be before start date");
      return false;
    }

    // Validate duration
    if (!formData.duration) {
      setError("Test duration is required");
      return false;
    }

    const duration = parseInt(formData.duration);
    if (isNaN(duration) || duration <= 0) {
      setError("Duration must be a positive number");
      return false;
    }

    if (duration > 1440) { // 24 hours in minutes
      setError("Duration cannot exceed 24 hours (1440 minutes)");
      return false;
    }

    // Validate max participants
    if (!formData.maxParticipants) {
      setError("Max participants is required");
      return false;
    }

    const maxParticipants = parseInt(formData.maxParticipants);
    if (isNaN(maxParticipants) || maxParticipants <= 0) {
      setError("Max participants must be a positive number");
      return false;
    }

    // Validate passmark
    if (!formData.passmark) {
      setError("Pass mark is required");
      return false;
    }

    const passmark = parseInt(formData.passmark);
    if (isNaN(passmark) || passmark < 0 || passmark > 100) {
      setError("Pass mark must be between 0 and 100");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!validateForm()) {
      return;
    }

    try {
      setLoading(true);
      const token = localStorage.getItem('token');

      // Format dates with times
      const startDateTime = new Date(formData.startDate);
      const [startHours, startMinutes] = (formData.startTime || '00:00').split(':');
      startDateTime.setHours(parseInt(startHours), parseInt(startMinutes), 0, 0);
      
      const endDateTime = new Date(formData.endDate);
      const [endHours, endMinutes] = (formData.endTime || '23:59').split(':');
      endDateTime.setHours(parseInt(endHours), parseInt(endMinutes), 59, 999);

      const payload = {
        title: formData.sessionName.trim(),
        quiz_topic: formData.quizTopic.trim(),
        start_date: startDateTime.toISOString(),
        end_date: endDateTime.toISOString(),
        duration: parseInt(formData.duration),
        max_participants: parseInt(formData.maxParticipants),
        pass_mark: parseInt(formData.passmark),
        draft: false,
      };

      const response = await fetch(`http://localhost:3000/api/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok && data.status === "ok") {
        const newSession = { ...data.data, draft: false };
        
        setSuccess("Session created successfully! Redirecting to question builder...");
        
        if (addSession) {
          addSession(newSession);
        }

        localStorage.setItem('currentSessionId', data.data?.id);
        
        if (redirectToBuilder && data.data?.id) {
          setTimeout(() => {
            navigate(`/session/${data.data.id}/questions`);
          }, 1500);
        } else {
          setTimeout(() => {
            setFormData({
              sessionName: '',
              quizTopic: '',
              duration: '',
              maxParticipants: '',
              passmark: '',
              startDate: '',
              startTime: '',
              endDate: '',
              endTime: '',
            });
            setSuccess(null);
          }, 2000);
        }
      } else {
        setError(data.message || "Failed to create session");
      }
    } catch (err: any) {
      setError(err.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  // Calculate min/max dates for inputs
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Create New Quiz Session</h1>
        <p className="text-gray-600">Set up a new quiz session with timing, duration, and settings</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg border border-gray-200 p-8 space-y-8">
        {/* Session Details Section */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
              <Tag className="text-blue-600" size={16} />
            </div>
            Session Details
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Session Name */}
            <div>
              <label htmlFor="sessionName" className="block text-sm font-semibold text-gray-900 mb-3">
                Session Name *
              </label>
              <input
                type="text"
                id="sessionName"
                name="sessionName"
                value={formData.sessionName}
                onChange={handleChange}
                placeholder="Introduction to Calculus"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Quiz Topic */}
            <div>
              <label htmlFor="quizTopic" className="block text-sm font-semibold text-gray-900 mb-3">
                Quiz Topic *
              </label>
              <input
                type="text"
                id="quizTopic"
                name="quizTopic"
                value={formData.quizTopic}
                onChange={handleChange}
                placeholder="Mathematics"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Duration */}
            <div>
              <label htmlFor="duration" className="block text-sm font-semibold text-gray-900 mb-3">
                Duration (minutes) *
              </label>
              <input
                type="number"
                id="duration"
                name="duration"
                value={formData.duration}
                onChange={handleChange}
                placeholder="60"
                min="1"
                max="1440"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Max Participants */}
            <div>
              <label htmlFor="maxParticipants" className="block text-sm font-semibold text-gray-900 mb-3">
                Max Participants *
              </label>
              <input
                type="number"
                id="maxParticipants"
                name="maxParticipants"
                value={formData.maxParticipants}
                onChange={handleChange}
                placeholder="50"
                min="1"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Pass Mark */}
            <div>
              <label htmlFor="passmark" className="block text-sm font-semibold text-gray-900 mb-3">
                Pass Mark (%) *
              </label>
              <input
                type="number"
                id="passmark"
                name="passmark"
                value={formData.passmark}
                onChange={handleChange}
                placeholder="70"
                min="0"
                max="100"
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>
        </div>

        {/* Timing Details Section */}
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
              <CalendarIcon className="text-blue-600" size={16} />
            </div>
            Timing Details
          </h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Start Date */}
            <div>
              <label htmlFor="startDate" className="block text-sm font-semibold text-gray-900 mb-3">
                Start Date *
              </label>
              <input
                type="date"
                id="startDate"
                name="startDate"
                value={formData.startDate}
                onChange={handleChange}
                min={today}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Start Time */}
            <div>
              <label htmlFor="startTime" className="block text-sm font-semibold text-gray-900 mb-3">
                Start Time *
              </label>
              <input
                type="time"
                id="startTime"
                name="startTime"
                value={formData.startTime}
                onChange={handleChange}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* End Date */}
            <div>
              <label htmlFor="endDate" className="block text-sm font-semibold text-gray-900 mb-3">
                End Date *
              </label>
              <input
                type="date"
                id="endDate"
                name="endDate"
                value={formData.endDate}
                onChange={handleChange}
                min={formData.startDate || today}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* End Time */}
            <div>
              <label htmlFor="endTime" className="block text-sm font-semibold text-gray-900 mb-3">
                End Time *
              </label>
              <input
                type="time"
                id="endTime"
                name="endTime"
                value={formData.endTime}
                onChange={handleChange}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>
        </div>

        {/* Session Join Code */}
        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-3">
            Session Join Code
          </label>
          <input
            type="text"
            value="Generated after creation"
            disabled
            className="w-full px-4 py-2.5 border border-gray-300 rounded-lg text-sm bg-gray-50 text-gray-500 cursor-not-allowed"
          />
        </div>

        {/* Error and Success Messages */}
        {(error || success) && (
          <div className={`p-4 rounded-lg border ${error ? 'bg-red-50 border-red-200 text-red-700' : 'bg-green-50 border-green-200 text-green-700'}`}>
            {error || success}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 px-6 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-all disabled:opacity-50"
          >
            {loading ? 'Creating...' : 'Create Session'}
          </button>
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="flex-1 px-6 py-2.5 bg-white text-blue-600 font-medium rounded-lg border border-blue-600 hover:bg-blue-50 transition-all"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateSessionForm;