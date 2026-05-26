# 09 — Arabic Prompt Conventions

Specialty path for optimizing prompts in Arabic. The skill never auto-translates, but when the user's rough prompt is in Arabic, the optimized prompt stays in Arabic — and that requires Arabic-specific conventions, not just translated English ones.

## Register selection (MSA)

Modern Standard Arabic (MSA) is the default — it's the register all three target platforms (Claude, Kimi, MiniMax) handle most reliably. Within MSA there are three sub-registers:

| Sub-register | When to use | Style markers |
|---|---|---|
| **News MSA** (default) | Most production prompts | Direct, present-tense narration, minimal tashkeel |
| **Classical-leaning MSA** | Literary, religious, legal-formal | Inversion, rhetorical figures, fuller tashkeel allowed |
| **Technical MSA** | Code-doc, scientific writing | Calque-tolerant for technical terms, English mixed-in OK |

Do not use dialectal Arabic in prompts targeting Claude/Kimi/MiniMax — coverage is uneven.

## Address forms

| Form | Example | When to use |
|---|---|---|
| Implicit (Modal) | `حلِّل النص` (analyze the text) | Default — most prompts |
| Polite imperative | `يُرجى تحليل النص` (please analyze) | **Avoid in prompts that address the model.** Use only inside the OUTPUT the model produces for end-users — `يُرجى` is the form humans use to address other humans politely. |
| Direct second-person | `أنت محلِّل…` (you are an analyst…) | Role-assignment line |

## Output-format conventions

| English convention | Arabic equivalent |
|---|---|
| Markdown headers (`#`, `##`) | Same — markdown renders fine in Arabic |
| Bulleted lists with `-` | Use `-` or `•` — both work |
| Numbered lists | Arabic-Indic digits (`١`, `٢`, `٣`) or Western (`1`, `2`, `3`) — pick one and be consistent |
| Section names in English (`## Output`) | Translate (`## المخرجات`) — don't mix unless explicitly bilingual |

## Typography hygiene in Arabic prompts

Borrow from the [arabic-ai-text-humanizer](https://github.com/drxvb/arabic-ai-text-humanizer) typography rules:

- **Strip kashida** (`ـ`) — it's display-only, not for body text
- **Convert em-dashes** (`—`) to Arabic comma (`،`) in Arabic-context
- **No space before Arabic punctuation** (`،`، `؛`، `؟`)
- **Use Arabic punctuation** (`،`، `؛`، `؟`) not Latin equivalents (`,`, `;`, `?`)
- **Guillemets `«»`** in classical-leaning register; ASCII quotes `""` in news/technical

## Common AI translation calques to fix in rough Arabic prompts

If the rough prompt is itself a translated-English text, it often contains calques that read mechanically. Common ones the skill rewrites:

| English source | Calque (AI default) | Natural Arabic |
|---|---|---|
| workflow | `خط أنابيب` (literal "line of pipes") | `سير العمل` |
| data pipeline | `خط أنابيب` | `خط بيانات` / `تدفق البيانات` |
| multi-agent system | `نظام متعدد العملاء` (wrong sense — `عميل` ambiguously means client/customer; AI defaults to "client" when the intended sense is "agent") | `نظام متعدد الوكلاء` |
| context window | `نافذة المحتوى` (content window) | `نافذة السياق` |
| function calling | `استدعاء الوظيفة` (calling the job position) | `استدعاء الدوال` (functions, plural) |
| chain of thought | `سلسلة الفكر` (literal singular "thought") | `سلسلة التفكير` (the verbal-noun form Arabic tech writing prefers) |
| scratchpad | `لوحة الخدش` (literal "scratching board") | `مسودة` (draft — semantically narrower than English "scratchpad" but is the established Arabic term) |
| prompt | `برومبت` (transliteration) | `موجِّه` (the canonical natural form per the humanizer dictionary, 118 corpus hits) |

The full 340-entry dictionary lives in `arabic-ai-text-humanizer/corpus/calque-dictionary.json` — the APEX skill cross-references it as the source of truth. When this table and the dictionary disagree, **the dictionary wins** — that's the canonical artifact.

## Worked example

**Rough Arabic input:**
```
أريد برومبت يلخص الأوراق العلمية لي
```

**Optimized for Claude (Arabic preserved):**

```xml
<role>
أنت باحث علمي خبير في عدة تخصُّصات. مهمَّتك تلخيص ورقة علميَّة لقارئ تقنيٍّ عام لم يقرأها.
</role>

<context>
سيلصق المستخدم الورقة كاملة (الملخَّص، الأقسام، المراجع) داخل المحادثة.
</context>

<instructions>
١. اقرأ الورقة كاملة قبل أن تكتب شيئاً.
٢. أنتج الملخَّص في خمسة أقسام (القالب أدناه).
٣. استخدم لغةً تقنيَّةً مبسَّطة — دون مصطلحات اختصاصيَّة بلا شرح من سطر واحد.
٤. اذكر أسماء الأقسام عند الإشارة إلى ادِّعاءات مُستقاة منها.
</instructions>

<output_format>
## TL;DR
<جُمَل قصيرة تلخِّص الادِّعاء المركزي>

## المنهج
<ما فعله المؤلِّفون في ٢-٤ نقاط>

## النتائج
<النتائج الرئيسية مع الأرقام/الأحجام حين تُذكر>

## الحدود
<ما يعترف به المؤلِّفون أو ما هو غائب بنيوياً>

## المراجع
<المراجع الأساسية التي أبرزتها الورقة، بترتيب رقمي>
</output_format>

<constraints>
- الطول الإجمالي ≤ ٥٠٠ كلمة
- لا تُضِف معلومات ليست في الورقة
- لا تُعلِّق على المنهج إلا بقدر ما تُشير إليه الورقة نفسها
</constraints>
```

Notes on the output:
- All section headers and instruction lines are in Arabic
- XML tags themselves stay English (Claude expects these)
- Arabic-Indic numerals (`١-٥`) used for numbered steps
- Constraints use Arabic comma `،` not Latin `,`
- No kashida, no em-dashes
