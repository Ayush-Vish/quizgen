#!/usr/bin/env python3

import os
import shutil
import unittest
import logging

import quizgen.latex
import quizgen.pdf
import quizgen.util.dirent
import quizgen.util.json
import tests.base

class TestDockerPdfConversion(tests.base.BaseTest):
    def test_quiz_to_pdf(self):
        if not quizgen.latex.is_available(use_docker=True):
            self.skipTest("Docker is not installed or not running")

        source_quiz_path = tests.base.discover_good_quiz_files()[1]
        logging.warning("source path '%s" , source_quiz_path)     
        if not os.path.exists(source_quiz_path):
            self.skipTest(f"Quiz file '{source_quiz_path}' not found")

        temp_dir = quizgen.util.dirent.get_temp_path()
        quiz_json_path = os.path.join(temp_dir, "quiz.json")
        logging.warning("quiz_json_path '%s" , quiz_json_path)
        quizgen.util.dirent.copy_dirent(source_quiz_path, quiz_json_path)

        # Load quiz to get title
        quiz_data = quizgen.util.json.load_path(quiz_json_path)

        logging.warning("quiz_data '%s" , quiz_data)
        
        quiz_title = quiz_data.get("title", "Single Question Quiz")

        # Generate PDF with Docker
        quizgen.latex.set_pdflatex_use_docker(True)
        quizgen.pdf.make_with_path(quiz_json_path, base_out_dir=temp_dir)
        pdf_file = os.path.join(temp_dir, quiz_title, f"{quiz_title}.pdf")

        self.assertTrue(os.path.exists(pdf_file), f"PDF file '{pdf_file}' was not generated")
        self.assertGreater(os.path.getsize(pdf_file), 1000, f"Generated PDF '{pdf_file}' is too small")

        # Cleanup
        quizgen.util.dirent.remove_dirent(temp_dir)

    # def test_quiz_with_image_to_pdf(self):
    #     if not quizgen.latex.is_available(use_docker=True):
    #         self.skipTest("Docker is not installed or not running")

    #     # Create a quiz with an image based on tests/questions/good/prompt-image/
    #     source_image_quiz_dir = os.path.join("tests", "questions", "good", "prompt-image")
    #     source_question_path = os.path.join(source_image_quiz_dir, "question.json")
    #     source_image_path = os.path.join(source_image_quiz_dir, "prompt.md")
    #     if not os.path.exists(source_question_path) or not os.path.exists(source_image_path):
    #         self.skipTest(f"Image quiz files not found in '{source_image_quiz_dir}'")

    #     # Setup temporary directory
    #     temp_dir = quizgen.util.dirent.get_temp_path()
    #     temp_quiz_dir = os.path.join(temp_dir, "image_quiz")
    #     os.makedirs(temp_quiz_dir, exist_ok=True)

    #     # Construct a quiz JSON using the question with an image
    #     quiz_json = {
    #         "title": "Image Test Quiz",
    #         "description": "A quiz with an image question",
    #         "questions": [quizgen.util.json.load_path(source_question_path)]
    #     }
    #     quiz_json_path = os.path.join(temp_quiz_dir, "quiz.json")
    #     quizgen.util.json.dump_path(quiz_json, quiz_json_path, indent=4)

    #     # Copy the image file (prompt.md references an image)
    #     shutil.copy(source_image_path, temp_quiz_dir)

    #     # Generate PDF with Docker
    #     quizgen.latex.set_pdflatex_use_docker(True)
    #     quizgen.pdf.make_with_path(quiz_json_path, base_out_dir=temp_dir)
    #     pdf_file = os.path.join(temp_dir, "Image Test Quiz", "Image Test Quiz.pdf")

    #     self.assertTrue(os.path.exists(pdf_file), f"PDF file '{pdf_file}' was not generated")
    #     self.assertGreater(os.path.getsize(pdf_file), 1000, f"Generated PDF '{pdf_file}' is too small")

    #     # Cleanup
    #     quizgen.util.dirent.remove_dirent(temp_dir)
