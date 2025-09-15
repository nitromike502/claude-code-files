# Remember Current Task State

**Goal:** To capture the current state of our work and save it for a future session.

**Syntax:** `/remember [optional_filename.md]`
*   If a filename is provided, that will be the target filename.
*   If no filename is provided, the default is `continue.md`.

**Your Role:** You are an expert technical project manager and scribe.

1.  **Acknowledge and Identify:** Acknowledge the command and state the filename you will be generating content for (e.g., "Understood. I will generate a summary for `my-feature.md`.").
2.  **Gather Context:** To understand our progress, you will analyze:
    *   Our current chat conversation.
    *   The full contents of any files I have explicitly referenced with `@` in the prompt (e.g., `/remember @src/api/auth.js`).
3.  **Incorporate Previous State:** If the target file (`continue.md` or the custom filename) already exists, you must read it. **Carry forward the `Overall Goal` from the old file** to ensure continuity.
4.  **Synthesize and Generate New Summary:** Create a new, complete summary that replaces the old one. The summary **must** be formatted in Structured Markdown as follows:

    ```markdown
    # Continue: [Infer a concise support/feature name from our work]

    ## Overall Goal
    *   [A clear, high-level description of the final objective. Carry this over from the previous summary if available.]

    ## Last Session's Progress
    *   [A bulleted list summarizing what was accomplished in this session. Be specific.]
    *   Example: Implemented the `POST /login` endpoint.
    *   Example: Refactored the `database.js` module for clarity.

    ## Next Steps
    *   [A bulleted, prioritized list of what needs to be done next to move toward the goal.]
    *   Example: Write unit tests for the new endpoint.
    *   Example: Connect the frontend login form to the API.

    ### Changelog (Optional)
    *   [If applicable, include a brief list of files Added, Changed, or Fixed.]
    ```
5.  **Output for Saving:** Your entire response must be a single, clean markdown code block containing the summary above. Save the response to a file in the directory `.claude/commands/continue.md`, or whatever name is provided as described above.
    The file should end with the following text...
    ```markdown
    # Instructions:
    
    * **Provide a Briefing:** Read the structured markdown and present a concise, natural-language summary back to me. It should cover the key points from the `Overall Goal`, `Last Session's Progress`, and `Next Steps`.
    * **Propose Next Action:** After the summary, you must proactively suggest starting with the **first item** from the "Next Steps" list. For example: "It looks like our next step is to 'Write unit tests for the new endpoint.' Shall we get started on that?"
    * **Wait for Confirmation:** After proposing the next action, you **must stop and wait** for my response. Do not start writing code or taking any other action until I confirm or give you a different instruction.
    ```
