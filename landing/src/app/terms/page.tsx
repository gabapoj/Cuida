/**
 * Terms of Service page — legal terms for Nearwise Health.
 * Route: /terms
 */
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms & Conditions | Nearwise Health",
  description: "Nearwise Health Terms and Conditions",
};

export default function Terms() {
  return (
    <>
      <style>{`
        .tos-wrapper {
          min-height: 100vh;
          background: #faf8f5;
          font-family: var(--font-dm-sans), 'DM Sans', sans-serif;
          color: #2c2c2c;
        }

        .tos-nav {
          padding: 20px 40px;
          border-bottom: 1px solid #e8e3dc;
          background: #faf8f5;
        }

        .tos-nav-inner {
          max-width: 800px;
          margin: 0 auto;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .tos-logo {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 20px;
          font-weight: 600;
          color: #2c6e49;
          text-decoration: none;
        }

        .tos-back-link {
          font-size: 14px;
          color: #666;
          text-decoration: none;
          display: flex;
          align-items: center;
          gap: 6px;
          transition: color 0.2s;
        }
        .tos-back-link:hover { color: #2c6e49; }

        .tos-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 60px 40px 100px;
        }

        .tos-wrapper .doc-label {
          font-size: 12px;
          font-weight: 500;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: #2c6e49;
          margin-bottom: 16px;
        }

        .tos-wrapper h1 {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 40px;
          font-weight: 600;
          color: #1a1a1a;
          line-height: 1.2;
          margin-bottom: 12px;
        }

        .tos-wrapper .effective-date {
          font-size: 14px;
          color: #888;
          margin-bottom: 48px;
          padding-bottom: 48px;
          border-bottom: 1px solid #e8e3dc;
        }

        .tos-wrapper .intro {
          font-size: 17px;
          line-height: 1.75;
          color: #444;
          margin-bottom: 48px;
          font-weight: 300;
        }

        .tos-wrapper section {
          margin-bottom: 44px;
        }

        .tos-wrapper h2 {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 20px;
          font-weight: 600;
          color: #1a1a1a;
          margin-bottom: 14px;
        }

        .tos-wrapper p {
          font-size: 15px;
          line-height: 1.8;
          color: #555;
          margin-bottom: 12px;
        }

        .tos-wrapper ul {
          padding-left: 20px;
          margin-bottom: 12px;
        }

        .tos-wrapper li {
          font-size: 15px;
          line-height: 1.8;
          color: #555;
          margin-bottom: 6px;
        }

        .tos-wrapper .sms-box {
          background: #f0f7f4;
          border: 1px solid #c5dfd0;
          border-radius: 12px;
          padding: 28px 32px;
          margin: 24px 0;
        }

        .tos-wrapper .sms-box h3 {
          font-family: var(--font-playfair), 'Lora', serif;
          font-size: 16px;
          font-weight: 600;
          color: #1a1a1a;
          margin-bottom: 14px;
        }

        .tos-wrapper .sms-box p,
        .tos-wrapper .sms-box li {
          font-size: 14px;
          color: #444;
        }

        .tos-wrapper .keyword-row {
          display: flex;
          gap: 10px;
          flex-wrap: wrap;
          margin-top: 12px;
        }

        .tos-wrapper .keyword-pill {
          background: #fff;
          border: 1px solid #c5dfd0;
          border-radius: 20px;
          padding: 5px 14px;
          font-size: 13px;
          font-weight: 500;
          color: #2c6e49;
        }

        .tos-wrapper .disclaimer-box {
          background: #fff8f0;
          border-left: 3px solid #e8924a;
          padding: 18px 22px;
          border-radius: 0 8px 8px 0;
          margin: 20px 0;
        }

        .tos-wrapper .disclaimer-box p {
          margin: 0;
          font-size: 14px;
          color: #7a4a1a;
          font-weight: 500;
        }

        .tos-wrapper .contact-block {
          background: #fff;
          border: 1px solid #e8e3dc;
          border-radius: 12px;
          padding: 28px 32px;
          margin-top: 8px;
        }

        .tos-wrapper .contact-block p { margin-bottom: 4px; }

        .tos-wrapper strong { font-family: var(--font-playfair), 'Lora', serif; }

        .tos-wrapper a { color: #2c6e49; }

        .tos-footer {
          text-align: center;
          padding: 32px;
          font-size: 13px;
          color: #aaa;
          border-top: 1px solid #e8e3dc;
        }
      `}</style>

      <div className="tos-wrapper">
        <nav className="tos-nav">
          <div className="tos-nav-inner">
            <a href="/" className="tos-logo">Nearwise Health</a>
            <a href="/" className="tos-back-link">&larr; Back to home</a>
          </div>
        </nav>

        <div className="tos-container">
          <p className="doc-label">Legal</p>
          <h1>Terms of Service</h1>
          <p className="effective-date"><strong>Effective Date:</strong> March 10, 2026 &nbsp;&nbsp;<strong>Last Updated:</strong> March 10, 2026</p>

          <p className="intro">
            These Terms of Service (&ldquo;Terms&rdquo;) govern your use of the Nearwise Health companion care service (&ldquo;Service&rdquo;) operated by Nearwise Health (&ldquo;we,&rdquo; &ldquo;us,&rdquo; or &ldquo;our&rdquo;), a sole proprietor. By creating an account or using the Service, you agree to these Terms. If you do not agree, do not use the Service.
          </p>

          <section>
            <h2>1. Eligibility</h2>
            <p>You must be at least 18 years old to use the Service. By creating an account, you represent and warrant that:</p>
            <ul>
              <li>You are 18 years of age or older</li>
              <li>You have the legal capacity to enter into these Terms</li>
              <li>You are not prohibited from using the Service under applicable law</li>
            </ul>
          </section>

          <section>
            <h2>2. Accounts</h2>
            <p><strong>Registration.</strong> You must provide a valid phone number and accurate information during sign-up. You are responsible for keeping your account information up to date.</p>
            <p><strong>Account security.</strong> You are responsible for all activity under your account. Do not share your login credentials with anyone. Notify us immediately at <a href="mailto:info@nearwise.xyz">info@nearwise.xyz</a> if you suspect unauthorized access.</p>
            <p><strong>One account per person.</strong> You may not create more than one account or create an account on behalf of someone else without their explicit consent.</p>
          </section>

          <section>
            <h2>3. The Gloria Companion Call</h2>
            <p>
              The Service connects enrolled seniors (&ldquo;Care Recipients&rdquo;) with Gloria, an AI companion that conducts proactive daily wellness check-in calls. Gloria is designed to have natural, friendly conversations while monitoring seven dimensions of wellbeing &mdash; including mood, sleep, medications, nutrition, mobility, social connection, and cognition. The Service is purchased by adult family members (&ldquo;Subscribers&rdquo;) on behalf of Care Recipients.
            </p>
            <p>
              By enrolling a Care Recipient, you confirm that the Care Recipient is aware of and has consented to receiving daily calls and SMS notifications from the Service. Subscribers receive post-call activity summaries and wellness updates.
            </p>
            <div className="disclaimer-box">
              <p>Nearwise Health is a companion care and wellness monitoring service. It is not a licensed medical service, emergency response system, or substitute for professional healthcare. Do not use Nearwise Health as a replacement for emergency services. In an emergency, call 911.</p>
            </div>
          </section>

          <section>
            <h2>4. Prohibited Conduct</h2>
            <p>You agree not to:</p>
            <ul>
              <li>Use the Service if you are under 18</li>
              <li>Create a false or misleading profile or misrepresent your identity or a Care Recipient&apos;s identity</li>
              <li>Enroll a Care Recipient without their knowledge or consent</li>
              <li>Use the Service for commercial solicitation, spam, or advertising</li>
              <li>Attempt to reverse-engineer, scrape, or exploit the Service or its infrastructure</li>
              <li>Circumvent any security or access controls</li>
              <li>Violate any applicable local, state, national, or international law</li>
            </ul>
            <p>We reserve the right to remove content and suspend or terminate accounts that violate these rules, at our sole discretion and without notice.</p>
          </section>

          <section>
            <h2>5. SMS Messaging Program</h2>
            <div className="sms-box">
              <h3>Nearwise Health SMS Program Details</h3>
              <p><strong>Program name:</strong> Nearwise Health</p>
              <p><strong>Message types:</strong> Wellness check-in call reminders, medication reminders, post-call activity summaries, and service notifications</p>
              <p><strong>Message frequency:</strong> Varies based on service plan and activity &mdash; typically 1&ndash;3 messages per day</p>
              <p><strong>Rates:</strong> Message and data rates may apply</p>
              <p style={{marginTop: "16px"}}><strong>SMS Keywords:</strong></p>
              <div className="keyword-row">
                <span className="keyword-pill">STOP &mdash; Opt out</span>
                <span className="keyword-pill">HELP &mdash; Get support</span>
                <span className="keyword-pill">START &mdash; Re-subscribe</span>
              </div>
              <p style={{marginTop: "16px", fontSize: "13px", color: "#666"}}>
                Reply <strong>STOP</strong> at any time to cancel SMS messages from this program. Reply <strong>HELP</strong> for help or contact us at info@nearwise.xyz. Carriers are not liable for delayed or undelivered messages.
              </p>
            </div>
          </section>

          <section>
            <h2>6. Subscription &amp; Payment</h2>
            <p>
              Nearwise Health is offered as a subscription service. By subscribing, you authorize us to charge your payment method on a recurring basis at the rate disclosed at checkout. Subscriptions renew automatically unless cancelled. You may cancel at any time by contacting us.
            </p>
            <p>We reserve the right to change pricing with advance notice. Continued use after a price change constitutes acceptance.</p>
          </section>

          <section>
            <h2>7. Privacy</h2>
            <p>Our collection and use of your personal information is described in our <a href="/privacy-policy">Privacy Policy</a>. By using the Service, you consent to our data practices as described there.</p>
          </section>

          <section>
            <h2>8. Termination</h2>
            <p>We may suspend or terminate your account at any time, with or without cause or notice. You may cancel your account at any time by contacting <a href="mailto:info@nearwise.xyz">info@nearwise.xyz</a>. Upon termination, your right to use the Service ceases immediately and we will delete your data as described in the Privacy Policy.</p>
          </section>

          <section>
            <h2>9. Disclaimers</h2>
            <p style={{fontWeight: 500}}>
              THE SERVICE IS PROVIDED &ldquo;AS IS&rdquo; AND &ldquo;AS AVAILABLE&rdquo; WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SERVICE WILL BE UNINTERRUPTED, ERROR-FREE, OR FREE OF HARMFUL COMPONENTS. WE ARE NOT RESPONSIBLE FOR THE CONDUCT OF CARE RECIPIENTS OR SUBSCRIBERS, OR FOR MISSED CALLS, DELAYED MESSAGES, OR TECHNICAL FAILURES OUTSIDE OUR CONTROL.
            </p>
          </section>

          <section>
            <h2>10. Limitation of Liability</h2>
            <p style={{fontWeight: 500}}>
              TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, NEARWISE HEALTH SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING FROM YOUR USE OF THE SERVICE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
            </p>
          </section>

          <section>
            <h2>11. Indemnification</h2>
            <p>You agree to indemnify and hold harmless Nearwise Health from any claim, damage, loss, or expense (including reasonable attorneys&apos; fees) arising from your use of the Service, your content, or your violation of these Terms.</p>
          </section>

          <section>
            <h2>12. Governing Law</h2>
            <p>These Terms are governed by the laws of the State of New York, United States, without regard to conflict of law principles. Any dispute arising under these Terms shall be resolved in the state or federal courts located in New York.</p>
          </section>

          <section>
            <h2>13. Changes to These Terms</h2>
            <p>
              We may update these Terms from time to time. We will notify you of material changes by posting the updated Terms here with a new effective date. Your continued use of the Service after changes take effect constitutes acceptance of the updated Terms.
            </p>
          </section>

          <section>
            <h2>14. Contact</h2>
            <div className="contact-block">
              <p><strong>Nearwise Health</strong></p>
              <p>Email: <a href="mailto:info@nearwise.xyz">info@nearwise.xyz</a></p>
              <p>Website: <a href="https://nearwise.xyz">nearwise.xyz</a></p>
            </div>
          </section>
        </div>

        <footer className="tos-footer">
          &copy; {new Date().getFullYear()} Nearwise Health. All rights reserved.
        </footer>
      </div>
    </>
  );
}
