# ground_truth_21.py
# Hand-verified ground truth for 21_online_exam_system.js
#
# Source has:
#   Classes: Question, Exam, IExamRepository, ExamRepository,
#            ExamService, ExamController, DatabaseConnection
#   Architecture: 4-layer Controller -> Service -> Repository -> DB
#   Language: JavaScript (ES6 classes, extends)

SAMPLE   = "21_online_exam_system.js"
LANGUAGE = "javascript"

# ── CLASS DIAGRAM ──────────────────────────────────────────────────────────
CLASS_GT = {
    "classes": {
        "Question", "Exam", "IExamRepository",
        "ExamRepository", "ExamService", "ExamController", "DatabaseConnection"
    },
    "fields": {
        "Question.questionId", "Question.examId", "Question.text",
        "Question.marks", "Question.options", "Question.answer",
        "Exam.examId", "Exam.title", "Exam.courseId",
        "Exam.duration", "Exam.published", "Exam.questions",
        "ExamRepository.connection",
        "ExamService.repository",
        "ExamController.service",
        "DatabaseConnection.connectionString", "DatabaseConnection.connected",
    },
    "methods": {
        "Question.getQuestionId", "Question.getExamId", "Question.getText",
        "Question.getMarks", "Question.getOptions", "Question.getAnswer",
        "Question.setAnswer", "Question.addOption",
        "Exam.getExamId", "Exam.getTitle", "Exam.getCourseId",
        "Exam.getDuration", "Exam.isPublished", "Exam.getQuestions",
        "Exam.setPublished", "Exam.addQuestion",
        "IExamRepository.findExamById", "IExamRepository.findAllExams",
        "IExamRepository.findExamsByCourse", "IExamRepository.saveExam",
        "IExamRepository.deleteExam", "IExamRepository.saveQuestion",
        "IExamRepository.findQuestionsByExam", "IExamRepository.deleteQuestion",
        "ExamRepository.findExamById", "ExamRepository.findAllExams",
        "ExamRepository.findExamsByCourse", "ExamRepository.saveExam",
        "ExamRepository.deleteExam", "ExamRepository.saveQuestion",
        "ExamRepository.findQuestionsByExam", "ExamRepository.deleteQuestion",
        "ExamService.getExam", "ExamService.getAllExams",
        "ExamService.getExamsByCourse", "ExamService.createExam",
        "ExamService.publishExam", "ExamService.deleteExam",
        "ExamService.addQuestion", "ExamService.removeQuestion",
        "ExamService.getQuestions", "ExamService._validateExam",
        "ExamController.handleGetExam", "ExamController.handleGetAllExams",
        "ExamController.handleGetByCourse", "ExamController.handleCreateExam",
        "ExamController.handlePublishExam", "ExamController.handleDeleteExam",
        "ExamController.handleAddQuestion", "ExamController.handleRemoveQuestion",
        "ExamController.handleGetQuestions",
        "DatabaseConnection.connect", "DatabaseConnection.disconnect",
        "DatabaseConnection.isConnected", "DatabaseConnection.getConnectionString",
    },
    "relationships": {
        ("implements", "ExamRepository",  "IExamRepository"),
        ("associates", "ExamRepository",  "DatabaseConnection"),
        ("associates", "ExamService",     "IExamRepository"),
        ("associates", "ExamController",  "ExamService"),
        ("depends_on", "IExamRepository", "Exam"),
        ("depends_on", "IExamRepository", "Question"),
        ("depends_on", "ExamRepository",  "Exam"),
        ("depends_on", "ExamRepository",  "Question"),
        ("depends_on", "ExamService",     "Exam"),
        ("depends_on", "ExamService",     "Question"),
        ("depends_on", "ExamController",  "Exam"),
        ("depends_on", "ExamController",  "Question"),
    }
}
CLASS_VERIFIED = True

# ── PACKAGE DIAGRAM ────────────────────────────────────────────────────────
PACKAGE_GT = {
    "packages": set(),
    "members": {
        "Question", "Exam", "IExamRepository",
        "ExamRepository", "ExamService", "ExamController", "DatabaseConnection"
    },
    "dependencies": {
        "ExamRepository->IExamRepository",
        "ExamRepository->DatabaseConnection",
        "ExamService->IExamRepository",
        "ExamController->ExamService",
    }
}
PACKAGE_VERIFIED = True

# ── SEQUENCE DIAGRAM ───────────────────────────────────────────────────────
SEQUENCE_GT = {
    "participants": {
        "ExamController",
        "ExamService",
        "ExamRepository",
    },
    "key_messages": {
        "ExamController->ExamService:getExam",
        "ExamController->ExamService:createExam",
        "ExamController->ExamService:publishExam",
        "ExamService->ExamRepository:findExamById",
        "ExamService->ExamRepository:saveExam",
        "ExamService->ExamRepository:saveQuestion",
    }
}
SEQUENCE_VERIFIED = True

# ── COMPONENT DIAGRAM ──────────────────────────────────────────────────────
COMPONENT_GT = {
    "components": {
        "Question", "Exam", "IExamRepository",
        "ExamRepository", "ExamService", "ExamController", "DatabaseConnection"
    },
    "interfaces": {
        "IExamRepository", "ExamService", "DatabaseConnection"
    },
    "connections": {
        "ExamRepository->DatabaseConnection",
        "ExamService->IExamRepository",
        "ExamController->ExamService",
    }
}
COMPONENT_VERIFIED = True

# ── ACTIVITY DIAGRAM ───────────────────────────────────────────────────────
ACTIVITY_GT = {
    "actions": {
        "getExam", "getAllExams", "getExamsByCourse",
        "createExam", "publishExam", "deleteExam",
        "addQuestion", "removeQuestion", "getQuestions",
        "findExamById", "saveExam",
    },
    "decisions": {
        "more items",
    },
    "swimlanes": set()
}
ACTIVITY_VERIFIED = True