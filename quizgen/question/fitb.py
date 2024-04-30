import quizgen.common
import quizgen.constants
import quizgen.question.base

class FITB(quizgen.question.base.Question, question_type = quizgen.constants.QUESTION_TYPE_FITB):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validate_answers(self):
        """
        Set up the answers to look like fill in multiple blanks with an empty key.
        """

        # Standardize an alternate format.
        # Note that this is the format we will eventually output,
        # but we want to validate the user-facing format so errors are more clear.
        if (isinstance(self.answers, dict)):
            if (len(self.answers) != 1):
                raise quizgen.common.QuizValidationError("Dict format should have exactly one entry (''), found %d entries." % (len(self.answers)))

            if ('' not in self.answers):
                raise quizgen.common.QuizValidationError("Dict format does not have required key '' (empty string).")

            self.answers = self.answers['']

            # If this was already in the full FIMB format, then we need to pull out the values.
            if ((isinstance(self.answers, dict)) and ('values' in self.answers)):
                self.answers = self.answers['values']

        self._check_type(self.answers, list, f"'answers' value")

        if (len(self.answers) == 0):
            raise quizgen.common.QuizValidationError("Expected 'answers' value to be non-empty.")

        self.answers = {'': self.answers}

        self._validate_fimb_answers()
