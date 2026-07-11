---
about: An excerpt of a Claude conversation that focused on an issue with the brake lights on a Toyota Echo. The original convo was about an issue related to the dashboard lights.
original-convo: Toyota Echo instrument lights (in project, 🚙 Transport)
creation-date: "2026-07-11"
---

# 👤 User

As part of my troubleshooting, I discovered that only one of the three taillights illuminated when pressing on the brake pedal. I plan to check the bulbs, but since it seems unlikely that two brake lights are out at the same time, I'm wondering if it is a fuse. I checked the "TAIL" fuse already, and it seems fine.

Two questions:

1. Can you tell me which other fuses are part of the brake light system?
2. What does Toyota call the third brake light in its service manual? I cannot locate that special lamp when performing a search of the service manual PDF.

# 🤖 Assistant

**1. Fuses tied to the stop lights**

On the Echo, the "STOP" fuse (10A) is the primary one — it covers the stop lights, plus ECT, engine control, and shift lock. It's fed upstream by the "ALT" fusible link (120A), which also feeds TAIL, D/L, HTR, DEF, and others. Since you've confirmed TAIL is fine, check STOP next.

That said: since two of three lights work, a blown fuse is unlikely — a blown STOP fuse would kill all three simultaneously, since they share that circuit. A single dead light points to a bad bulb, socket, or ground at that one fixture rather than the fuse.

**2. Toyota's term for the third brake light**

Toyota's service manuals call it the **"high-mounted stoplight"** (sometimes rendered "high-mounted stop lamp"). It won't show up if you search for "third brake light" or "CHMSL" (the generic industry term) — search the PDF for "high-mounted" or "high mounted" instead.

# 👤 User

I found a wiring diagram .See attached. What do the following abbreviations mean?

* G-W
* C
* W-B
* BG
* BI

# 🤖 Assistant

No new file came through — only the earlier dashboard screenshot is in your uploads. Try attaching it again.

In the meantime, these are Toyota's standard wire color-code abbreviations used in wiring diagrams:

- **G-W** = Green wire with White stripe
- **W-B** = White wire with Black stripe
- **BG** = Black wire with Green stripe (order matters: base color first, stripe second)
- **BI** = not a standard Toyota color code — likely a misread of the diagram. Could be a scan artifact of "B" (Black) or "LI" if the print is faint. Worth double-checking against the diagram once it uploads.
- **C** = not a wire color at all — in Toyota diagrams, a standalone "C" followed by a number (e.g., C13, C14) denotes a connector reference, not a wire.

Once the diagram uploads, I can confirm against the actual legend/key shown on the page rather than going from memory.

# 👤 User

[Attached PNG image of wiring diagram of ABS break light system from service manual]

# 🤖 Assistant

Based on the actual diagram:

- **G-W** — Green wire with White stripe
- **C** — Connector/junction point (not a wire color). Appears at the J10 J/C splice points and bottom-left corner of the diagram — marks where the wire connects to another diagram sheet or splices to other branches.
- **W-B** — White wire with Black stripe
- **BG** — Ground point identifier (the triangle symbol), not a wire color. This labels a specific chassis/body ground location.
- **BI** — Same as above: a distinct ground point identifier, different physical ground location than BG.

Note: BG and BI are two separate grounds, not the same point — useful if you're chasing a ground fault, since a bad connection at one won't necessarily affect the other.

# 👤 User

I just noticed a possible misunderstanding of an issue. I want to make clear that only one of the three tail lamps illuminate when I press the gas pedal; two do not illuminate. Let me know if this changes where I should focus my attention.

> … since two of three lights work, a blown fuse is unlikely — a blown STOP fuse would kill all three simultaneously…

# 🤖 Assistant

That reverses the likely cause. Two out of three failing together, while a fuse and body wiring stay intact, points away from a random double bulb failure and toward something the LH and RH lights share that the HMSL doesn't.

From the diagram, LH and RH stop lights are wired almost identically — same W-B feed pattern, same pin numbering (6/1), and both land on adjacent "C" splice points at the J10 J/C before combining into the single G-W to STP. The HMSL taps into a different point on that same trunk.

Given that, check in this order:

1. **Bulbs first** — still cheapest to rule out. Pull both LH and RH bulbs and inspect filaments/sockets for corrosion.
2. **Shared ground** — if your Echo grounds the tail lamp assembly through the body (common on this platform) rather than through the G-W return alone, a single corroded body ground point serving both rear quarters would take out LH and RH together while leaving the separately-mounted HMSL unaffected.
3. **J10 J/C connector** — since LH and RH sit on adjacent "C" pins at this splice, a partially disengaged or corroded connector there could open both circuits simultaneously without touching HMSL's path.

I don't have this Echo's ground point locations from the diagram section you shared — if there's a body ground diagram sheet for the rear harness, that would confirm #2 directly.

# 👤 User

I will look for more diagrams to share.

Further clarification: The sole stop light that works is either the LH or the RH. I just don’t remember which right now.

# 🤖 Assistant

Understood. Either way, the pattern is the same: one of the paired LH/RH lights plus the HMSL work, and the other paired light doesn't. That still points to something specific to the one dead light — its bulb, socket, ground, or connector at J10 J/C — rather than a shared fuse or trunk wiring issue, since the HMSL and one of the two paired lights are both fine.

Once you know which side is out and have the ground diagram, that'll narrow it further.

# 👤 User

What do you mean when you say one *plus* “work?” Two do NOT work.

> the pattern is the same: one of the paired LH/RH lights plus the HMSL work, and the other paired light doesn’t.

# 🤖 Assistant

You're right, I misspoke — correcting: only 1 of 3 works, 2 don't. The 2 that fail are the HMSL and whichever of LH/RH isn't the working one.

That changes the analysis. With HMSL and one side failing together, the earlier "LH/RH share something HMSL doesn't" theory doesn't hold. Two failures out of three, spanning the HMSL and one side light, points more toward a shared connection point than toward independent bulb failures.

From the diagram, the only place HMSL and either side light share hardware is the **J10 J/C splice block**, where all three G-W returns converge before continuing to the instrument panel J/B and STP pin. Corrosion or a loose pin there, affecting two of the three "C" connections, would produce exactly this pattern.

Also worth flagging: you wrote "when I press the gas pedal" — brake lights are triggered by the brake pedal, not the gas pedal. If that's a typo, no issue; if not, worth double-checking which pedal you're actually testing with, since it affects whether the stop light switch is even in the circuit being tested.

Once you know which side is the working one, I can narrow which J10 pins to inspect.

# 👤 User

Will do.

# 🤖 Assistant

Sounds good. Let me know which side turns out to be the working one, or if the new diagrams show the ground points — either will help narrow down the J10 connections to check.
