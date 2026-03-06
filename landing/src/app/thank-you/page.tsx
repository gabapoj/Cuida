/**
 * Thank You page — shown after a user successfully submits their email
 * for early access. Displays confirmation and next steps.
 */
export default function ThankYou() {
  return (
    <>
      <style>{`
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
          --cream: #fdfaf6;
          --warm-gray: #6b6560;
          --dark: #1a1714;
          --accent: #2d6a4f;
          --accent-light: #e8f5ee;
          --border: #e8e2da;
        }

        body {
          font-family: 'Inter', sans-serif;
          background: var(--cream);
          color: var(--dark);
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }

        .ty-nav {
          padding: 1.25rem 2rem;
          border-bottom: 1px solid var(--border);
          display: flex;
          align-items: center;
        }

        .ty-logo {
          font-family: 'Lora', serif;
          font-weight: 600;
          font-size: 1.25rem;
          color: var(--dark);
          text-decoration: none;
        }

        .ty-main {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 3rem 1.5rem;
        }

        .ty-card {
          max-width: 520px;
          width: 100%;
          text-align: center;
        }

        .ty-checkmark {
          width: 64px;
          height: 64px;
          background: var(--accent-light);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin: 0 auto 2rem;
          animation: pop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
        }

        @keyframes pop {
          from { transform: scale(0); opacity: 0; }
          to   { transform: scale(1); opacity: 1; }
        }

        .ty-checkmark svg {
          width: 32px;
          height: 32px;
          color: var(--accent);
        }

        .ty-card h1 {
          font-family: 'Lora', serif;
          font-size: 2rem;
          font-weight: 600;
          line-height: 1.25;
          margin-bottom: 1rem;
          color: var(--dark);
          animation: fadeUp 0.5s 0.1s ease both;
        }

        .ty-card h1 em {
          font-style: italic;
          color: var(--accent);
        }

        .ty-card p {
          font-size: 1.05rem;
          line-height: 1.7;
          color: var(--warm-gray);
          margin-bottom: 1rem;
          animation: fadeUp 0.5s 0.2s ease both;
        }

        @keyframes fadeUp {
          from { transform: translateY(12px); opacity: 0; }
          to   { transform: translateY(0);    opacity: 1; }
        }

        .ty-divider {
          border: none;
          border-top: 1px solid var(--border);
          margin: 2rem 0;
          animation: fadeUp 0.5s 0.3s ease both;
        }

        .ty-what-next {
          text-align: left;
          animation: fadeUp 0.5s 0.35s ease both;
        }

        .ty-what-next h2 {
          font-family: 'Inter', sans-serif;
          font-size: 0.75rem;
          font-weight: 600;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: var(--warm-gray);
          margin-bottom: 1rem;
        }

        .ty-step {
          display: flex;
          align-items: flex-start;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .ty-step-num {
          width: 28px;
          height: 28px;
          min-width: 28px;
          background: var(--accent-light);
          color: var(--accent);
          border-radius: 50%;
          font-size: 0.8rem;
          font-weight: 600;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-top: 1px;
        }

        .ty-step-text strong {
          display: block;
          font-size: 0.95rem;
          font-weight: 600;
          margin-bottom: 0.15rem;
          color: var(--dark);
        }

        .ty-step-text span {
          font-size: 0.875rem;
          color: var(--warm-gray);
          line-height: 1.5;
        }

        .ty-back-link {
          display: inline-block;
          margin-top: 2rem;
          font-size: 0.9rem;
          color: var(--accent);
          text-decoration: none;
          font-weight: 500;
          animation: fadeUp 0.5s 0.45s ease both;
        }

        .ty-back-link:hover {
          text-decoration: underline;
        }

        .ty-footer {
          text-align: center;
          padding: 1.5rem;
          font-size: 0.8rem;
          color: var(--warm-gray);
          border-top: 1px solid var(--border);
        }
      `}</style>

      <nav className="ty-nav">
        <a href="/" className="ty-logo">Nearwise</a>
      </nav>

      <main className="ty-main">
        <div className="ty-card">
          <div className="ty-checkmark">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>

          <h1>You&apos;re on the list. <em>Welcome.</em></h1>

          <p>We&apos;ll be in touch shortly.</p>

          <hr className="ty-divider" />

          <div className="ty-what-next">
            <h2>What happens next</h2>

            <div className="ty-step">
              <div className="ty-step-num">1</div>
              <div className="ty-step-text">
                <strong>Check your inbox</strong>
                <span>You&apos;ll receive a confirmation email with details about early access and next steps.</span>
              </div>
            </div>

            <div className="ty-step">
              <div className="ty-step-num">2</div>
              <div className="ty-step-text">
                <strong>We&apos;ll reach out personally</strong>
                <span>A member of our team will follow up to learn more about your loved one and get Gloria set up.</span>
              </div>
            </div>
          </div>

          <a href="/" className="ty-back-link">&larr; Back to Nearwise</a>
        </div>
      </main>

      <footer className="ty-footer">
        &copy; 2026 Nearwise Health
      </footer>
    </>
  );
}
