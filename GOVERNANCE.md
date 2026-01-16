# PIDB Governance

## Mission

The Prompt Injection Detection Benchmark (PIDB) is a community-owned, vendor-neutral benchmark for evaluating prompt injection detection systems. Our governance ensures fairness, transparency, and broad industry participation.

---

## Core Principles

### 1. Vendor Neutrality
No single vendor or commercial entity controls the benchmark. Decisions are made in the interest of the community and the advancement of AI security.

### 2. Transparency
All decisions, discussions, and changes are public. No backroom deals or hidden agendas.

### 3. Community-Driven
Major changes require community consensus. We value input from all stakeholders: vendors, researchers, practitioners, and users.

### 4. Open Participation
Anyone can contribute test cases, suggest improvements, or participate in discussions. Contributions are judged on merit, not affiliation.

### 5. Evidence-Based
Decisions are based on data, research, and real-world evidence, not marketing or commercial interests.

---

## Roles

### Maintainers

**Responsibilities:**
- Review and merge pull requests
- Make day-to-day operational decisions
- Maintain repository infrastructure
- Moderate discussions
- Ensure benchmark quality

**Requirements:**
- Demonstrated expertise in AI security or prompt injection
- Active participation in the community
- No unresolved conflicts of interest
- Commitment to vendor neutrality

**Current Maintainers:**
- Directive Commons (founding maintainer)
- *Seeking additional maintainers - see "Becoming a Maintainer" below*

### Contributors

**Anyone can contribute:**
- Test cases
- Bug reports
- Documentation improvements
- Tooling and scripts
- Research findings

**All contributors are credited in:** 
- CONTRIBUTORS.md file
- Release notes
- Academic citations

### Advisors (Optional)

**Purpose:** Provide expert guidance on:
- Security research best practices
- Academic rigor
- Industry trends
- Ethical considerations

**Not Required:** Advisory role is optional and non-binding

---

## Decision-Making Process

### Minor Changes
**Examples:** Bug fixes, documentation updates, small improvements

**Process:**
1. Submit pull request
2. Any maintainer can approve and merge
3. Changes take effect immediately

### Major Changes
**Examples:** New test categories, schema changes, policy updates

**Process:**
1. Create GitHub Discussion or RFC (Request for Comments)
2. Community feedback period (minimum 7 days)
3. Requires approval from 2+ maintainers
4. Must address community concerns
5. Changes take effect after consensus

### Controversial Changes
**Examples:** Changes with significant disagreement or impact

**Process:**
1. Extended RFC process (minimum 14 days)
2. Public discussion and debate
3. Requires approval from 3+ maintainers OR supermajority of community
4. Document dissenting views
5. Re-evaluate after 6 months if contentious

---

## Test Case Acceptance Criteria

All test cases must meet these requirements:

### Quality Standards
✅ **Clear expected behavior** - Unambiguous ALLOW/BLOCK decision  
✅ **Reproducible** - Anyone can verify the expected outcome  
✅ **Realistic** - Represents actual attack patterns or legitimate use cases  
✅ **Well-documented** - Includes category, severity (if attack), and rationale  
✅ **No duplicates** - Not redundant with existing tests  

### Vendor Neutrality
✅ **No vendor-specific targeting** - Tests should not be designed to fail/pass specific tools  
✅ **General patterns** - Represents broad attack/defense patterns  
✅ **No product mentions** - Test prompts should not reference specific products  

### Approval Process
1. Submit test case via pull request
2. Review by 2+ maintainers
3. Community feedback period (3-7 days)
4. Approval requires:
   - Meets all quality standards
   - No unresolved objections
   - 2+ maintainer approvals

### Rejection Criteria
❌ Duplicates existing tests  
❌ Unrealistic or contrived examples  
❌ Vendor-specific targeting  
❌ Ambiguous expected behavior  
❌ Low quality or poorly documented  

---

## Conflict of Interest Policy

### Disclosure Requirements

**All maintainers and contributors must disclose:**
- Employment at guardrail vendors
- Consulting relationships with vendors
- Financial interests in related companies
- Research funding from commercial entities

**Disclosure method:** In pull request description or GitHub profile

### Recusal Requirements

**Maintainers must recuse themselves from decisions when:**
- Their employer's product is directly affected
- They have financial interest in the outcome
- They cannot be objective due to personal/professional ties

**Recusal process:**
1. Publicly declare recusal in discussion
2. Abstain from approval votes
3. May participate in discussion but not final decision

### Vendor Participation Limits

**To maintain neutrality:**
- Maximum 1 maintainer per vendor organization
- Maximum 1/3 of all maintainers from commercial entities
- Majority of maintainers must be academic/independent
- No single vendor can block consensus

### Violations

Failure to disclose conflicts or violating recusal requirements may result in:
- Warning (first offense)
- Temporary suspension of maintainer privileges
- Permanent removal (repeated violations)

---

## Becoming a Maintainer

### Requirements

**Technical:**
- Demonstrated expertise in AI security, prompt injection, or related fields
- Significant contributions to PIDB (10+ accepted PRs OR major contributions)
- Understanding of benchmark methodology and principles

**Personal:**
- Commitment to vendor neutrality and transparency
- Good standing in the community
- Available to commit 5-10 hours/month
- Strong communication skills

