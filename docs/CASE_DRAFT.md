# UNSCRIPTED
Intelligence is not authority.

## Body page 1 | The problem I chose

### A decision that almost wasn't yours
It is 2040. A senior AI engineer receives an offer in Tokyo: 40% higher compensation, relocation support, 48 hours to respond. Their agent proposes rejecting it because, in 2036, they said they wanted to stay in India. The prediction might even be accurate. The mistake is treating it as permission. A person should be allowed to become someone their agent did not predict.

### My scope and assumptions
I assume personal agents are widely available, handle routine tasks and can propose consequential actions. Participating agent platforms expose an execution gateway; users retain final authority. I focus on busy professionals in India who already delegate across work and personal life. The job: handle routine work without deciding my career, money or relationships for me. A secondary stakeholder is anyone whose private information appears in the agent's context.

### Why protect authority?
Delegation has real benefits: accessible assistance, less administration and fewer routine errors. But an agent optimized around yesterday's preferences can make yesterday permanent. Repeatedly accepting its suggestions can displace deliberation. Private conversations can expose people who never adopted the product. When agents transact with other agents, one unauthorized decision can propagate before anyone notices. Responsibility becomes hard to trace, while commercial incentives can shape which options a person sees.

I prioritize the authority gap because it is both consequential and actionable: knowing a user does not establish the right to act. Improving recommendation accuracy alone cannot close that gap. Blocking all delegation would throw away its benefits.

### Evidence that shaped the design
Ping Identity's 2026 report describes 70% of Indian respondents as willing to independently delegate decisions and access; 87% worry about an agent misrepresenting their personality or values [1]. Those are separate questions, not a measured overlap. Pew finds 61% of US adults want more control over how AI is used in their lives [2]. These are distinct samples and attitudes, not demand estimates for this product.

Lee et al. surveyed 319 knowledge workers, collecting 936 examples; greater confidence in generative AI was associated with less reported critical-thinking effort [3]. This motivates testing an independent first choice, but does not prove that my design improves thinking.

### The product opportunity
Build a permission boundary between an agent's proposal and execution. Give routine tasks standing, limited authority; ask for present intent when stakes rise. Generic confirmation can still anchor a user to the agent's answer. My hypothesis is that capturing a first response before revealing that answer makes the review more deliberate. That first response is revisable, never a claim about the user's true desire.

## Body page 2 | The product and the test

### UNSCRIPTED: a personal AI intent firewall
A shared, deterministic engine checks intent freshness, delegated authority, third-party exposure and consequence. It routes each structured proposal to execute, review or block. An agent can explain a rule; it cannot expand its permission. Intent Contracts define scope, recipients, limits and expiry. A Decision Passport records the original assumption, first response, contract snapshot, rule, authorization and simulated outcome.

### Three boundaries, one system
Career: show neutral Tokyo offer facts, capture the user's independent reaction, then reveal the proposed rejection and its 2036 assumption. The user can request details, explicitly authorize rejection, or defer. Exploring never means accepting the job; deferring does not stop the deadline.

Money: block a proposed INR 200,000 investment against an INR 25,000 cap. Raising the cap removes that violation, but the consequential action still needs explicit approval. Changing a permission is not making a transaction.

Privacy: block a friend's private chat, contact and health details from reaching a planning service. Offer a generic itinerary request instead. The user cannot grant themselves another person's consent. Meanwhile, an INR 820 grocery reorder within its contract proceeds without interruption.

### What I build first, and what I defer
P0 is the shared engine, complete Tokyo flow, investment boundary, third-party block, editable contracts and passports. These demonstrate autonomy, authority, privacy and accountability together. Next, test whether people understand scopes and review reasons. Defer real integrations, verified third-party consent, cross-agent revocation and signed attestations until enforcement is dependable.

The prototype is browser-local HTML/CSS/JavaScript with simulated outcomes. Real deployment needs authenticated, expiring approvals and a trusted gateway that refuses unapproved actions. Closed agents and out-of-band execution remain outside its control. A gateway outage should hold consequential actions, with a direct human path to the underlying service. Local passports are inspectable records, not tamper-proof evidence.

### How I would know it works
North star: consequential actions completed with valid, understandable authorization divided by consequential actions attempted. Pair this with overall task completion so blocking everything cannot look successful. Guardrails are unauthorized executions, unnecessary interruptions on permitted routine tasks, review time, abandonment and privacy incidents. Count blocks as events, never as impact.

Run a small, consented usability pilot with career, finance and privacy tasks. Randomize human-first versus AI-first presentation, using an unanchored baseline intent check. Measure comprehension of the final authorization, unintended commitments and completion time. Inspect disagreements qualitatively; a small pilot cannot establish causal impact. Do not launch the gateway until adversarial tests show approvals cannot bypass hard rules.

### The trade-off and the path in
Every review consumes attention; too few reviews surrender authority. Tune friction by reversibility and stakes, and test contract comprehension rather than adding alerts. Start with privacy-conscious professionals already using several agents. Free personal controls and paid multi-agent policies/history are monetization hypotheses, not validated willingness to pay. Platform partnerships supply the enforcement point; platform-native permission controls are also the main competitive risk. The defensible promise is a boundary the user can understand and inspect.
