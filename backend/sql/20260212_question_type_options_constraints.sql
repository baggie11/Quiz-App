-- Ensure questions has canonical type + options payload storage.
alter table if exists public.questions
  add column if not exists question_type text;

alter table if exists public.questions
  add column if not exists options jsonb;

-- Backfill legacy type values to new canonical values.
update public.questions
set question_type = case lower(coalesce(question_type, ''))
  when 'multiple_choice' then 'mcq'
  when 'multiple_select' then 'mcq'
  when 'msq' then 'mcq'
  when 'single_choice' then 'singlechoice'
  when 'quiz' then 'singlechoice'
  when 'open_ended' then 'open'
  else lower(question_type)
end
where question_type is not null;

-- Keep allowed values constrained.
do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'questions_question_type_check'
  ) then
    alter table public.questions
      add constraint questions_question_type_check
      check (question_type in ('mcq', 'singlechoice', 'open', 'rating'));
  end if;
end $$;
