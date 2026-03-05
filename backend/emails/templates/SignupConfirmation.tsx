import { Heading, Section, Text } from '@react-email/components';
import * as React from 'react';
import { BaseLayout, Button } from './components';

interface SignupConfirmationProps {
  user_email: string;
}

export default function SignupConfirmation({
  user_email = 'user@example.com',
}: SignupConfirmationProps) {
  return (
    <BaseLayout preview="Welcome to Cuida — your account is ready">
      <Section className="mb-6">
        <Heading className="text-foreground text-[28px] font-bold m-0 leading-tight tracking-tight">
          Welcome to Cuida
        </Heading>
      </Section>

      <Text className="text-muted-foreground text-base leading-relaxed mb-6 font-normal">
        Your account for <strong className="text-foreground font-semibold">{user_email}</strong> is
        all set. We're glad to have you here.
      </Text>

      <Text className="text-muted-foreground text-base leading-relaxed mb-8 font-normal">
        Cuida helps you stay connected with your loved ones. Get started by exploring the app.
      </Text>

      <Section className="my-8 text-center">
        <Button href="https://app.cuida.app">Open Cuida</Button>
      </Section>

      {/* Help notice */}
      <Section className="mt-12 p-4 bg-neutral-50 rounded-lg border border-neutral-100">
        <Text className="text-muted-foreground text-sm leading-relaxed m-0">
          <strong className="text-foreground font-semibold">Need help?</strong>
          <br />
          Reply to this email and we'll get back to you as soon as we can.
        </Text>
      </Section>
    </BaseLayout>
  );
}
