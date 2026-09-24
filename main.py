"""
CCCS 106: Application Development and Emerging Technologies
Week 5 Laboratory Task: CSPC Scholarship Intake Portal
Instructor: Allan O. Ibo, Jr., MSc

Instructions:
  Complete the TODO blocks in Tier 1 and Tier 2.
Target Framework: Flet v0.86.5 (Python 3.12+)
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Tuple
import flet as ft


# ============================================================================
# TIER 3: DOMAIN DATA CONTRACT & CUSTOM EXCEPTIONS
# ============================================================================

class ScholarshipValidationError(Exception):
    """Base exception for all scholarship domain validation errors."""
    


class IDFormatError(ScholarshipValidationError):
    """Raised when student ID does not conform to the CSPC format."""
    pass


class EmailDomainError(ScholarshipValidationError):
    """Raised when an email does not belong to the @cspc.edu.ph domain."""
    pass


class GWARangeError(ScholarshipValidationError):
    """Raised when GWA falls outside the 1.00 to 5.00 grading scale."""
    pass


@dataclass(frozen=True)
class ScholarshipApplicant:
    """Immutable domain contract representing a verified scholarship applicant."""
    full_name: str
    student_id: str
    email: str
    phone: str
    gwa: float
    program: str
    submitted_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# TIER 2: VALIDATION ENGINE (STUDENT IMPLEMENTATION)
# ============================================================================

class ScholarshipValidator:
    """Encapsulated validation rules and regex logic for scholarship applicants."""

    # Compile Regular Expressions
    NAME_REGEX = re.compile(r"^[A-Za-z\s.\-',]{2,60}$")
    STUDENT_ID_REGEX = re.compile(r"^20\d{2}-\d{4,5}$")
    CSPC_EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@cspc\.edu\.ph$")
    PH_PHONE_REGEX = re.compile(r"^(?:\+63|0)9\d{9}$")

    @classmethod
    def sanitize_string(cls, raw: Optional[str]) -> str:
        """Strip leading/trailing whitespace defensively handling None."""
        return (raw or "").strip()

    @classmethod
    def validate_name(cls, value: Optional[str]) -> str:
        """
        Validates full name.
        Returns: Sanitized clean name.
        Raises: ScholarshipValidationError if invalid.
        """
        # TODO: Implement sanitization and pattern validation
        clean = cls.sanitize_string(value)
        if not clean:
            raise ScholarshipValidationError("Full name is required.")
        if not cls.NAME_REGEX.match(clean):
            raise ScholarshipValidationError("Enter a valid name (2–60 letters, hyphens, or periods).")
        return clean

    @classmethod
    def validate_student_id(cls, value: Optional[str]) -> str:
        """
        Validates CSPC student ID format (YYYY-NNNN).
        Returns: Normalized student ID.
        Raises: IDFormatError if invalid.
        """
        clean_id = cls.sanitize_string(value)
        if not clean_id:
            raise ScholarshipValidationError("Student ID is required.")
        if not cls.STUDENT_ID_REGEX.match(clean_id):
            raise IDFormatError("Invalid student ID. Expected format: YYYY-NNNN (e.g., 2024-0123).")
        return clean_id

    @classmethod
    def validate_email(cls, value: Optional[str]) -> str:
        """
        Validates institutional CSPC email address.
        Returns: Lowercased, sanitized email.
        Raises: EmailDomainError if invalid.
        """
        # TODO: Implement email validation using cls.CSPC_EMAIL_REGEX
        pass

    @classmethod
    def validate_phone(cls, value: Optional[str]) -> str:
        """
        Validates and standardizes Philippine mobile numbers to 09XXXXXXXXX.
        Returns: Normalized 11-digit phone string.
        Raises: ScholarshipValidationError if invalid.
        """
        # TODO: Implement phone validation using cls.PH_PHONE_REGEX
        pass

    @classmethod
    def validate_gwa(cls, value: Optional[str]) -> float:
        """
        Defensively parses string to float and checks 1.00 <= GWA <= 5.00.
        Returns: Parsed float value.
        Raises: GWARangeError if out of bounds or non-numeric.
        """
        # TODO: Implement defensive float parsing and range check
        pass


# ============================================================================
# TIER 1: FLET PRESENTATION LAYER
# ============================================================================

def main(page: ft.Page):
    page.title = "CSPC Scholarship Intake Portal"
    page.window.width = 620
    page.window.height = 780
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 25

    # Storage for approved applications during this session
    approved_applicants: list[ScholarshipApplicant] = []

    # UI Controls
    name_field = ft.TextField(
        label="Full Name",
        hint_text="e.g., Maria Clara Santos",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius=8
    )

    id_field = ft.TextField(
        label="Student ID Number",
        hint_text="e.g., 2024-0123",
        prefix_icon=ft.Icons.BADGE_OUTLINED,
        border_radius=8
    )

    email_field = ft.TextField(
        label="Institutional Email",
        hint_text="e.g., mclara.santos@cspc.edu.ph",
        prefix_icon=ft.Icons.ALTERNATE_EMAIL,
        border_radius=8
    )

    phone_field = ft.TextField(
        label="Philippine Mobile Number",
        hint_text="e.g., 09181234567 or +639181234567",
        prefix_icon=ft.Icons.PHONE_ANDROID_OUTLINED,
        border_radius=8
    )

    gwa_field = ft.TextField(
        label="Academic General Weighted Average (GWA)",
        hint_text="Scale: 1.00 (highest) to 5.00 (passing/failing)",
        prefix_icon=ft.Icons.GRADE_OUTLINED,
        border_radius=8
    )

    program_dropdown = ft.Dropdown(
        label="Scholarship Program",
        hint_text="Select your scholarship grant",
        leading_icon=ft.Icons.SCHOOL_OUTLINED,
        border_radius=8,
        options=[
            ft.dropdown.Option("CHED Tulong Dunong Program (TDP)"),
            ft.dropdown.Option("DOST Science & Technology Scholarship"),
            ft.dropdown.Option("CSPC Institutional Academic Scholarship"),
            ft.dropdown.Option("UniFAST Tertiary Education Subsidy (TES)"),
        ]
    )

    status_summary = ft.Text(
        value="Ready to accept applications.",
        color=ft.Colors.GREY_400,
        size=13
    )

    # ------------------------------------------------------------------------
    # REAL-TIME ERROR CLEARING HANDLERS (UX ENHANCEMENT)
    # ------------------------------------------------------------------------
    def clear_field_error(e):
        """Instantly clears error state when the user begins typing."""
        if e.control.error:
            e.control.error = None
            page.update()

    def clear_dropdown_error(e):
        """Instantly clears dropdown error state on selection."""
        if e.control.error_text:
            e.control.error_text = None
            page.update()

    name_field.on_change = clear_field_error
    id_field.on_change = clear_field_error
    email_field.on_change = clear_field_error
    phone_field.on_change = clear_field_error
    gwa_field.on_change = clear_field_error
    program_dropdown.on_change = clear_dropdown_error

    # ------------------------------------------------------------------------
    # FORM SUBMISSION & MULTI-TIER DEFENSIVE PIPELINE
    # ------------------------------------------------------------------------
    def submit_application(e):
        has_errors = False

        # Reset all error states before evaluation
        name_field.error = None
        id_field.error = None
        email_field.error = None
        phone_field.error = None
        gwa_field.error = None
        program_dropdown.error_text = None

        # 1. Validate Name
        try:
            clean_name = ScholarshipValidator.validate_name(name_field.value)
        except ScholarshipValidationError as err:
            name_field.error = str(err)
            has_errors = True

        # 2. Validate Student ID
        # TODO: Wrap validate_student_id in try...except and set id_field.error
        clean_id = None

    # ------------------------------------------------------------------------
    # 5. GWA NUMERIC & RANGE VALIDATION
    # ------------------------------------------------------------------------
    def test_valid_gwa(self):
        self.assertEqual(ScholarshipValidator.validate_gwa("1.00"), 1.00)
        self.assertEqual(ScholarshipValidator.validate_gwa(" 1.45 "), 1.45)
        self.assertEqual(ScholarshipValidator.validate_gwa("5.00"), 5.00)

    def test_invalid_gwa_out_of_bounds(self):
        with self.assertRaises(GWARangeError):
            ScholarshipValidator.validate_gwa("0.95")  # Beyond highest honor
        with self.assertRaises(GWARangeError):
            ScholarshipValidator.validate_gwa("5.25")  # Beyond failing bound
        with self.assertRaises(GWARangeError):
            ScholarshipValidator.validate_gwa("-1.50")

    def test_invalid_gwa_non_numeric(self):
        with self.assertRaises(GWARangeError):
            ScholarshipValidator.validate_gwa("uno")
        with self.assertRaises(GWARangeError):
            ScholarshipValidator.validate_gwa("1.45GPA")
        with self.assertRaises(GWARangeError):
            ScholarshipValidator.validate_gwa("")

    # ------------------------------------------------------------------------
    # 6. DOMAIN CONTRACT (@DATACLASS) IMMUTABILITY
    # ------------------------------------------------------------------------
    def test_dataclass_contract_creation(self):
        applicant = ScholarshipApplicant(
            full_name="Maria Clara Santos",
            student_id="2024-0891",
            email="mclara.santos@cspc.edu.ph",
            phone="09181234567",
            gwa=1.45,
            program="DOST Science & Technology Scholarship"
        )
        self.assertEqual(applicant.full_name, "Maria Clara Santos")
        self.assertEqual(applicant.gwa, 1.45)

        # Frozen contract test (mutation must raise FrozenInstanceError)
        with self.assertRaises(Exception):
            applicant.gwa = 1.00

    # ------------------------------------------------------------------------
    # 7. GUI EVENT FLOW INTEGRATION TEST (MOCK RUNNER)
    # ------------------------------------------------------------------------
    def test_gui_submission_flow(self):
        from unittest.mock import MagicMock
        import flet as ft
        import scholarship_portal

        mock_page = MagicMock()
        mock_page.window = MagicMock()
        mock_page.show_dialog = MagicMock()
        mock_page.update = MagicMock()

        # Initialize GUI
        scholarship_portal.main(mock_page)

        col = mock_page.add.call_args[0][0]
        submit_btn = next(c for c in col.controls if isinstance(c, ft.FilledButton))
        name_field = col.controls[2]
        id_field = col.controls[3]
        email_field = col.controls[4]
        phone_field = col.controls[5]
        gwa_field = col.controls[6]
        program_dropdown = col.controls[7]

        # Trigger submission on invalid empty fields
        submit_btn.on_click(MagicMock())
        self.assertIsNotNone(name_field.error)
        self.assertTrue(mock_page.show_dialog.called)

        # Populate valid applicant data
        name_field.value = "Maria Clara Santos"
        id_field.value = "2024-0891"
        email_field.value = "mclara.santos@cspc.edu.ph"
        phone_field.value = "09181234567"
        gwa_field.value = "1.45"
        program_dropdown.value = "DOST Science & Technology Scholarship"

        # Trigger valid submission (builds dataclass and card with ft.Border.all)
        mock_page.show_dialog.reset_mock()
        submit_btn.on_click(MagicMock())
        self.assertIsNone(name_field.error)
        self.assertTrue(mock_page.show_dialog.called)


if __name__ == "__main__":
    unittest.main()