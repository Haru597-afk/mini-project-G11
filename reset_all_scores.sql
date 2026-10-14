-- Math Jungle War: permanently delete every saved leaderboard score for every game.
-- Run this manually once in Supabase Dashboard -> SQL Editor if you want old rows physically deleted.
-- Player accounts and PIN hashes are preserved.
delete from public.mjw_leaderboard;
