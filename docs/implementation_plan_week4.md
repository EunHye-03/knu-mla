# Implementation Plan - Week 4 Feature Expansion

## Goal Description
Implement comprehensive frontend features for Auth (Email Signup, Forgot/Reset Password), Account Management (Delete), and enhanced Memo/Project management with strict i18n support.

## Proposed Changes

### 1. Internationalization Update
#### [MODIFY] [language-context.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/components/layout/language-context.tsx)
- Add translation keys for:
    - **Auth**: `forgot_password`, `reset_password`, `email_label`, `email_placeholder`, `signup_email_error`, `reset_link_sent`.
    - **Account**: `delete_account`, `delete_account_warning`, `type_delete_to_confirm`, `account_deleted`.
    - **Memos**: `memos_title`, `rename_memo`, `delete_memo_confirm`, `emoji_picker`.
    - **Projects**: `projects_manage_title`, `edit_project`, `delete_project_confirm`.

### 2. API Service Expansion
#### [MODIFY] [api.ts](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/services/api.ts)
- Add methods:
    - `getMemos`, `updateMemo`, `deleteMemo`
    - `getProjects`, `updateProject`, `deleteProject`
    - `signupWithEmail` (update existing or new)
    - `requestPasswordReset`, `resetPassword`
    - `deleteAccount`

### 3. Authentication Features
#### [MODIFY] [app/login/page.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/app/login/page.tsx)
- Add "Forgot Password?" link pointing to `/forgot-password`.

#### [NEW] [app/forgot-password/page.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/app/forgot-password/page.tsx)
- Input email form to request reset link.

#### [NEW] [app/reset-password/page.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/app/reset-password/page.tsx)
- Handle `token` query param.
- Input new password and confirm.

#### [MODIFY] [app/register/page.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/app/register/page.tsx)
- Add **Email** field (required).
- Add specific validation for email format.

### 4. Settings & Account Management
#### [MODIFY] [components/SettingsDialog.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/components/SettingsDialog.tsx)
- Add "Danger Zone" or "Account" tab.
- Add "Delete Account" flow with confirmation modal ("Type DELETE").

### 5. Feature Management Pages
#### [NEW] [app/memos/page.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/app/memos/page.tsx)
- Full page list of memos.
- Actions: Rename, Delete, Change Emoji.

#### [NEW] [app/projects/page.tsx](file:///c:/Users/ASUS/Desktop/knu%20mla/frontend/app/projects/page.tsx)
- Full page list of projects.
- Actions: Edit (Name/Desc), Delete.
