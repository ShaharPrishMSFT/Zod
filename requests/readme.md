# Worktree Communication System

This directory serves as a central communication hub between different worktrees in the FormalAI repository. It enables structured request exchange and cross-worktree collaboration while maintaining clear boundaries.

## Communication Protocol

1. **Request Creation**
   - Create a new markdown file in the format: `YYYYMMDD_requestor-target.md`
   - Example: `20250512_python-configuration.md` for a request from python worktree to configuration worktree

2. **Request Structure**
   ```markdown
   # Request: [Brief Title]
   
   ## From
   [Source Worktree]
   
   ## To
   [Target Worktree]
   
   ## Description
   [Detailed request description]
   
   ## Status
   - [ ] Pending
   - [ ] In Progress
   - [ ] Completed
   - [ ] Rejected
   
   ## Response
   [To be filled by target worktree]
   ```

3. **Request Processing**
   - Target worktree periodically checks for requests
   - Updates status as appropriate
   - Provides response in the designated section
   - Commits changes to maintain communication history

## Active Communications Index

No active communications at present. This section will be updated as communications are created.

Format:
- [YYYYMMDD] [Requestor] → [Target]: [Brief Description] (Status)

## Historical Communications

No historical communications yet. Completed requests will be moved here.
