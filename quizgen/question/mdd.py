import quizgen.common
import quizgen.constants
import quizgen.parser.parse
import quizgen.question.base

class MDD(quizgen.question.base.Question, question_type = quizgen.constants.QUESTION_TYPE_MDD):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validate_answers(self):
        self._check_type(self.answers, dict, "'answers' key")

        if (len(self.answers) == 0):
            raise quizgen.common.QuizValidationError("No answers provided, at least one answer required.")

        for (key, answers) in list(self.answers.items()):
            # If this was already in the full MDD format, then we need to pull out the values.
            if ((isinstance(answers, dict)) and ('values' in answers)):
                answers = answers['values']

            values = self._validate_answer_list(answers, self.base_dir, min_correct = 1, max_correct = 1)

            self.answers[key] = {
                'key': {
                    'text': key,
                    'document': quizgen.parser.parse.parse_text(key, base_dir = self.base_dir),
                },
                'values': values,
            }

    def _shuffle(self, rng):
        for key in self.answers:
            rng.shuffle(self.answers[key]['values'])
