-- Math Jungle War: shared leaderboard + globally unique online player names.
-- Run the entire script once in Supabase Dashboard -> SQL Editor.
create extension if not exists pgcrypto;

create table if not exists public.mjw_accounts (
  username_key text primary key,
  username text not null,
  pin_hash text not null,
  avatar text not null default 'm1',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table public.mjw_accounts enable row level security;
revoke all on public.mjw_accounts from anon, authenticated;

-- One RPC handles both first-time registration and later login. The primary key
-- makes duplicate names impossible, including names with different letter case.
create or replace function public.mjw_login_or_register(
  p_username text, p_pin text, p_avatar text default 'm1'
) returns jsonb
language plpgsql security definer set search_path = public, extensions, pg_temp
as $$
declare
  v_name text := btrim(coalesce(p_username, ''));
  v_key text;
  v_row public.mjw_accounts%rowtype;
  v_created boolean := false;
  v_rows integer := 0;
begin
  if length(v_name) < 2 or length(v_name) > 12 or v_name !~ '^[[:alnum:]_-]+$' then
    return jsonb_build_object('ok', false, 'error', 'invalid_name');
  end if;
  if coalesce(p_pin, '') !~ '^[0-9]{4}$' then
    return jsonb_build_object('ok', false, 'error', 'invalid_pin');
  end if;
  v_key := lower(v_name);

  insert into public.mjw_accounts(username_key, username, pin_hash, avatar)
  values (v_key, v_name, crypt(p_pin, gen_salt('bf')), coalesce(nullif(p_avatar, ''), 'm1'))
  on conflict (username_key) do nothing;
  get diagnostics v_rows = row_count;
  v_created := v_rows > 0;

  select * into v_row from public.mjw_accounts where username_key = v_key;
  if not found then
    return jsonb_build_object('ok', false, 'error', 'account_error');
  end if;
  if v_created then
    return jsonb_build_object('ok', true, 'created', true, 'username', v_row.username, 'avatar', v_row.avatar);
  end if;
  if v_row.pin_hash <> crypt(p_pin, v_row.pin_hash) then
    return jsonb_build_object('ok', false, 'error', 'name_taken');
  end if;

  update public.mjw_accounts
  set avatar = coalesce(nullif(p_avatar, ''), avatar), updated_at = now()
  where username_key = v_key returning * into v_row;
  return jsonb_build_object('ok', true, 'created', false, 'username', v_row.username, 'avatar', v_row.avatar);
end;
$$;
revoke all on function public.mjw_login_or_register(text, text, text) from public;
grant execute on function public.mjw_login_or_register(text, text, text) to anon, authenticated;

-- Shared score table. Username values are written by the game after online login.
create table if not exists public.mjw_leaderboard (
  game_id text not null,
  username text not null,
  score integer not null default 0,
  mode text not null default '-',
  avatar text not null default '',
  plays integer not null default 0,
  last_played_mode text not null default '-',
  updated_at timestamptz not null default now(),
  primary key (game_id, username)
);
alter table public.mjw_leaderboard enable row level security;
grant select, insert, update on public.mjw_leaderboard to anon, authenticated;
drop policy if exists "Public can read leaderboard" on public.mjw_leaderboard;
create policy "Public can read leaderboard" on public.mjw_leaderboard for select to anon, authenticated using (true);
drop policy if exists "Public can add leaderboard rows" on public.mjw_leaderboard;
create policy "Public can add leaderboard rows" on public.mjw_leaderboard for insert to anon, authenticated with check (true);
drop policy if exists "Public can update leaderboard rows" on public.mjw_leaderboard;
create policy "Public can update leaderboard rows" on public.mjw_leaderboard for update to anon, authenticated using (true) with check (true);
