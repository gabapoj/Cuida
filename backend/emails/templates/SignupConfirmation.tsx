import { Section, Text } from '@react-email/components';
import * as React from 'react';
import { BaseLayout, Button, Divider } from './components';

interface SignupConfirmationProps {
  user_email: string;
}

export default function SignupConfirmation({
  user_email = 'user@example.com',
}: SignupConfirmationProps) {
  return (
    <BaseLayout
      preview="Welcome to Nearwise — your account is ready"
      footerNote="You're receiving this because you created a Nearwise account."
    >
      <Text className="font-serif text-[26px] leading-tight text-dark m-0 mb-5">
        Welcome to Nearwise.
      </Text>

      <Text className="font-sans text-[15px] leading-relaxed text-mid m-0 mb-5">
        Your account for <strong className="text-dark font-semibold">{user_email}</strong> is
        all set. We're glad to have you here.
      </Text>

      <Text className="font-sans text-[15px] leading-relaxed text-mid m-0 mb-7">
        Nearwise is here to help you stay connected with your loved ones — a warm, daily
        companion that keeps you in the loop without the constant worry.
      </Text>

      <Divider />

      <Section className="mb-8">
        <Button href="https://app.nearwise.com">Open Nearwise →</Button>
      </Section>

      <Divider />

      <Text className="font-sans text-[15px] leading-relaxed text-mid m-0">
        Questions? Just reply to this email and we'll get back to you as soon as we can.
      </Text>
    </BaseLayout>
  );
}
