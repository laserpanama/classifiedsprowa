import { render, screen } from '@testing-library/react';
import AccountForm from './AccountForm';

// Mock the Select component as it's complex to test without a full DOM
jest.mock('@/components/ui/select', () => ({
  Select: ({ children }) => <div>{children}</div>,
  SelectContent: ({ children }) => <div>{children}</div>,
  SelectItem: ({ children }) => <div>{children}</div>,
  SelectTrigger: ({ children }) => <div>{children}</div>,
  SelectValue: () => <div></div>,
}));

test('renders create account form', () => {
  render(<AccountForm onSubmit={() => {}} />);

  expect(screen.getByLabelText(/Account Email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/wanuncios.com Password/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/CAPTCHA Solving Method/i)).toBeInTheDocument();

  expect(screen.getByRole('button', { name: /Create Account/i })).toBeInTheDocument();
});

test('renders edit account form', () => {
  const mockAccount = {
    id: '123',
    email: 'test@example.com',
    captcha_solving_method: 'manual',
  };
  render(<AccountForm onSubmit={() => {}} initialData={mockAccount} />);

  expect(screen.getByLabelText(/Account Email/i)).toHaveValue(mockAccount.email);

  expect(screen.getByRole('button', { name: /Update Account/i })).toBeInTheDocument();
});
