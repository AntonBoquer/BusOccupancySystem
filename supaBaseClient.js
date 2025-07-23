import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// ✅ Hardcoded credentials since .env does not work in plain JavaScript
const SUPABASE_URL = "https://yhsoxuyjrdchmbrlwqci.supabase.co";
const SUPABASE_KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inloc294dXlqcmRjaG1icmx3cWNpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEwNzE0MjksImV4cCI6MjA1NjY0NzQyOX0.pSsbZwAG8HNOQ-WPuKaRunoTn-Bal4uqDMlnhupe0DY";

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export default supabase; // ✅ Export the Supabase client
