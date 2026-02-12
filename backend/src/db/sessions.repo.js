import {supabase} from './index.js';
import {generateUniqueJoinCode} from '../utils/joinCode.js'; 

/**
 * Get session by join code
 * @param {string} joinCode
 * @returns {Promise<Object>} session object
 */

export async function getSessionByJoinCode(joinCode){
    const {data,error} = await supabase
    .from('sessions')
    .select('*')
    .eq('join_code',joinCode)
    .maybeSingle();

    if (error) throw new Error(error.message);
    return data;
}

/** Get session by ID
 * @param {string} sessionId
 * @returns {Promise<Object>} session object
 */

export async function getSessionById(sessionId){
    const {data, error} = await supabase
    .from('sessions')
    .select("*")
    .eq('id',sessionId)
    .maybeSingle();

    if (error) throw new Error(error.message);
    return data;
}

/** Create a new session
 * @param {string} teacherId
 * @param {Object} sessionData
 * @returns {Promise<Object>} created session
 */
export async function createSession(teacherId,sessionData){
  const {
    title,
    start_date = null,
    end_date = null,
    duration,
    is_draft = true,
  } = sessionData;

  const join_code = await generateUniqueJoinCode();

  const {data,error} = await supabase
  .from('sessions')
  .insert([{
    teacher_id : teacherId,
    title,
    start_date,
    end_date,
    duration_minutes : duration,
    is_draft,
    join_code,
  }])
  .select(`
    id,
      teacher_id,
      title,
      join_code,
      start_date,
      end_date,
      duration_minutes,
      is_draft,
      created_at
    `)
    .single();

    if (error) throw new Error(error.message);
    return data;
}

/**
 * Get all sessions created by a teacher
 * @param {string} teacherId
 * @returns {Promise<Array>} list of sessions
 */

export async function getSessionsByTeacherId(teacherId){
  const {data , error} = await supabase
  .from('sessions')
  .select('*')
  .eq('teacher_id',teacherId);

  if (error) throw new Error(error.message);
  return data;
}

export async function deleteSessionDependencies(sessionId) {
  const { data: questions, error: questionFetchError } = await supabase
    .from("questions")
    .select("id")
    .eq("session_id", sessionId);

  if (questionFetchError) throw new Error(questionFetchError.message);

  const questionIds = (questions || []).map((q) => q.id);
  if (questionIds.length > 0) {
    const { error: optionDeleteError } = await supabase
      .from("question_options")
      .delete()
      .in("question_id", questionIds);
    if (optionDeleteError) throw new Error(optionDeleteError.message);
  }

  const { error: questionDeleteError } = await supabase
    .from("questions")
    .delete()
    .eq("session_id", sessionId);
  if (questionDeleteError) throw new Error(questionDeleteError.message);

  const { error: participantDeleteError } = await supabase
    .from("participants")
    .delete()
    .eq("session_id", sessionId);
  if (participantDeleteError) throw new Error(participantDeleteError.message);

  const { error: activityDeleteError } = await supabase
    .from("session_activity")
    .delete()
    .eq("session_id", sessionId);
  if (activityDeleteError) throw new Error(activityDeleteError.message);
}

export async function deleteSessionByIdAndTeacherId(sessionId, teacherId) {
  const { data, error } = await supabase
    .from("sessions")
    .delete()
    .eq("id", sessionId)
    .eq("teacher_id", teacherId)
    .select("id")
    .maybeSingle();

  if (error) throw new Error(error.message);
  return data;
}