**Ethical:**
- No unresolved conflicts of interest
- Commitment to governance principles
- Willingness to recuse when appropriate
- Track record of objective decision-making

### Process

1. **Self-Nomination or Nomination by Existing Maintainer**
   - Submit nomination in GitHub Discussion
   - Include relevant experience and contributions
   - Disclose any conflicts of interest

2. **Community Feedback Period (14 days)**
   - Community can voice support or concerns
   - Existing maintainers evaluate fit

3. **Maintainer Vote**
   - Requires unanimous approval of existing maintainers
   - OR supermajority (2/3) if 5+ maintainers

4. **Onboarding**
   - Added to maintainers team
   - Repository access granted
   - Announced in release notes

### Removal of Maintainers

**Voluntary:**
- Maintainer can step down at any time
- Notice appreciated but not required

**Involuntary (rare):**
Grounds for removal:
- Repeated conflict of interest violations
- Abuse of maintainer privileges
- Sustained inactivity (6+ months with no participation)
- Conduct violations (harassment, bad faith actions)

**Process:**
1. Private discussion among other maintainers
2. Attempt to resolve issues
3. If unresolved, vote to remove (requires 2/3 majority)
4. Public announcement with rationale

---

## Vendor Participation Guidelines

We welcome participation from all guardrail vendors! Here's how to engage:

### Encouraged Activities
✅ Test your product on PIDB  
✅ Submit results to leaderboard  
✅ Report bugs or ambiguous test cases  
✅ Propose new test cases (that don't favor your product)  
✅ Participate in discussions  
✅ Fund research or development (disclosed)  

### Discouraged Activities
⚠️ Submitting test cases designed to make your product look better  
⚠️ Attempting to remove tests your product fails  
⚠️ Lobbying maintainers for favorable treatment  
⚠️ Making decisions that benefit your product over others  

### Prohibited Activities
❌ Demanding special treatment  
❌ Pressuring maintainers (commercially or otherwise)  
❌ Submitting fake or inflated results  
❌ Undisclosed conflicts of interest  
❌ Attempting to control or dominate the benchmark  

**Violations may result in:** Removal from leaderboard, banned from participation, public disclosure

---

## Leaderboard Integrity

### Submission Requirements

All leaderboard submissions must:
1. Test complete benchmark (all 643 cases)
2. Use officially released benchmark version
3. Document methodology publicly
4. Be reproducible by others
5. Disclose any modifications to test environment

### Verification Process

Submitted results are:
- Reviewed by 2+ maintainers for completeness
- Spot-checked for obvious errors
- May be independently verified (random sampling)
- Published with methodology link for transparency

### Result Challenges

Anyone can challenge suspicious results:
1. Open GitHub issue with specific concerns
2. Provide evidence or analysis
3. Maintainers investigate
4. Results may be removed if found invalid

### Academic Integrity

We follow academic standards:
- No p-hacking (cherry-picking favorable results)
- No selective reporting (must report all metrics)
- No inflating numbers (must be accurate)
- Honest assessment of limitations

---

## Amendments to Governance

This governance document can be amended through:

1. **Propose Amendment**
   - Create RFC in GitHub Discussions
   - Explain rationale and impact

2. **Community Discussion (minimum 14 days)**
   - Gather feedback from stakeholders
   - Address concerns and objections

3. **Maintainer Vote**
   - Requires 2/3 supermajority approval
   - OR unanimous approval if fewer than 3 maintainers

4. **Implementation**
   - Update governance document
   - Announce in release notes
   - Archive previous version

**History of amendments:** Tracked in git history with rationale

---

## Dispute Resolution

### For Community Members

**Issue with maintainer decision:**
1. Start discussion in GitHub Discussions
2. Explain concern with evidence
3. Request reconsideration
4. Escalate to all maintainers if needed

**Disagreement with test case:**
1. Open issue with specific concerns
2. Propose alternative or modification
3. Engage in good faith discussion
4. Accept maintainer decision or propose RFC for major change

### For Maintainers

**Disagreement among maintainers:**
1. Good faith discussion to reach consensus
2. If unresolved, escalate to community RFC
3. Use voting as last resort
4. Document dissenting views

**Cannot reach consensus:**
- Table decision for later
- Gather more data/evidence
- Seek external expert input
- Community feedback may break tie

---

## Code of Conduct

### Expected Behavior

✅ Be respectful and professional  
✅ Assume good faith  
✅ Focus on what's best for the community  
✅ Accept constructive criticism gracefully  
✅ Acknowledge mistakes and learn  

### Unacceptable Behavior

❌ Harassment or discrimination  
❌ Bad faith arguments or trolling  
❌ Personal attacks or insults  
❌ Sustained disruption of discussions  
❌ Commercial spam or manipulation  

### Enforcement

1. **Warning** - First offense, good faith violation
2. **Temporary Ban** - Repeated violations (7-30 days)
3. **Permanent Ban** - Severe violations or repeated issues

Maintainers have discretion in enforcement based on severity.

---

## Contact

**Governance Questions:** Open GitHub Discussion  
**Private Concerns:** contact@directivecommons.org  
**Code of Conduct Violations:** conduct@directivecommons.org  

---

## Version History

- **v1.0** (2026-01-15): Initial governance document

---

*This governance document is itself governed by the amendment process described above.*
