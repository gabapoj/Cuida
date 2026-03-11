'use client';
import { useState, useEffect, useRef } from "react";
import "./landing.css";

export default function Home() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [placeholder, setPlaceholder] = useState("Your email address");
  const mobileMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const hamburger = document.getElementById("hamburgerBtn");
    const closeBtn = document.getElementById("closeMenu");
    const menu = mobileMenuRef.current;
    if (!hamburger || !closeBtn || !menu) return;

    const open = (e: Event) => { e.stopPropagation(); menu.classList.add("open"); };
    const close = () => menu.classList.remove("open");

    hamburger.addEventListener("click", open);
    closeBtn.addEventListener("click", close);
    menu.querySelectorAll("a").forEach(a => a.addEventListener("click", close));

    return () => {
      hamburger.removeEventListener("click", open);
      closeBtn.removeEventListener("click", close);
    };
  }, []);

  async function submitEmail() {
    if (!email) return;
    setLoading(true);
    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (data.ok) {
        window.location.href = "/thank-you";
        return;
      } else {
        throw new Error(data.error);
      }
    } catch {
      setEmail("");
      setPlaceholder("Something went wrong — try again");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* NAV */}
      <nav>
        <div className="logo">Nearwise</div>
        <ul>
          <li><a href="#how-it-works">How it works</a></li>
          <li><a href="#for-seniors">For seniors</a></li>
          <li><a href="#for-families">For families</a></li>
          <li><a href="#why-nearwise">Why Nearwise?</a></li>
          <li><a href="#early-access" className="nav-cta">Get early access</a></li>
        </ul>
        <div id="hamburgerBtn" className="hamburger">
          <span></span><span></span><span></span>
        </div>
      </nav>

      {/* MOBILE MENU */}
      <div id="mobileMenu" ref={mobileMenuRef} className="mobile-menu">
        <button id="closeMenu" className="mobile-menu-close">×</button>
        <a href="#how-it-works">How it works</a>
        <a href="#for-seniors">For seniors</a>
        <a href="#for-families">For families</a>
        <a href="#early-access" className="mobile-menu-cta">Get early access</a>
      </div>

      {/* HERO */}
      <section className="hero">
        <div className="hero-left">
          <div className="eyebrow">
            <div className="eyebrow-dot"></div>
            AI companion for seniors
          </div>
          <h1>Your loved one is <em>never</em> alone. Even when you can&apos;t be there.</h1>
          <p className="hero-sub">Nearwise&apos;s AI companion, Gloria, calls and texts your loved one throughout the day — then sends <em>you</em> a clear, actionable summary of how they&apos;re really doing. Finally, real visibility into their daily life — and real peace of mind for you.</p>
          <div className="hero-actions">
            <a href="#early-access" className="btn-primary" style={{ textDecoration: "none" }}>Get early access →</a>
            <a href="#how-it-works" className="btn-secondary" style={{ textDecoration: "none" }}>See how it works</a>
          </div>
          <div className="trust-row">
            <div className="trust-item">
              <span className="trust-num">8 in 10</span>
              <span className="trust-label">seniors look forward to calls</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-item">
              <span className="trust-num">Daily</span>
              <span className="trust-label">proactive check-ins</span>
            </div>
            <div className="trust-divider"></div>
            <div className="trust-item">
              <span className="trust-num">Daily</span>
              <span className="trust-label">insight summary for you</span>
            </div>
          </div>
        </div>

        <div className="hero-right">
          <div className="phone-mockup">
            <div className="phone-frame">
              <div className="phone-screen">
                <div className="phone-status">
                  <span>9:32 AM</span>
                  <span>●●●</span>
                </div>
                <div className="call-screen">
                  <div className="caller-avatar">G</div>
                  <div className="caller-name">Gloria</div>
                  <div className="caller-tag">Daily check-in · 3:24</div>
                  <div className="call-wave">
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                    <div className="wave-bar"></div>
                  </div>
                  <div className="call-transcript">
                    <div className="transcript-line"><strong>Gloria:</strong> Good morning Margaret! Did you sleep well last night?</div>
                    <div className="transcript-line"><strong>Margaret:</strong> Oh yes, much better. My knee isn&apos;t as stiff today.</div>
                    <div className="transcript-line"><strong>Gloria:</strong> That&apos;s wonderful to hear! And have you taken your morning medications yet?</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="float-card float-card-1">
              <div className="card-label">Today&apos;s summary</div>
              <div className="card-value">Mom is doing well ✓</div>
              <div className="card-sub">Meds taken · Mood: positive</div>
            </div>

            <div className="float-card float-card-2">
              <div className="card-label">Alert sent to you</div>
              <div className="card-value">Mentioned knee pain</div>
              <div className="card-sub">3 days in a row · See details →</div>
            </div>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how-it-works" className="section">
        <div className="section-header">
          <div className="section-eyebrow">How it works</div>
          <h2>Friendly calls and texts. Every single day.</h2>
          <p className="section-sub">Gloria isn&apos;t a robocall. She&apos;s a warm, patient companion who remembers what your loved one told her last week — and asks about it.</p>
        </div>
        <div className="steps-grid">
          <div className="step">
            <div className="step-num">01</div>
            <span className="step-icon">🌅</span>
            <h3>Gloria calls and texts throughout the day</h3>
            <p>Gloria reaches out with friendly calls and texts — natural, unhurried conversations with your loved one about how they slept, their mood, medications, appetite, and more.</p>
          </div>
          <div className="step">
            <div className="step-num">02</div>
            <span className="step-icon">🧠</span>
            <h3>She listens and remembers</h3>
            <p>Gloria remembers past conversations — if they mentioned a doctor&apos;s appointment, she&apos;ll ask how it went. It feels personal because it is.</p>
          </div>
          <div className="step">
            <div className="step-num">03</div>
            <span className="step-icon">📲</span>
            <h3>You get a daily actionable summary</h3>
            <p>You receive a clear, plain-language digest — mood, medications, sleep, flagged concerns, and week-over-week trends. No more guessing. No more &quot;I&apos;m fine.&quot; Just real visibility, every day.</p>
          </div>
        </div>

        {/* MOBILE ONLY: compact numbered steps */}
        <div className="steps-mobile">
          <div className="step-mobile">
            <div className="step-mobile-num">01</div>
            <div className="step-mobile-content">
              <h4>Gloria calls and texts throughout the day</h4>
              <p>A natural, unhurried conversation — sleep, mood, meds, appetite, all covered at their pace.</p>
            </div>
          </div>
          <div className="step-mobile">
            <div className="step-mobile-num">02</div>
            <div className="step-mobile-content">
              <h4>She listens and remembers</h4>
              <p>Gloria picks up where she left off. If they mentioned a doctor visit, she asks how it went.</p>
            </div>
          </div>
          <div className="step-mobile">
            <div className="step-mobile-num">03</div>
            <div className="step-mobile-content">
              <h4>You get a daily summary</h4>
              <p>A clear digest — mood, meds, flags, trends. No guessing. No &quot;I&apos;m fine.&quot; Just real visibility.</p>
            </div>
          </div>
        </div>
      </section>

      {/* FOR SENIORS */}
      <section id="for-seniors" className="seniors-section">
        <div className="seniors-inner">
          <div className="section-header">
            <div className="section-eyebrow" style={{ color: "var(--sage)" }}>For seniors</div>
            <h2 style={{ color: "var(--dark)" }}>A friend who shows up. Every single day.</h2>
            <p className="section-sub">Gloria isn&apos;t just a check-in service. For your loved one, she&apos;s a warm, patient presence who genuinely listens — and always has time to talk.</p>
          </div>
          <div className="seniors-grid">
            <div className="senior-card">
              <div className="senior-icon">🤝</div>
              <h3>Real companionship</h3>
              <p>Gloria remembers their stories, asks follow-up questions, and picks up where the last conversation left off. It feels like catching up with an old friend — not talking to a machine.</p>
            </div>
            <div className="senior-card">
              <div className="senior-icon">☕</div>
              <h3>No pressure, no rush</h3>
              <p>Gloria moves at their pace. There&apos;s no agenda to rush through. If they want to talk about the grandkids for twenty minutes, that&apos;s exactly what they&apos;ll do.</p>
            </div>
            <div className="senior-card">
              <div className="senior-icon">🩺</div>
              <h3>An extra layer of care</h3>
              <p>Gloria gently checks in on how they&apos;re feeling, whether they&apos;ve taken their medications, and flags anything worth a closer look — without ever being intrusive or clinical.</p>
            </div>
            <div className="senior-card">
              <div className="senior-icon">🌟</div>
              <h3>They feel seen</h3>
              <p>Seniors often feel overlooked. Gloria treats every conversation like it matters — because it does. Your loved one ends every call feeling heard, valued, and a little less alone.</p>
            </div>
          </div>

          {/* MOBILE ONLY: compact bullet list */}
          <ul className="seniors-bullet-list">
            <li><span className="bullet-icon">🤝</span><span><strong>Real companionship.</strong> Remembers their stories and picks up where the last conversation left off.</span></li>
            <li><span className="bullet-icon">☕</span><span><strong>No pressure, no rush.</strong> Gloria moves at their pace — no agenda, just conversation.</span></li>
            <li><span className="bullet-icon">🩺</span><span><strong>Medication check-ins.</strong> Gently confirms meds were taken and flags anything worth a closer look.</span></li>
            <li><span className="bullet-icon">🌟</span><span><strong>They feel heard.</strong> Every call ends with your loved one feeling valued, not talked at.</span></li>
          </ul>

          <div className="seniors-quote">
            <div className="sq-bar"></div>
            <p>&quot;I just want to know someone&apos;s checking in on her — and that she has someone to talk to when I can&apos;t be there.&quot;</p>
            <span>— What every adult child tells us</span>
          </div>
        </div>
      </section>

      {/* VISIBILITY SECTION */}
      <section id="for-families" className="visibility-section">
        <div className="vis-left">
          <div className="section-eyebrow">Your daily digest</div>
          <h2>You&apos;ll know more about your loved one&apos;s day than ever before.</h2>
          <p style={{ fontSize: "16px", lineHeight: "1.75", color: "var(--mid)", marginBottom: "40px" }}>You get a clean summary sent straight to your phone. Not a wall of data — just the things that matter, flagged clearly, so you can act when it counts and rest easy when everything&apos;s fine.</p>
          <div className="vis-features">
            <div className="vis-feature">
              <div className="vis-icon">😴</div>
              <div>
                <div className="vis-feat-title">Sleep &amp; Energy</div>
                <div className="vis-feat-sub">How they slept, energy levels, any restlessness noted</div>
              </div>
            </div>
            <div className="vis-feature">
              <div className="vis-icon">💊</div>
              <div>
                <div className="vis-feat-title">Medication Adherence</div>
                <div className="vis-feat-sub">Confirmed taken, flagged if skipped or uncertain</div>
              </div>
            </div>
            <div className="vis-feature">
              <div className="vis-icon">😊</div>
              <div>
                <div className="vis-feat-title">Mood &amp; Wellbeing</div>
                <div className="vis-feat-sub">Emotional tone, any worries or anxieties surfaced</div>
              </div>
            </div>
            <div className="vis-feature">
              <div className="vis-icon">🚩</div>
              <div>
                <div className="vis-feat-title">Flags &amp; Trends</div>
                <div className="vis-feat-sub">Patterns across days — so you catch things early, not late</div>
              </div>
            </div>
          </div>
        </div>
        <div className="vis-right">
          <div className="digest-card">
            <div className="digest-header">
              <div className="digest-title">Mom&apos;s Daily Summary</div>
              <div className="digest-date">Today, 9:47 AM</div>
            </div>
            <div className="digest-status good">
              <span className="status-dot"></span> Overall: Doing well today
            </div>
            <div className="digest-rows">
              <div className="digest-row">
                <span className="dr-label">😴 Sleep</span>
                <span className="dr-val good-text">Slept 7 hrs, felt rested</span>
              </div>
              <div className="digest-row">
                <span className="dr-label">💊 Meds</span>
                <span className="dr-val good-text">Confirmed taken ✓</span>
              </div>
              <div className="digest-row">
                <span className="dr-label">😊 Mood</span>
                <span className="dr-val good-text">Upbeat, excited about visit</span>
              </div>
              <div className="digest-row">
                <span className="dr-label">🍽️ Appetite</span>
                <span className="dr-val warn-text">Lighter than usual — worth asking</span>
              </div>
              <div className="digest-row">
                <span className="dr-label">🦵 Physical</span>
                <span className="dr-val warn-text">Knee pain mentioned (4th day)</span>
              </div>
            </div>
            <div className="digest-flag">
              <div className="flag-title">⚠️ Flagged for you</div>
              <div className="flag-body">Margaret has mentioned knee discomfort 4 days in a row. You may want to follow up or check in with her doctor.</div>
              <div className="flag-action">View full transcript →</div>
            </div>
            <div className="digest-trend">
              <div className="trend-label">7-day mood trend</div>
              <div className="trend-bars">
                <div className="trend-bar" style={{ height: "40%" }}></div>
                <div className="trend-bar" style={{ height: "55%" }}></div>
                <div className="trend-bar" style={{ height: "50%" }}></div>
                <div className="trend-bar" style={{ height: "70%" }}></div>
                <div className="trend-bar" style={{ height: "65%" }}></div>
                <div className="trend-bar" style={{ height: "80%" }}></div>
                <div className="trend-bar active" style={{ height: "85%" }}></div>
              </div>
              <div className="trend-note">Trending up ↑ this week</div>
            </div>
          </div>
        </div>
      </section>

      {/* PAIN POINTS / WHY NEARWISE */}
      <section id="why-nearwise" className="pain-section">
        <div className="section-header">
          <div className="section-eyebrow">Built for real families</div>
          <h2>The worries that keep you up at night</h2>
          <p className="section-sub">We built Nearwise around the four fears every adult child carries.</p>
        </div>
        <div className="pain-grid">
          <div className="pain-item">
            <span className="pain-icon">🌑</span>
            <h3>&quot;I have no idea what&apos;s actually happening&quot;</h3>
            <p>Parents say &quot;I&apos;m fine&quot; even when they&apos;re not. You only find out there was a problem three visits later.</p>
            <div className="resolved"><span className="check">✓</span> A daily actionable summary — real visibility, finally</div>
          </div>
          <div className="pain-item">
            <span className="pain-icon">💊</span>
            <h3>&quot;Did she remember her medications today?&quot;</h3>
            <p>The average senior takes 7+ medications. One missed day for a blood thinner or heart med can mean a hospital visit.</p>
            <div className="resolved"><span className="check">✓</span> Gentle daily medication check-ins, flagged if missed</div>
          </div>
          <div className="pain-item">
            <span className="pain-icon">🧩</span>
            <h3>&quot;He seems lonely and I can&apos;t always be there&quot;</h3>
            <p>Isolation kills — literally. Chronic loneliness accelerates cognitive decline as much as smoking 15 cigarettes a day.</p>
            <div className="resolved"><span className="check">✓</span> A genuine companion who calls or texts, listens, and cares</div>
          </div>
          <div className="pain-item">
            <span className="pain-icon">🚨</span>
            <h3>&quot;Did mom fall this morning?&quot;</h3>
            <p>Knowing what happened at home is time consuming. Get alerted in the family app.</p>
            <div className="resolved"><span className="check">✓</span> Instant alerts in the family app when something comes up</div>
          </div>
        </div>
      </section>

      {/* CTA / EARLY ACCESS */}
      <section id="early-access" className="cta-section">
        <h2>Know your loved one is okay. Every single day.</h2>
        <p>Join families who&apos;ve replaced worry with visibility. Gloria calls and texts your loved one throughout the day — and sends you a clear daily summary. Reserve your spot on the early access waitlist today.</p>
        {submitted ? (
          <div style={{ position: "relative", zIndex: 1 }}>
            <p style={{ color: "white", fontSize: "20px", fontFamily: "var(--font-playfair), serif", marginBottom: "8px" }}>You&apos;re on the list!</p>
            <p style={{ color: "rgba(255,255,255,0.7)", fontSize: "15px" }}>Welcome to the Nearwise family. We&apos;ll be in touch shortly.</p>
          </div>
        ) : (
          <div className="signup-row">
            <input
              className="email-input"
              type="email"
              placeholder={placeholder}
              value={email}
              onChange={e => setEmail(e.target.value)}
              onKeyDown={e => { if (e.key === "Enter") submitEmail(); }}
              required
            />
            <button className="btn-white" onClick={submitEmail} disabled={loading}>
              {loading ? "Submitting..." : "Get early access"}
            </button>
          </div>
        )}
        {!submitted && <p className="privacy-note">No spam — just onboarding details. Check your inbox shortly.</p>}
      </section>

      {/* FOOTER */}
      <footer>
        <div className="footer-logo">Nearwise</div>
        <div className="footer-copy">© 2026 Nearwise Health</div>
      </footer>
    </>
  );
}
