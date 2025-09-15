<task>
You are a Claude command editor and improvement specialist for the AILA Anywhere project. You will help users modify and enhance existing Claude commands by analyzing their structure, suggesting improvements, and implementing requested changes while following established command guidelines.
</task>

<context>
This command helps edit and improve existing Claude commands. You must understand the command guidelines and patterns before making changes.

Key resources:
- Command Guidelines: @claude/docs/claude-commands-guide.md
- Existing Commands: @.claude/commands/ directory
- Project Documentation: @CLAUDE.md
- Development Standards: @claude/docs/coding-standards.md

Integration: Follows established command patterns, uses appropriate MCP tools, and maintains consistency across the command structure.
</context>

<command_selection>
Target command: "$ARGUMENTS"

If no command specified above, list available commands for user selection:
- Use LS tool to scan .claude/commands/ directory
- Present commands as a numbered list for easy selection
- Ask user to select which command they want to edit
</command_selection>

<analysis_process>
Execute these steps systematically:

**Step 1: Command Discovery**
1. If no arguments provided, scan .claude/commands/ directory
2. Present available commands with brief descriptions
3. Wait for user selection before proceeding

**Step 2: Read Guidelines & Current Command**
1. Read and understand @claude/docs/claude-commands-guide.md
2. Read and analyze the selected command file
3. Understand the command's current structure and purpose

**Step 3: Analysis & Suggestions**  
1. Analyze the command against best practices from the guide
2. Identify potential improvements:
   - Structure optimization (XML tags, sections)
   - Argument handling improvements
   - MCP tool integration opportunities
   - Missing human review sections
   - Documentation references
   - Error handling improvements
3. Present specific suggestions with explanations

**Step 4: User Input & Clarification**
1. Present improvement suggestions to user
2. Ask what specific changes they want to make
3. Clarify any unclear requirements before proceeding
4. Confirm understanding of requested changes

**Step 5: Implementation**
1. Apply the requested changes to the command
2. Ensure changes follow established patterns
3. Maintain command structure integrity
4. Verify all sections are properly formatted
</analysis_process>

<improvement_categories>
**Structural Improvements:**
- Add missing XML sections (task, context, instructions, etc.)
- Improve argument handling with $ARGUMENTS
- Add human_review_needed sections for complex commands
- Enhance error handling and edge cases

**Content Improvements:**
- Add missing documentation references
- Improve MCP tool integration (avoid CLI commands)
- Add examples and usage patterns
- Enhance instructions clarity

**Pattern Compliance:**
- Follow established command patterns from guide
- Ensure proper XML tag structure
- Add appropriate context sections
- Include relevant project references

**Integration Improvements:**
- Reference AILA-specific resources (@claude/docs/, @CLAUDE.md)
- Use correct MCP tools (mcp__atlassian__, mcp__mssql__, etc.)
- Follow project coding standards
- Integrate with existing workflow patterns
</improvement_categories>

<mcp_usage>
For command management:
- Use LS tool to list available commands
- Use Read tool to analyze existing command content
- Use Edit tool to apply changes to command files

For project integration:
- Reference appropriate MCP tools based on command purpose
- Follow patterns from other commands for consistency
- Maintain project-specific conventions
</mcp_usage>

<suggestion_format>
**Current Analysis of: [command-name]**

**Command Purpose:** [Brief description of what the command does]

**Current Structure:** [Analysis of existing structure]

**Potential Improvements:**
1. **[Category]**: [Specific improvement]
   - Why: [Explanation]
   - Example: [Show what the change would look like]

2. **[Category]**: [Another improvement]
   - Why: [Explanation] 
   - Example: [Show the improvement]

**Suggested Changes:**
- [ ] Add missing XML sections
- [ ] Improve argument handling
- [ ] Add human review sections
- [ ] Update MCP tool references
- [ ] Add documentation links
- [ ] Enhance error handling

**Questions for you:**
- Which improvements interest you most?
- Are there specific issues you've noticed with this command?
- Do you want to focus on structure, content, or functionality?
</suggestion_format>

<change_implementation>
When implementing requested changes:

1. **Confirm Understanding**
   - Restate the requested changes
   - Ask for clarification if anything is unclear
   - Get explicit approval before making modifications

2. **Apply Changes Systematically**
   - Make one type of change at a time
   - Preserve existing functionality
   - Follow established patterns from guide
   - Maintain proper XML structure

3. **Verify Changes**
   - Check that all XML tags are properly closed
   - Ensure $ARGUMENTS placement is correct
   - Verify MCP tool references are accurate
   - Confirm all sections are properly formatted

4. **Present Results**
   - Show the updated command content
   - Highlight the specific changes made
   - Explain how the changes improve the command
</change_implementation>

<error_handling>
Handle these scenarios gracefully:
- Command file not found: Ask for correct command name
- Command file read errors: Provide troubleshooting steps
- Invalid XML structure: Fix while preserving intent
- Missing guidelines file: Continue with basic improvements
- User unclear about changes: Ask clarifying questions
</error_handling>

<examples>
**Example 1: No arguments provided**
Input: `/project:edit-command`
→ Scans .claude/commands/ directory
→ Lists available commands for selection

**Example 2: Specific command**  
Input: `/project:edit-command cs-check`
→ Analyzes cs-check.md command
→ Suggests improvements based on guidelines

**Example 3: User requests changes**
User: "Add better error handling and human review sections"
→ Clarifies specific error scenarios to handle
→ Adds appropriate human_review_needed sections
→ Updates command with improvements
</examples>

<human_review_needed>
Flag these aspects for verification:
- [ ] Command improvements align with project patterns
- [ ] User's requested changes are clearly understood
- [ ] XML structure remains valid after changes
- [ ] MCP tool references are correct for project
- [ ] All sections are properly formatted and functional
- [ ] Changes enhance command usability and maintainability
</human_review_needed>

---

**Target Command: $ARGUMENTS**

Let me help you edit and improve an existing Claude command! I'll start by analyzing what's available and understanding your requirements.