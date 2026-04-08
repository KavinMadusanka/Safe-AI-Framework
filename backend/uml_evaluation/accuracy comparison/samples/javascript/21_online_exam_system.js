// 21_online_exam_system.js
// Online Exam System — 4-layer architecture
// Classes: Exam, Question, IExamRepository, ExamRepository,
//          ExamService, ExamController, DatabaseConnection

// ── Models ─────────────────────────────────────────────────────────────────

class Question {
    constructor(questionId, examId, text, marks) {
        this.questionId = questionId;
        this.examId     = examId;
        this.text       = text;
        this.marks      = marks;
        this.options    = [];
        this.answer     = null;
    }

    getQuestionId() { return this.questionId; }
    getExamId()     { return this.examId; }
    getText()       { return this.text; }
    getMarks()      { return this.marks; }
    getOptions()    { return this.options; }
    getAnswer()     { return this.answer; }

    setAnswer(answer) { this.answer = answer; }
    addOption(option) { this.options.push(option); }
}

class Exam {
    constructor(examId, title, courseId, duration) {
        this.examId    = examId;
        this.title     = title;
        this.courseId  = courseId;
        this.duration  = duration;
        this.published = false;
        this.questions = [];
    }

    getExamId()    { return this.examId; }
    getTitle()     { return this.title; }
    getCourseId()  { return this.courseId; }
    getDuration()  { return this.duration; }
    isPublished()  { return this.published; }
    getQuestions() { return this.questions; }

    setPublished(published)  { this.published = published; }
    addQuestion(question)    { this.questions.push(question); }
}

// ── Repository Interface ───────────────────────────────────────────────────

class IExamRepository {
    findExamById(examId)           { throw new Error("Not implemented"); }
    findAllExams()                 { throw new Error("Not implemented"); }
    findExamsByCourse(courseId)    { throw new Error("Not implemented"); }
    saveExam(exam)                 { throw new Error("Not implemented"); }
    deleteExam(examId)             { throw new Error("Not implemented"); }
    saveQuestion(question)         { throw new Error("Not implemented"); }
    findQuestionsByExam(examId)    { throw new Error("Not implemented"); }
    deleteQuestion(questionId)     { throw new Error("Not implemented"); }
}

// ── Database Layer ─────────────────────────────────────────────────────────

class DatabaseConnection {
    constructor(connectionString) {
        this.connectionString = connectionString;
        this.connected        = false;
    }

    connect()          { this.connected = true; }
    disconnect()       { this.connected = false; }
    isConnected()      { return this.connected; }
    getConnectionString() { return this.connectionString; }
}

// ── Repository Implementation ──────────────────────────────────────────────

class ExamRepository extends IExamRepository {
    constructor(connection) {
        super();
        this.connection = connection;
    }

    findExamById(examId) {
        this.connection.connect();
        return null;
    }

    findAllExams() {
        this.connection.connect();
        return [];
    }

    findExamsByCourse(courseId) {
        this.connection.connect();
        return [];
    }

    saveExam(exam) {
        this.connection.connect();
    }

    deleteExam(examId) {
        this.connection.connect();
    }

    saveQuestion(question) {
        this.connection.connect();
    }

    findQuestionsByExam(examId) {
        this.connection.connect();
        return [];
    }

    deleteQuestion(questionId) {
        this.connection.connect();
    }
}

// ── Service Layer ──────────────────────────────────────────────────────────

class ExamService {
    constructor(repository) {
        this.repository = repository;
    }

    getExam(examId) {
        return this.repository.findExamById(examId);
    }

    getAllExams() {
        return this.repository.findAllExams();
    }

    getExamsByCourse(courseId) {
        return this.repository.findExamsByCourse(courseId);
    }

    createExam(exam) {
        this._validateExam(exam);
        this.repository.saveExam(exam);
    }

    publishExam(examId) {
        const exam = this.repository.findExamById(examId);
        exam.setPublished(true);
        this.repository.saveExam(exam);
    }

    deleteExam(examId) {
        this.repository.deleteExam(examId);
    }

    addQuestion(question) {
        this.repository.saveQuestion(question);
    }

    removeQuestion(questionId) {
        this.repository.deleteQuestion(questionId);
    }

    getQuestions(examId) {
        return this.repository.findQuestionsByExam(examId);
    }

    _validateExam(exam) {
        if (!exam.getTitle()) throw new Error("Exam title cannot be empty");
        if (exam.getDuration() <= 0) throw new Error("Duration must be positive");
    }
}

// ── Controller Layer ───────────────────────────────────────────────────────

class ExamController {
    constructor(service) {
        this.service = service;
    }

    handleGetExam(examId)          { return this.service.getExam(examId); }
    handleGetAllExams()            { return this.service.getAllExams(); }
    handleGetByCourse(courseId)    { return this.service.getExamsByCourse(courseId); }
    handleCreateExam(exam)         { this.service.createExam(exam); }
    handlePublishExam(examId)      { this.service.publishExam(examId); }
    handleDeleteExam(examId)       { this.service.deleteExam(examId); }
    handleAddQuestion(question)    { this.service.addQuestion(question); }
    handleRemoveQuestion(qId)      { this.service.removeQuestion(qId); }
    handleGetQuestions(examId)     { return this.service.getQuestions(examId); }
}

module.exports = {
    Question, Exam, IExamRepository, ExamRepository,
    ExamService, ExamController, DatabaseConnection
};