/**
 * Privacy Policy page — legal privacy policy for Nearwise Health.
 * Route: /privacy-policy
 */
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy | Nearwise Health",
  description: "Nearwise Health Privacy Policy",
};

export default function PrivacyPolicy() {
  return (
    <>
      <style>{`
        .pp-wrapper {
          min-height: 100vh;
          background: #faf8f5;
          font-family: var(--font-dm-sans), 'DM Sans', sans-serif;
          color: #2c2c2c;
        }

        .pp-nav {
          padding: 20px 40px;
          border-bottom: 1px solid #e8e3dc;
          background: #faf8f5;
        }

        .pp-nav-inner {
          max-width: 800px;
          margin: 0 auto;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .pp-logo {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 20px;
          font-weight: 600;
          color: #2c6e49;
          text-decoration: none;
        }

        .pp-back-link {
          font-size: 14px;
          color: #666;
          text-decoration: none;
          display: flex;
          align-items: center;
          gap: 6px;
          transition: color 0.2s;
        }
        .pp-back-link:hover { color: #2c6e49; }

        .pp-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 60px 40px 100px;
        }

        .pp-wrapper .doc-label {
          font-size: 12px;
          font-weight: 500;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: #2c6e49;
          margin-bottom: 16px;
        }

        .pp-wrapper h1 {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 40px;
          font-weight: 600;
          color: #1a1a1a;
          line-height: 1.2;
          margin-bottom: 12px;
        }

        .pp-wrapper .effective-date {
          font-size: 14px;
          color: #888;
          margin-bottom: 48px;
          padding-bottom: 48px;
          border-bottom: 1px solid #e8e3dc;
        }

        .pp-wrapper .intro {
          font-size: 17px;
          line-height: 1.75;
          color: #444;
          margin-bottom: 48px;
          font-weight: 300;
        }

        .pp-wrapper section {
          margin-bottom: 44px;
        }

        .pp-wrapper h2 {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 20px;
          font-weight: 600;
          color: #1a1a1a;
          margin-bottom: 14px;
        }

        .pp-wrapper p {
          font-size: 15px;
          line-height: 1.8;
          color: #555;
          margin-bottom: 12px;
        }

        .pp-wrapper ul {
          padding-left: 20px;
          margin-bottom: 12px;
        }

        .pp-wrapper li {
          font-size: 15px;
          line-height: 1.8;
          color: #555;
          margin-bottom: 6px;
        }

        .pp-wrapper .highlight-box {
          background: #f0f7f4;
          border-left: 3px solid #2c6e49;
          padding: 18px 22px;
          border-radius: 0 8px 8px 0;
          margin: 20px 0;
        }

        .pp-wrapper strong { font-family: var(--font-playfair), 'Lora', serif; }

        .pp-wrapper .highlight-box p {
          margin: 0;
          color: #2c6e49;
          font-weight: 500;
          font-size: 14px;
        }

        .pp-wrapper .contact-block {
          background: #fff;
          border: 1px solid #e8e3dc;
          border-radius: 12px;
          padding: 28px 32px;
          margin-top: 8px;
        }

        .pp-wrapper .contact-block p { margin-bottom: 4px; }

        .pp-wrapper table {
          width: 100%;
          border-collapse: collapse;
          margin: 16px 0;
          font-size: 14px;
        }

        .pp-wrapper th {
          text-align: left;
          padding: 10px 14px;
          background: #f0f7f4;
          color: #2c6e49;
          font-weight: 500;
          border-bottom: 2px solid #c5dfd0;
        }

        .pp-wrapper td {
          padding: 10px 14px;
          border-bottom: 1px solid #e8e3dc;
          color: #555;
          vertical-align: top;
        }

        .pp-wrapper h3 {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 16px;
          font-weight: 600;
          color: #1a1a1a;
          margin-bottom: 10px;
          margin-top: 20px;
        }

        .pp-wrapper a { color: #2c6e49; }

        .pp-footer {
          text-align: center;
          padding: 32px;
          font-size: 13px;
          color: #aaa;
          border-top: 1px solid #e8e3dc;
        }
      `}</style>

      <div className="pp-wrapper">
        <nav className="pp-nav">
          <div className="pp-nav-inner">
            <a href="/" className="pp-logo">Nearwise Health</a>
            <a href="/" className="pp-back-link">&larr; Back to home</a>
          </div>
        </nav>

        <div className="pp-container">
          <p className="doc-label">Legal</p>
          <h1>Privacy Policy</h1>
          <p className="effective-date">Effective Date: March 10, 2026 &nbsp;&middot;&nbsp; Last Updated: March 10, 2026</p>

          <p className="intro">
            This Privacy Policy describes how Nearwise Health (&ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;), a sole proprietor operating the Nearwise Health companion care service (&ldquo;Service&rdquo;), collects, uses, and shares information about you.
          </p>

          <section>
            <h2>1. Information We Collect</h2>
            <h3>Information You Provide</h3>
            <ul>
              <li><strong>Account information:</strong> name, email address, and phone number during enrollment</li>
              <li><strong>Care Recipient information:</strong> name and phone number of the senior family member receiving the service</li>
              <li><strong>Payment information:</strong> processed securely through our payment provider</li>
              <li><strong>Communications:</strong> messages or inquiries you send us</li>
            </ul>
            <h3>Information Collected Automatically</h3>
            <ul>
              <li><strong>Device information:</strong> device type, operating system, and browser type</li>
              <li><strong>Usage data:</strong> IP address and interactions with our website</li>
            </ul>
          </section>

          <section>
            <h2>2. How We Use Your Information</h2>
            <p>We use the information we collect to:</p>
            <ul>
              <li>Create and maintain your account</li>
              <li>Conduct daily AI wellness check-in phone calls with enrolled seniors</li>
              <li>Send transactional SMS messages (see Section 3)</li>
              <li>Send service-related communications and updates</li>
              <li>Respond to questions and support requests</li>
              <li>Enforce our Terms of Service and prevent abuse</li>
            </ul>
          </section>

          <section>
            <h2>3. SMS Messaging</h2>
            <p>We send SMS messages for service operation purposes only:</p>

            <h3>Service Notifications (A2P / Application-to-Person)</h3>
            <p>
              When you enroll in Nearwise Health, you and/or your Care Recipient consent to receive SMS notifications related to the service, including wellness check-in reminders, medication reminders, and post-call activity summaries. Message frequency: typically 1&ndash;3 messages per day.
            </p>

            <h3>OTP / Phone Verification (Transactional)</h3>
            <p>
              When you create an account or log in, we may send a one-time passcode (OTP) to verify your identity. Message frequency: one message per sign-in or verification event.
            </p>

            <p><strong>Message and data rates may apply.</strong></p>
            <p>To opt out of SMS messages, reply <strong>STOP</strong> to any message. Reply <strong>HELP</strong> for assistance.</p>
            <div className="highlight-box">
              <p>Your phone number and SMS opt-in data will not be shared with or sold to third parties for marketing purposes.</p>
            </div>
          </section>

          <section>
            <h2>4. How We Share Your Information</h2>
            <p>We do not sell your personal information. We share information only with the following service providers, solely to operate the Service:</p>
            <table>
              <thead>
                <tr>
                  <th>Provider</th>
                  <th>Purpose</th>
                  <th>Privacy Policy</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Twilio</td>
                  <td>Phone calls and SMS delivery</td>
                  <td><a href="https://www.twilio.com/legal/privacy" target="_blank" rel="noreferrer">twilio.com/legal/privacy</a></td>
                </tr>
                <tr>
                  <td>Stripe</td>
                  <td>Payment processing</td>
                  <td><a href="https://stripe.com/privacy" target="_blank" rel="noreferrer">stripe.com/privacy</a></td>
                </tr>
                <tr>
                  <td>Vercel</td>
                  <td>Website hosting</td>
                  <td><a href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noreferrer">vercel.com/legal/privacy-policy</a></td>
                </tr>
              </tbody>
            </table>
            <p>We may also disclose your information if required by law, legal process, or to protect the rights and safety of our users or the public.</p>
          </section>

          <section>
            <h2>5. Data Retention</h2>
            <p>
              We retain your personal information for as long as your account is active. If you delete your account, we will delete your profile and associated data within 30 days, except where retention is required by law.
            </p>
          </section>

          <section>
            <h2>6. Your Rights and Choices</h2>
            <p>You may:</p>
            <ul>
              <li><strong>Access or correct</strong> your information by contacting us</li>
              <li><strong>Delete your account</strong> by contacting us at <a href="mailto:info@nearwise.xyz">info@nearwise.xyz</a></li>
              <li><strong>Opt out of SMS</strong> by replying STOP to any text message we send</li>
            </ul>
            <p>For California residents and others with applicable rights under GDPR, CCPA, or similar laws, you may also request a copy of your data or object to certain processing by contacting us at the address below.</p>
          </section>

          <section>
            <h2>7. Children&apos;s Privacy</h2>
            <p>
              The Service is intended for adults 18 years of age and older. We do not knowingly collect information from children under 13. If we learn we have collected such information, we will delete it promptly.
            </p>
          </section>

          <section>
            <h2>8. Security</h2>
            <p>
              We use industry-standard security measures, including TLS encryption in transit, to protect your information. No system is completely secure; use the Service at your own risk.
            </p>
          </section>

          <section>
            <h2>9. Changes to This Policy</h2>
            <p>
              We may update this policy from time to time. We will notify you of material changes by posting the updated policy here with a new effective date. Your continued use of the Service after changes take effect constitutes acceptance.
            </p>
          </section>

          <section>
            <h2>10. Contact Us</h2>
            <p>For privacy questions, data requests, or to report a concern:</p>
            <div className="contact-block">
              <p><strong>Nearwise Health</strong></p>
              <p>Email: <a href="mailto:info@nearwise.xyz">info@nearwise.xyz</a></p>
              <p>Website: <a href="https://nearwise.xyz">nearwise.xyz</a></p>
            </div>
          </section>
        </div>

        <footer className="pp-footer">
          &copy; {new Date().getFullYear()} Nearwise Health. All rights reserved.
        </footer>
      </div>
    </>
  );
}
