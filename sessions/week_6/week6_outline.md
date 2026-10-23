1. short feedback from last week as always, quiz grade overview (5 min)
2. final project expectations (presentation+report) (\~5 min together with week 6 assessment)
   1. jupyter notebook allowed instead of streamlit app
   2. but then require HTML in github pages
3. assessment for 6 week - get started with the shared github repo - invite Gustav and me, deploy the scaffolding if it's an app or GitHub page
   1. tricky part is collaborating - I'd recommend having a clear division of labor early on to avoid merge conflicts
4. student pitches - 15 groups \* (1.5 min + 1 min feedback/questions)= \~40 min
5. intro to what we'll cover today (\~5 min)
   1. streamlit from empty github repo, to scaffolded app to deployed app
   2. few main points: relative paths, requirements.txt, env/secret vars, lock parts of the app; localhost development and deployment on streamlit cloud; public vs private repo; data currently on github - easy to start with supabase if they want to keep data private
   3. other points - user auth, roles - just mention
6. sample project walkthrough as described above (\~40 min)
7. for agentic engineering, I would add one slide on the regular workflow and invite to the agentic AI workshop
8. main pitfalls:
   1. env/secret variables - not on github, not in the AI chats
   2. sensitive data - files, tabular (same - not on github, not in AI chats)
   3. money - anything that touches services you pay for (use rate limiters, rotate API keys often)
   4. server load / user roles - make sure that public-facing websites are minimal load on the server
