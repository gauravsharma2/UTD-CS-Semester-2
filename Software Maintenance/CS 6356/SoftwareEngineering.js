class SoftwareEngineering {
    definition = "a branch of engineering that deals with design, implementation, and maintenance of complex computer programs.";
    answerLength = 0;
    noOfQuestions = 0;

    whatIsSoftwareEngineering() {
        return definition;
    }
    useWords() {
        let perfect = 100;
        let answer = 0;
        if (answer != perfect) {
            return "try using words this time.";
        }
    }
    makeASentence() {
        if (answerLength === 1) {
            return "that was just a word. try to make a sentence, please.";
        }
    }
    askQuestions() {
        if (noOfQuestions <= 4) {
            return "look, this is a discussion. if we do not get more questions, i will start asking you more questions.";
        }
    }
    copyAndPaste() {
        let copyResponse = "";
        if (copyResponse === definition) {
            return "this sounds like a copy paste response. what do those words mean?";
        }
    }
    why() {
        return "just why?";
    }
    calcGrade() {
        let participation = 0;
        let quiz = 0;
        let exam = 0;
        let hw = 0;

        if (participation === 10 && quiz === 15 && exam === 30 && hw === 15) {
            grade = "A";
        }
    }
    presentationFeedback() {
        let feedback = "";
        if (feedback === "this was alright, but I still don't understand what software engineering is") {
            return "we are in trouble";
        }
    }
    loadSlides() {
        return "slides are loading. please wait.";
    }
    updateSyllabus() {
        let finalDate = "May 6th, 2023";
        return (finalDate + " is the final date. No changes.");
    }
}