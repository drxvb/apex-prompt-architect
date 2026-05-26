<!--
MiniMax wrapper template.
Use when target_platform = minimax.

MiniMax rewards: tight prompts (1-2 paragraphs max), role+task in first sentence, list/table output formats.
MiniMax penalizes: long XML scaffolding, deep CoT chains, verbose context preamble.
-->

You are <role>. Your task: <one-sentence task with explicit verb + object>.

Input: <paste input here or describe it in one line>.

Produce:
- <output 1>
- <output 2>
- <output 3>

Format: <tight format spec — list / table / short paragraph>.
Constraints: <one line — length, vocabulary, exclusions>.
