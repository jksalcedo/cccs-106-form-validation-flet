# Week 5 Laboratory Task: CSPC Scholarship Intake Portal
### CCCS 106: Application Development and Emerging Technologies
### Collaborative Group Laboratory Worksheet

 **Instructor:** Allan O. Ibo, Jr., MSc

 ---

**Target Framework:** Python 3.12+ & Flet SDK v0.86.5

#### Functional Requirements Matrix

The application intake form captures five (5) core fields with strict validation rules:

| Field Name | Flet Control | Constraint / Validation Rule | Error Message Feedback |
| --- | --- | --- | --- |
| **Applicant Name** | `ft.TextField` | Mandatory, 2 to 60 characters, alphabetic characters, hyphens, periods, and spaces only. | `"Enter a valid name (2–60 letters, hyphens, or periods)."` |
| **Student ID** | `ft.TextField` | Mandatory, strictly follows CSPC student ID pattern: `^20\d{2}-\d{4,5}$` (e.g., `2024-0123`). | `"Invalid Student ID. Expected format: YYYY-NNNN (e.g., 2024-0123)."` |
| **CSPC Email** | `ft.TextField` | Mandatory, must end with the official institutional domain `@cspc.edu.ph`. | `"Institutional email required (must end with @cspc.edu.ph)."` |
| **Mobile Number** | `ft.TextField` | Mandatory, valid 11-digit Philippine mobile format: `^(?:\+63|0)9\d{9}$`. | `"Invalid mobile number. Expected: 09XXXXXXXXX or +639XXXXXXXXX."` |
| **Academic GWA** | `ft.TextField` | Mandatory numeric float between `1.00` (highest grade) and `5.00` (failing grade). | `"GWA must be a valid number between 1.00 and 5.00."` |
| **Program** | `ft.Dropdown` | Mandatory selection from predefined CSPC scholarship programs. | `"Please select an accredited scholarship program."` |