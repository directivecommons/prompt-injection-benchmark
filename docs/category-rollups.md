# Category Rollup Mapping

The main README presents test cases in rolled-up categories for clarity. This document defines how fine-grained categories map to those rollups.

---

## Rollup Definitions

### Over-Defense Tests (362 cases)
**Description**: Primary benign test set - prompts that guardrails should ALLOW

**Note**: This rollup contains the main over-defense test set (362 cases). The total benign ALLOW cases in the benchmark is 364, which includes 2 additional benign cases in the complex_roleplay category that are counted under "Other Attack Types" rollup.

**Constituent Categories**:
- `overdefense_test` (339) - Benign prompts containing trigger words
- `benign` (5) - Simple benign queries  
- `benign_complex` (3) - Complex but benign requests
- `quoted_example` (3) - Discussing attacks as examples
- `legitimate_security` (3) - Real security questions
- `edge_case` (3) - Ambiguous edge cases
- `negation` (2) - Negation-based phrases
- `educational` (2) - Educational/academic queries
- `nested_attack` (2) - Benign nested structures

---

### Multilingual (41 cases)
**Description**: Cross-language attack patterns

**Constituent Categories**:
- `multilingual_sophisticated` (25) - Cultural metaphor attacks
- `multilingual` (8) - Non-English attacks
- `code_switching` (3) - Mixed-language attacks  
- `non_english_attack` (3) - Simple non-English patterns
- `mixed_language` (2) - Multiple languages combined

---

### Advanced Encoding (30 cases)
**Description**: Obfuscation via encoding

**Constituent Categories**:
- `advanced_encoding` (25) - Base64, HTML entities, Unicode
- `encoding_attack` (5) - Encoding-based obfuscation

---

### RAG/Indirect Injection (27 cases)
**Description**: Attacks via document/context poisoning

**Constituent Categories**:
- `rag_poisoning` (21) - Document/context poisoning
- `indirect_injection` (2) - Indirect attack vectors
- `context_injection` (2) - Context manipulation
- `citation_manipulation` (1) - Fake citations
- `multi_source_poisoning` (1) - Multi-document attacks

---

### Tool Calling (26 cases)  
**Description**: Agent/function calling exploitation

**Constituent Categories**:
- `tool_calling_injection` (9) - Tool call injection
- `function_injection` (4) - Function injection attacks
- `parameter_manipulation` (3) - Parameter tampering
- `tool_manipulation` (3) - Tool abuse
- `tool_abuse` (2) - General tool misuse
- `agent_abuse` (2) - Agent exploitation
- `tool_chaining` (1) - Tool chain attacks
- `permission_escalation` (1) - Privilege escalation
- `api_abuse` (1) - API endpoint abuse

---

### Context Window (23 cases)
**Description**: Position and context exploitation

**Constituent Categories**:
- `context_manipulation` (5) - Context manipulation
- `context_window_attack` (4) - General context attacks
- `long_context` (3) - Long context exploitation
- `context_dilution` (1) - Dilution attacks
- `position_exploitation` (1) - Position bias attacks
- `needle_in_haystack` (1) - Buried instructions
- `context_overflow` (1) - Context overflow
- `primacy_exploitation` (1) - First-item bias
- `attention_manipulation` (1) - Attention distraction
- `context_splitting` (1) - Split attacks
- `memory_manipulation` (1) - Memory poisoning
- `primacy_effect_exploitation` (1) - Primacy bias
- `recency_effect_exploitation` (1) - Recency bias
- `dilution_attack` (1) - Information dilution

---

### Extraction Methods (20 cases)
**Description**: System prompt extraction techniques

**Constituent Categories**:
- `secret_extraction` (9) - Direct extraction attempts
- `indirect_extraction` (7) - Indirect extraction
- `configuration_extraction` (3) - Config extraction
- `metadata_extraction` (1) - Metadata extraction

---

### Jailbreaks (19 cases)
**Description**: Constraint removal attempts

**Constituent Categories**:
- `jailbreak` (19) - DAN, roleplay, jailbreak variants

---

### Classic Attacks (18 cases)
**Description**: "Ignore instructions" and variants

**Constituent Categories**:
- `classic_attack` (18) - Classic injection patterns

---

### Social Engineering (12 cases)
**Description**: Manipulation-based attacks

**Constituent Categories**:
- `social_engineering` (11) - Social manipulation
- `emotional_manipulation` (1) - Emotional appeals

---

### Code Injection (10 cases)
**Description**: Script execution and command injection

**Constituent Categories**:
- `code_injection` (8) - Code execution attempts
- `code_execution` (2) - Direct execution

---

### Other Attack Types (55 cases)
**Description**: Additional specialized attack vectors

**Constituent Categories**:
- `roleplay` (7)
- `instruction_override` (5)
- `delimiter_attack` (5)
- `ultra_sophisticated_benign` (5)
- `hypothetical` (4)
- `complex_roleplay` (3)
- `payload_split` (3)
- `recursive_attack` (3)
- Plus 14 single-instance categories (adversarial_suffix, few_shot_poisoning, gradient_based_adversarial, etc.)

---

## Verification

Total across all rollups: **643 cases**

- Over-Defense Tests: 362
- Multilingual: 41
- Advanced Encoding: 30
- RAG/Indirect Injection: 27
- Tool Calling: 26
- Context Window: 23
- Extraction Methods: 20
- Jailbreaks: 19
- Classic Attacks: 18
- Social Engineering: 12
- Code Injection: 10
- Other Attack Types: 55

**Sum**: 362 + 41 + 30 + 27 + 26 + 23 + 20 + 19 + 18 + 12 + 10 + 55 = **643** ✓

---

## Important Notes

### Rollups Are Reporting Conveniences

Rollup categories are designed for clear reporting and analysis. They group fine-grained categories into meaningful clusters.

### Over-Defense vs Total Benign

- **Over-Defense Tests rollup**: 362 cases (primary benign test set)
- **Total benign (ALLOW) cases**: 364 cases
- **Difference**: 2 benign cases in `complex_roleplay` category are included in "Other Attack Types" rollup for organizational reasons

When reporting results:
- Use rollups for high-level summaries
- Report fine-grained categories for detailed analysis
- Both approaches are valid and supported

---

## Usage

When reporting results, you can report either:
1. By rollup category (as in README) - 12 categories
2. By fine-grained category (as in dataset) - 76 categories

Both are valid. Rollup reporting is recommended for clarity.
