import type { Metadata } from "next";
import { Playfair_Display, DM_Sans } from "next/font/google";
import { GoogleTagManager } from "@next/third-parties/google";
import Script from "next/script";
import "./globals.css";

const playfair = Playfair_Display({
  subsets: ["latin"],
  style: ["normal", "italic"],
  weight: ["400", "500"],
  variable: "--font-playfair",
});

const dmSans = DM_Sans({
  subsets: ["latin"],
  weight: ["300", "400", "500"],
  variable: "--font-dm-sans",
});

export const metadata: Metadata = {
  title: "Nearwise — Peace of Mind, Every Day",
  description: "Nearwise's AI companion, Gloria, calls or texts your parent every day — then sends you a clear, actionable summary of how they're really doing.",
  icons: {
    icon: "/favicon.svg",
  },
};
// New comment! 
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <GoogleTagManager gtmId="GTM-W4PW6ZRG" />
      <body className={`${playfair.variable} ${dmSans.variable}`}>
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=AW-17993018268"
          strategy="beforeInteractive"
        />
        <Script id="gtag-init" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'AW-17993018268');
          `}
        </Script>
        {children}
      </body>
    </html>
  );
}
